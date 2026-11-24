"""Official Google Gemini API Client Wrapper (google-genai SDK) with Exponential Backoff & Offline Grounded Fallback."""
import asyncio
import logging
import os
import re
import time
from typing import Any, AsyncIterator, Dict, List, Optional

from google import genai
from google.genai import types

from src.embeddings.embedder import TextEmbedder

logger = logging.getLogger("MadadgaarAI.RAG.Gemini")

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"


def _is_retryable_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(code in msg for code in ("429", "503", "resource_exhausted", "unavailable", "rate limit", "temporarily"))


class GeminiRAGClient:
    """
    Wraps the official google-genai SDK (`from google import genai`) for:
    - Embeddings via `client.models.embed_content` (`RETRIEVAL_DOCUMENT` / `RETRIEVAL_QUERY`)
    - Streaming grounded generation via `client.models.generate_content_stream`
    - Automatic exponential backoff retries on HTTP 429 / 503
    - Seamless deterministic offline fallback when GEMINI_API_KEY is unset
    """

    def __init__(self, fallback_embedder: Optional[TextEmbedder] = None):
        self.fallback_embedder = fallback_embedder or TextEmbedder()
        self._client: Optional[genai.Client] = None
        self._cached_api_key: str = ""

    @property
    def api_key(self) -> str:
        return (os.getenv("GEMINI_API_KEY") or "").strip()

    @property
    def generation_model(self) -> str:
        return (os.getenv("SARAL_GEMINI_MODEL") or os.getenv("MADADGAAR_GEMINI_MODEL") or DEFAULT_GEMINI_MODEL).strip()

    @property
    def embedding_model(self) -> str:
        return (os.getenv("SARAL_GEMINI_EMBEDDING_MODEL") or DEFAULT_EMBEDDING_MODEL).strip()

    @property
    def is_live_gemini_enabled(self) -> bool:
        return bool(self.api_key)

    @property
    def backend_label(self) -> str:
        if self.is_live_gemini_enabled:
            return f"google-genai ({self.generation_model} + {self.embedding_model})"
        return "Grounded Offline RAG (set GEMINI_API_KEY for Gemini API)"

    def _get_client(self) -> Optional[genai.Client]:
        key = self.api_key
        if not key:
            return None
        if self._client is None or self._cached_api_key != key:
            self._client = genai.Client(api_key=key)
            self._cached_api_key = key
        return self._client

    def embed_texts(self, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
        """Generates dense embeddings via google-genai with exponential backoff, falling back cleanly offline."""
        if not texts:
            return []
        client = self._get_client()
        if client is None:
            return self.fallback_embedder.embed_batch(texts)

        vectors: List[List[float]] = []
        batch_size = 32
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            last_err: Optional[Exception] = None
            for attempt in range(4):
                try:
                    resp = client.models.embed_content(
                        model=self.embedding_model,
                        contents=batch,
                        config=types.EmbedContentConfig(task_type=task_type),
                    )
                    embs = resp.embeddings or []
                    if len(embs) != len(batch):
                        raise ValueError("Unexpected embedding count from Gemini API.")
                    for e in embs:
                        vectors.append(list(e.values))
                    last_err = None
                    break
                except Exception as exc:
                    last_err = exc
                    if attempt < 3 and _is_retryable_error(exc):
                        delay = 1.0 * (2 ** attempt)
                        logger.warning(f"Gemini embed retry {attempt + 1} after {delay}s: {exc}")
                        time.sleep(delay)
                    else:
                        break
            if last_err is not None:
                logger.warning(f"Gemini embed fallback activated: {last_err}")
                vectors.extend(self.fallback_embedder.embed_batch(batch))
        return vectors

    def _build_offline_grounded_answer(
        self,
        query: str,
        mode_name: str,
        retrieved_chunks: List[Dict[str, Any]],
    ) -> str:
        """Deterministic strict-grounding synthesis when GEMINI_API_KEY is not configured."""
        if not retrieved_chunks:
            return (
                "Your uploaded private documents do not contain enough information to answer this question. "
                "Please upload a relevant PDF, Markdown, text file, or arXiv/web URL into your Knowledge Base and try again."
            )

        top = retrieved_chunks[0]
        header_note = {
            "student": "### Step-by-Step Study Breakdown (Student Mode)",
            "researcher": "### Technical Evidence Synthesis (Researcher Mode)",
            "educator": "### Structured Teaching Notes (Educator Mode)",
        }.get(mode_name, "### Grounded Answer")

        lines = [header_note, ""]
        for idx, ch in enumerate(retrieved_chunks[:3], start=1):
            cite = f"[Source: {ch['doc_title']}, Page {ch['page_number']} / {ch['section_header']}]"
            sentences = [
                s.strip()
                for s in re.split(r"(?<=[.!?])\s+", ch["content"].strip())
                if len(s.strip()) > 20
            ]
            snippet = " ".join(sentences[:3]) if sentences else ch["content"][:320]
            prefix = f"**Step {idx} — {ch['section_header']}:**" if mode_name == "student" else f"**Finding {idx} ({ch['section_header']}):**"
            lines.append(f"{prefix} {snippet} {cite}")
            lines.append("")

        if mode_name == "student":
            lines.append(
                f"**Key Exam / Study Takeaway:** Review `{top['section_header']}` in *{top['doc_title']}* "
                f"(Page {top['page_number']}) and verify formulas/definitions against the cited source chunks."
            )
        elif mode_name == "educator":
            lines.append(
                f"**Quick Check Question:** Based on *{top['doc_title']}* (Page {top['page_number']}), "
                f"how would you explain `{top['section_header']}` in your own words?"
            )
        return "\n".join(lines).strip()

    async def generate_grounded_stream(
        self,
        system_instruction: str,
        user_prompt: str,
        query: str,
        mode_name: str,
        retrieved_chunks: List[Dict[str, Any]],
    ) -> AsyncIterator[str]:
        """Streams grounded tokens using google-genai generate_content_stream with retry & safe fallback."""
        if not retrieved_chunks:
            msg = (
                "Your uploaded documents do not contain enough information to answer this question accurately. "
                "Upload relevant study notes, papers, or URLs to your Private Knowledge Base so Saral AI can answer with inline citations."
            )
            yield msg
            return

        client = self._get_client()
        if client is not None:
            for attempt in range(3):
                try:
                    stream = client.models.generate_content_stream(
                        model=self.generation_model,
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.2,
                            max_output_tokens=1200,
                        ),
                    )
                    emitted_any = False
                    for chunk in stream:
                        text = getattr(chunk, "text", None)
                        if text:
                            emitted_any = True
                            yield text
                            await asyncio.sleep(0)
                    if emitted_any:
                        return
                except Exception as exc:
                    if attempt < 2 and _is_retryable_error(exc):
                        delay = 1.0 * (2 ** attempt)
                        logger.warning(f"Gemini stream retry {attempt + 1} after {delay}s: {exc}")
                        await asyncio.sleep(delay)
                    else:
                        logger.warning(f"Gemini stream fallback activated: {exc}")
                        break

        # Deterministic streaming fallback when GEMINI_API_KEY is unset or unavailable
        fallback_text = self._build_offline_grounded_answer(
            query=query,
            mode_name=mode_name,
            retrieved_chunks=retrieved_chunks,
        )
        words = fallback_text.split(" ")
        chunk_sz = 10
        for i in range(0, len(words), chunk_sz):
            piece = " ".join(words[i : i + chunk_sz])
            if i + chunk_sz < len(words):
                piece += " "
            yield piece
            await asyncio.sleep(0.01)
