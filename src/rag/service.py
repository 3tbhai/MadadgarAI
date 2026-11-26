"""Multi-Tenant Private Knowledge Base Ingestion, Hybrid RRF Retrieval & Streaming Grounded RAG Service."""
import asyncio
import hashlib
import logging
from typing import Any, AsyncIterator, Dict, List, Optional, Tuple
import uuid
import numpy as np
from rank_bm25 import BM25Okapi

from src.auth.database import SaralMultiTenantDB
from src.config import RRF_K_CONSTANT
from src.core.logging_utils import log_structured_event
from src.embeddings.hybrid_search import tokenize_text
from src.rag.chunker import LayoutAwareChunker, ParsedPage
from src.rag.gemini_client import GeminiRAGClient

logger = logging.getLogger("MadadgaarAI.RAG.Service")

MAX_UPLOAD_BYTES = 15 * 1024 * 1024  # 15 MB
ALLOWED_EXTENSIONS = {".pdf", ".md", ".markdown", ".txt"}
ALLOWED_MIME_PREFIXES = ("application/pdf", "text/plain", "text/markdown", "application/octet-stream")
CHUNK_SIZE_TOKENS = 800
CHUNK_OVERLAP_TOKENS = 150
RETRIEVAL_TOP_K = 6

SARAL_SYSTEM_PROMPT = (
    "You are Saral AI — a clear, accurate document assistant.\n"
    "GUIDELINES:\n"
    "1. Give clear, structured explanations grounded strictly in the provided Retrieved Context Chunks.\n"
    "2. Highlight key definitions, deadlines, requirements, or formulas (in LaTeX $...$ / $$...$$) when relevant.\n"
    "3. Attach inline citations immediately after factual claims using exact format: [Source: <Document Name>, Page <N> / <Section>].\n"
    "4. If the uploaded documents do not contain enough evidence to answer the question, explicitly state that the uploaded materials do not cover this topic rather than guessing or hallucinating."
)


