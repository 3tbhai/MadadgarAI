"""Layout-Aware Semantic / Recursive Document Chunker for PDF, Markdown, Plain Text & Web/arXiv URLs."""
from dataclasses import dataclass
import io
import logging
import re
from typing import List, Tuple
from bs4 import BeautifulSoup
import httpx
from pypdf import PdfReader

from src.crawlers.link_verifier import DEFAULT_HEADERS

logger = logging.getLogger("MadadgaarAI.RAG.Chunker")


@dataclass
class ParsedPage:
    page_number: int
    section_header: str
    text: str


@dataclass
class DocumentChunk:
    page_number: int
    section_header: str
    chunk_index: int
    content: str
    token_count: int


def _estimate_tokens(text: str) -> int:
    # Fast BPE-approximating token estimate (~1.3 tokens per whitespace word)
    words = text.split()
    return max(1, int(len(words) * 1.3))


class LayoutAwareChunker:
    """
    Layout-aware recursive chunker targeting ~800 tokens with ~150-token overlap,
    preserving page_number, section_header, and chunk_index metadata.
    """

    @staticmethod
    def extract_pdf_pages(file_bytes: bytes) -> List[ParsedPage]:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages: List[ParsedPage] = []
        current_header = "Introduction"
        for idx, page in enumerate(reader.pages, start=1):
            raw = (page.extract_text() or "").strip()
            if not raw:
                continue
            # Detect likely heading line at top of page
            for line in raw.splitlines()[:6]:
                clean = " ".join(line.split())
                if 4 <= len(clean) <= 90 and (
                    re.match(r"^(?:\d+(?:\.\d+)*\s+|chapter\s+\d+|section\s+\d+|abstract|introduction|methodology|results|conclusion|references)", clean, re.I)
                    or (clean.isupper() and len(clean.split()) <= 10)
                ):
                    current_header = clean
                    break
            pages.append(ParsedPage(page_number=idx, section_header=current_header, text=raw))
        return pages

    @staticmethod
    def extract_markdown_sections(raw_text: str) -> List[ParsedPage]:
        lines = raw_text.splitlines()
        sections: List[ParsedPage] = []
        current_header = "Overview"
        buf: List[str] = []
        sec_idx = 1

        for line in lines:
            m = re.match(r"^(#{1,4})\s+(.+)$", line.strip())
            if m:
                if buf and "\n".join(buf).strip():
                    sections.append(ParsedPage(page_number=sec_idx, section_header=current_header, text="\n".join(buf).strip()))
                    sec_idx += 1
                    buf = []
                current_header = m.group(2).strip()[:90]
            else:
                buf.append(line)

        if buf and "\n".join(buf).strip():
            sections.append(ParsedPage(page_number=sec_idx, section_header=current_header, text="\n".join(buf).strip()))
        return sections or [ParsedPage(page_number=1, section_header="Overview", text=raw_text.strip())]

    @staticmethod
    async def fetch_url_content(url: str) -> Tuple[str, str, List[ParsedPage]]:
        """Fetches a web URL or arXiv abstract/PDF page and returns (title, mime_type, pages)."""
        clean_url = url.strip()
        if not clean_url.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")

        async with httpx.AsyncClient(verify=False, headers=DEFAULT_HEADERS, timeout=15.0, follow_redirects=True) as hc:
            resp = await hc.get(clean_url)
            resp.raise_for_status()
            ctype = (resp.headers.get("content-type") or "text/html").split(";")[0].strip().lower()

            if "pdf" in ctype or clean_url.lower().endswith(".pdf") or resp.content[:4] == b"%PDF":
                pages = LayoutAwareChunker.extract_pdf_pages(resp.content)
                title = clean_url.rstrip("/").split("/")[-1] or "Remote PDF Document"
                return title, "application/pdf", pages

            soup = BeautifulSoup(resp.text, "html.parser")
            title = " ".join(soup.title.string.split())[:120] if (soup.title and soup.title.string) else clean_url
            for tag in soup(["script", "style", "noscript", "svg", "nav", "footer"]):
                tag.decompose()

            # Preserve heading-delimited sections from HTML (great for arXiv / docs / Wikipedia)
            sections: List[ParsedPage] = []
            current_header = "Overview"
            buf: List[str] = []
            sec_idx = 1
            root = soup.select_one("main, article, #abs, .ltx_document, #content") or soup.body or soup
            for elem in root.find_all(["h1", "h2", "h3", "p", "li", "blockquote"]):
                txt = " ".join(elem.get_text(" ", strip=True).split())
                if len(txt) < 4:
                    continue
                if elem.name in ("h1", "h2", "h3"):
                    if buf:
                        sections.append(ParsedPage(page_number=sec_idx, section_header=current_header, text="\n".join(buf)))
                        sec_idx += 1
                        buf = []
                    current_header = txt[:90]
                else:
                    buf.append(txt)
            if buf:
                sections.append(ParsedPage(page_number=sec_idx, section_header=current_header, text="\n".join(buf)))

            if not sections:
                plain = root.get_text("\n", strip=True)
                sections = [ParsedPage(page_number=1, section_header="Web Excerpt", text=plain)]
            return title, ctype, sections

    def chunk_pages(
        self,
        pages: List[ParsedPage],
        chunk_size_tokens: int = 800,
        chunk_overlap_tokens: int = 150,
    ) -> List[DocumentChunk]:
        """Recursively chunks parsed pages while preserving page numbers, headings, and token overlap."""
        chunks: List[DocumentChunk] = []
        chunk_idx = 0
        max_words = max(80, int(chunk_size_tokens / 1.3))
        overlap_words = max(20, min(max_words // 2, int(chunk_overlap_tokens / 1.3)))

        for page in pages:
            paragraphs = [p.strip() for p in re.split(r"\n{2,}", page.text) if p.strip()]
            if not paragraphs:
                continue

            current_words: List[str] = []
            for para in paragraphs:
                p_words = para.split()
                if len(current_words) + len(p_words) <= max_words:
                    current_words.extend(p_words)
                    continue

                if current_words:
                    content = " ".join(current_words).strip()
                    if len(content) >= 20:
                        chunks.append(
                            DocumentChunk(
                                page_number=page.page_number,
                                section_header=page.section_header,
                                chunk_index=chunk_idx,
                                content=content,
                                token_count=_estimate_tokens(content),
                            )
                        )
                        chunk_idx += 1
                    current_words = current_words[-overlap_words:] if overlap_words else []

                # Handle extra-long single paragraphs recursively by word windows
                if len(p_words) > max_words:
                    step = max(1, max_words - overlap_words)
                    for start in range(0, len(p_words), step):
                        window = p_words[start : start + max_words]
                        content = " ".join(window).strip()
                        if len(content) >= 20:
                            chunks.append(
                                DocumentChunk(
                                    page_number=page.page_number,
                                    section_header=page.section_header,
                                    chunk_index=chunk_idx,
                                    content=content,
                                    token_count=_estimate_tokens(content),
                                )
                            )
                            chunk_idx += 1
                    current_words = []
                else:
                    current_words.extend(p_words)

            if current_words:
                content = " ".join(current_words).strip()
                if len(content) >= 15:
                    chunks.append(
                        DocumentChunk(
                            page_number=page.page_number,
                            section_header=page.section_header,
                            chunk_index=chunk_idx,
                            content=content,
                            token_count=_estimate_tokens(content),
                        )
                    )
                    chunk_idx += 1

        return chunks