def _cosine_sim(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    va = np.asarray(a, dtype=np.float32)
    vb = np.asarray(b, dtype=np.float32)
    na = float(np.linalg.norm(va))
    nb = float(np.linalg.norm(vb))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(np.dot(va, vb) / (na * nb))


class MultiTenantRAGService:
    """
    Production multi-tenant RAG engine enforcing strict `user_id` isolation at every layer:
    - Async background ingestion with job status tracking (pending -> processing -> indexed / failed)
    - SHA-256 content deduplication per user
    - Gemini embeddings (`RETRIEVAL_DOCUMENT` / `RETRIEVAL_QUERY`) + Hybrid Vector/BM25 RRF retrieval
    - Grounded streaming generation with clickable citations
    """

    def __init__(
        self,
        db: Optional[SaralMultiTenantDB] = None,
        gemini_client: Optional[GeminiRAGClient] = None,
        chunker: Optional[LayoutAwareChunker] = None,
    ):
        self.db = db or SaralMultiTenantDB()
        self.gemini = gemini_client or GeminiRAGClient()
        self.chunker = chunker or LayoutAwareChunker()

    def validate_file_upload(self, filename: str, mime_type: str, file_bytes: bytes) -> str:
        if not file_bytes:
            raise ValueError("Uploaded file is empty.")
        if len(file_bytes) > MAX_UPLOAD_BYTES:
            raise ValueError(f"File exceeds maximum allowed size of {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.")
        lower = (filename or "document.txt").lower()
        ext = "." + lower.rsplit(".", 1)[-1] if "." in lower else ""
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file extension '{ext}'. Allowed: PDF, Markdown (.md), Plain Text (.txt).")
        clean_mime = (mime_type or "text/plain").split(";")[0].strip().lower()
        if not any(clean_mime.startswith(p) for p in ALLOWED_MIME_PREFIXES):
            raise ValueError(f"Unsupported MIME type '{clean_mime}'.")
        return clean_mime

    def prepare_file_document(
        self,
        user: Dict[str, Any],
        filename: str,
        mime_type: str,
        file_bytes: bytes,
    ) -> Tuple[Dict[str, Any], bool]:
        """Creates a pending document record (or returns existing duplicate via per-user SHA-256). Returns (doc, is_duplicate)."""
        clean_mime = self.validate_file_upload(filename, mime_type, file_bytes)
        content_hash = hashlib.sha256(file_bytes).hexdigest()
        existing = self.db.find_document_by_hash(user_id=user["id"], content_sha256=content_hash)
        if existing and existing["status"] == "indexed":
            return existing, True
        if existing:
            self.db.delete_user_document(existing["id"], user["id"])

        title = filename.rsplit(".", 1)[0].strip() or filename
        src_type = "pdf" if filename.lower().endswith(".pdf") or file_bytes[:4] == b"%PDF" else ("markdown" if filename.lower().endswith((".md", ".markdown")) else "text")
        doc = self.db.create_document(
            user_id=user["id"],
            title=title[:140],
            source_type=src_type,
            mime_type=clean_mime,
            file_size_bytes=len(file_bytes),
            content_sha256=content_hash,
            source_uri=filename,
        )
        return doc, False

    async def process_file_job(
        self, doc_id: str, user_id: str, title: str, source_type: str, file_bytes: bytes
    ) -> None:
        """Background job: extracts layout-aware pages, chunks, embeds via Gemini, and persists vectors."""
        self.db.update_document_status(doc_id, user_id, status="processing")
        try:
            if source_type == "pdf":
                pages = await asyncio.to_thread(self.chunker.extract_pdf_pages, file_bytes)
            else:
                decoded = file_bytes.decode("utf-8", errors="ignore")
                pages = self.chunker.extract_markdown_sections(decoded)

            if not pages:
                raise ValueError("No readable text found in document.")

            chunks = self.chunker.chunk_pages(
                pages,
                chunk_size_tokens=CHUNK_SIZE_TOKENS,
                chunk_overlap_tokens=CHUNK_OVERLAP_TOKENS,
            )
            if not chunks:
                raise ValueError("Document did not produce any indexable text chunks.")

            texts = [f"{title} | {c.section_header}\n{c.content}" for c in chunks]
            embeddings = await asyncio.to_thread(self.gemini.embed_texts, texts, "RETRIEVAL_DOCUMENT")

            chunk_rows: List[Dict[str, Any]] = []
            for ch, emb in zip(chunks, embeddings):
                chunk_rows.append({
                    "id": f"chk_{uuid.uuid4().hex[:14]}",
                    "doc_title": title,
                    "page_number": ch.page_number,
                    "section_header": ch.section_header,
                    "chunk_index": ch.chunk_index,
                    "content": ch.content,
                    "token_count": ch.token_count,
                    "embedding": emb,
                })

            saved_count = self.db.replace_document_chunks(doc_id=doc_id, user_id=user_id, chunks=chunk_rows)
            self.db.update_document_status(doc_id, user_id, status="indexed", chunk_count=saved_count)
            log_structured_event(logger, "document_indexed", user_id=user_id, doc_id=doc_id, chunks=saved_count)
        except Exception as exc:
            logger.error(f"Document ingestion failed for doc={doc_id}: {exc}")
            self.db.update_document_status(doc_id, user_id, status="failed", error_message=str(exc)[:240])

    async def prepare_and_process_url(
        self, user: Dict[str, Any], url: str, custom_title: Optional[str] = None
    ) -> Tuple[Dict[str, Any], bool]:
        """Fetches a remote URL / arXiv link, deduplicates per user, and indexes its chunks."""
        title, mime_type, pages = await self.chunker.fetch_url_content(url)
        final_title = (custom_title or title or url).strip()[:140]
        full_text = "\n\n".join(p.text for p in pages)
        if len(full_text.strip()) < 30:
            raise ValueError("Fetched URL did not contain enough readable text.")

        raw_bytes = full_text.encode("utf-8")
        content_hash = hashlib.sha256(raw_bytes).hexdigest()
        existing = self.db.find_document_by_hash(user["id"], content_hash)
        if existing and existing["status"] == "indexed":
            return existing, True
        if existing:
            self.db.delete_user_document(existing["id"], user["id"])

        doc = self.db.create_document(
            user_id=user["id"],
            title=final_title,
            source_type="url",
            mime_type=mime_type,
            file_size_bytes=len(raw_bytes),
            content_sha256=content_hash,
            source_uri=url.strip(),
        )
        self.db.update_document_status(doc["id"], user["id"], status="processing")
        try:
            chunks = self.chunker.chunk_pages(
                pages,
                chunk_size_tokens=CHUNK_SIZE_TOKENS,
                chunk_overlap_tokens=CHUNK_OVERLAP_TOKENS,
            )
            texts = [f"{final_title} | {c.section_header}\n{c.content}" for c in chunks]
            embeddings = await asyncio.to_thread(self.gemini.embed_texts, texts, "RETRIEVAL_DOCUMENT")
            chunk_rows = [
                {
                    "id": f"chk_{uuid.uuid4().hex[:14]}",
                    "doc_title": final_title,
                    "page_number": ch.page_number,
                    "section_header": ch.section_header,
                    "chunk_index": ch.chunk_index,
                    "content": ch.content,
                    "token_count": ch.token_count,
                    "embedding": emb,
                }
                for ch, emb in zip(chunks, embeddings)
            ]
            saved = self.db.replace_document_chunks(doc["id"], user["id"], chunk_rows)
            self.db.update_document_status(doc["id"], user["id"], status="indexed", chunk_count=saved)
            updated = self.db.get_user_document(doc["id"], user["id"]) or doc
            return updated, False
        except Exception as exc:
            self.db.update_document_status(doc["id"], user["id"], status="failed", error_message=str(exc)[:240])
            raise

    def hybrid_retrieve(
        self,
        user_id: str,
        query: str,
        doc_ids: Optional[List[str]] = None,
        top_k: int = RETRIEVAL_TOP_K,
    ) -> List[Dict[str, Any]]:
        """
        Tenant-isolated Hybrid Retrieval (Dense Vector Cosine + BM25 Lexical via Reciprocal Rank Fusion).
        Enforces strict WHERE user_id = :current_user_id pre-filtering.
        """
        chunks = self.db.load_user_chunks(user_id=user_id, doc_ids=doc_ids)
        if not chunks:
            return []

        q_tokens = tokenize_text(query)
        corpus_texts = [f"{c['doc_title']} {c['section_header']} {c['content']}" for c in chunks]
        corpus_tokens = [tokenize_text(t) for t in corpus_texts]

        # 1. BM25 lexical scoring
        bm25_ranks: Dict[int, int] = {}
        bm25_raw: Dict[int, float] = {}
        if q_tokens and any(corpus_tokens):
            bm25 = BM25Okapi(corpus_tokens)
            scores = bm25.get_scores(q_tokens)
            ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
            for rank, idx in enumerate(ranked, start=1):
                bm25_ranks[idx] = rank
                bm25_raw[idx] = float(scores[idx])

        # 2. Dense vector similarity scoring (uses native pgvector HNSW when on PostgreSQL)
        q_vecs = self.gemini.embed_texts([query], task_type="RETRIEVAL_QUERY")
        q_vec = q_vecs[0] if q_vecs else []
        pg_hits = self.db.vector_search_user_chunks(
            user_id=user_id,
            query_embedding=q_vec,
            top_k=max(len(chunks), top_k * 3),
            doc_ids=doc_ids,
        )
        if pg_hits is not None:
            sim_by_id = {h["id"]: float(h.get("dense_sim") or 0.0) for h in pg_hits}
            dense_sims = [sim_by_id.get(c["id"], 0.0) for c in chunks]
        else:
            dense_sims = [_cosine_sim(q_vec, c["embedding"]) for c in chunks]
        ranked_dense = sorted(range(len(dense_sims)), key=lambda i: dense_sims[i], reverse=True)
        dense_ranks = {idx: rank for rank, idx in enumerate(ranked_dense, start=1)}

        # 3. Reciprocal Rank Fusion + Evidence Gate
        max_rrf = 2.0 / (RRF_K_CONSTANT + 1)
        q_low = query.lower().strip()
        scored: List[Tuple[Dict[str, Any], float]] = []

        for idx, ch in enumerate(chunks):
            r_b = bm25_ranks.get(idx, len(chunks) + 1)
            r_d = dense_ranks.get(idx, len(chunks) + 1)
            rrf = (1.0 / (RRF_K_CONSTANT + r_b)) + (1.0 / (RRF_K_CONSTANT + r_d))
            norm_rrf = min(1.0, rrf / max_rrf)

            text_low = corpus_texts[idx].lower()
            token_overlap = sum(1 for tok in q_tokens if tok in text_low)
            sim = dense_sims[idx]
            b_score = bm25_raw.get(idx, 0.0)

            # Filter out completely unrelated noise chunks so we don't hallucinate on off-topic queries
            if token_overlap == 0 and sim < 0.22 and b_score <= 0.0 and q_low not in text_low:
                continue

            final_score = round(min(1.0, 0.55 * norm_rrf + 0.30 * max(0.0, sim) + 0.15 * min(1.0, token_overlap / max(1, len(q_tokens)))), 4)
            scored.append((ch, final_score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top_chunks: List[Dict[str, Any]] = []
        for ch, score in scored[:top_k]:
            item = {k: v for k, v in ch.items() if k != "embedding"}
            item["score"] = score
            top_chunks.append(item)
        return top_chunks

    def _build_generation_prompt(
        self,
        query: str,
        history: List[Dict[str, Any]],
        retrieved: List[Dict[str, Any]],
    ) -> str:
        hist_lines = [
            f"{m['role'].upper()}: {m['content'][:350]}"
            for m in history[-6:]
        ]
        ctx_blocks = [
            f"[Chunk {idx} | id={c['id']}] Document: {c['doc_title']} | Page: {c['page_number']} | Section: {c['section_header']}\n{c['content']}"
            for idx, c in enumerate(retrieved, start=1)
        ]
        parts = []
        if hist_lines:
            parts.append("Recent Conversation History:\n" + "\n".join(hist_lines))
        parts.append("Retrieved Context Chunks (Strictly Private User Knowledge Base):\n" + "\n\n".join(ctx_blocks))
        parts.append(f"Current User Question:\n{query}")
        return "\n\n---\n\n".join(parts)

    @staticmethod
    def _format_citations(retrieved: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                "chunk_id": c["id"],
                "doc_id": c["doc_id"],
                "doc_title": c["doc_title"],
                "page_number": c["page_number"],
                "section_header": c["section_header"],
                "score": c["score"],
                "excerpt": c["content"][:280] + ("..." if len(c["content"]) > 280 else ""),
                "label": f"[Source: {c['doc_title']}, Page {c['page_number']} / {c['section_header']}]",
            }
            for c in retrieved
        ]

    async def chat(
        self,
        user: Dict[str, Any],
        query: str,
        session_id: Optional[str] = None,
        doc_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Non-streaming grounded multi-tenant RAG chat turn."""
        session = self.db.get_or_create_chat_session(
            user_id=user["id"],
            session_id=session_id,
            title=query[:75],
        )
        history = self.db.get_chat_messages(session["id"], user["id"], limit=12)
        retrieved = await asyncio.to_thread(self.hybrid_retrieve, user["id"], query, doc_ids)
        citations = self._format_citations(retrieved)
        prompt = self._build_generation_prompt(query, history, retrieved)

        self.db.add_chat_message(session["id"], user["id"], role="user", content=query)

        tokens: List[str] = []
        async for tok in self.gemini.generate_grounded_stream(
            system_instruction=SARAL_SYSTEM_PROMPT,
            user_prompt=prompt,
            query=query,
            retrieved_chunks=retrieved,
        ):
            tokens.append(tok)
        answer = "".join(tokens).strip()

        cited_ids = [c["chunk_id"] for c in citations]
        assistant_msg = self.db.add_chat_message(
            session_id=session["id"],
            user_id=user["id"],
            role="assistant",
            content=answer,
            cited_chunk_ids=cited_ids,
            citations=citations,
        )
        log_structured_event(
            logger, "saral_chat_completed", user_id=user["id"],
            session_id=session["id"], cited_chunks=len(cited_ids),
        )
        return {
            "session_id": session["id"],
            "message_id": assistant_msg["id"],
            "answer": answer,
            "citations": citations,
            "cited_chunk_ids": cited_ids,
            "grounded": len(citations) > 0,
            "backend": self.gemini.backend_label,
        }

    async def chat_stream_events(
        self,
        user: Dict[str, Any],
        query: str,
        session_id: Optional[str] = None,
        doc_ids: Optional[List[str]] = None,
    ) -> AsyncIterator[Dict[str, Any]]:
        """Yields structured SSE events (`meta`, `delta`, `done`) for real-time streaming chat."""
        session = self.db.get_or_create_chat_session(
            user_id=user["id"],
            session_id=session_id,
            title=query[:75],
        )
        history = self.db.get_chat_messages(session["id"], user["id"], limit=12)
        retrieved = await asyncio.to_thread(self.hybrid_retrieve, user["id"], query, doc_ids)
        citations = self._format_citations(retrieved)
        prompt = self._build_generation_prompt(query, history, retrieved)

        self.db.add_chat_message(session["id"], user["id"], role="user", content=query)
        yield {
            "type": "meta",
            "session_id": session["id"],
            "citations": citations,
            "grounded": len(citations) > 0,
            "backend": self.gemini.backend_label,
        }

        buf: List[str] = []
        async for tok in self.gemini.generate_grounded_stream(
            system_instruction=SARAL_SYSTEM_PROMPT,
            user_prompt=prompt,
            query=query,
            retrieved_chunks=retrieved,
        ):
            buf.append(tok)
            yield {"type": "delta", "text": tok}

        answer = "".join(buf).strip()
        cited_ids = [c["chunk_id"] for c in citations]
        assistant_msg = self.db.add_chat_message(
            session_id=session["id"],
            user_id=user["id"],
            role="assistant",
            content=answer,
            cited_chunk_ids=cited_ids,
            citations=citations,
        )
        yield {
            "type": "done",
            "session_id": session["id"],
            "message_id": assistant_msg["id"],
            "cited_chunk_ids": cited_ids,
        }
