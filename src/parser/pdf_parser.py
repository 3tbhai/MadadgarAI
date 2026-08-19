"""Multimodal Layout and PDF Parser with OCR Fallback."""
import io
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

import pypdf
from PIL import Image

from src.parser.ocr_worker import OCRWorker, evaluate_text_density, is_scanned_document

logger = logging.getLogger("MadadgaarAI.Parser.PDF")


@dataclass
class ParsedDocument:
    raw_text: str
    num_pages: int
    sections: Dict[str, str] = field(default_factory=dict)
    tables: List[List[List[str]]] = field(default_factory=list)
    character_density: float = 0.0
    is_ocr_fallback: bool = False
    metadata: Dict[str, str] = field(default_factory=dict)


class PDFLayoutParser:
    def __init__(self):
        self.ocr_worker = OCRWorker()
        self.section_headers = [
            ("objectives", re.compile(r"(?:1\.?\s*)?(?:objectives?|scope|background|aim|overview)", re.I)),
            ("eligibility", re.compile(r"(?:2\.?\s*)?(?:eligibility|who can apply|target beneficiaries|criteria)", re.I)),
            ("financials", re.compile(r"(?:3\.?\s*)?(?:financial\s*(?:assistance|support|ceiling|grants?)|budget|fellowship)", re.I)),
            ("deadlines", re.compile(r"(?:4\.?\s*)?(?:important dates?|deadlines?|closing date|submission deadline)", re.I)),
            ("guidelines", re.compile(r"(?:5\.?\s*)?(?:how to apply|general guidelines|instructions|submission procedure)", re.I)),
        ]

    def parse_pdf(self, pdf_input: Union[str, Path, bytes]) -> ParsedDocument:
        """Parses PDF bytes or file path into structured sections and reading-order text."""
        if isinstance(pdf_input, (str, Path)):
            with open(pdf_input, "rb") as f:
                pdf_bytes = f.read()
        else:
            pdf_bytes = pdf_input

        reader = None
        extracted_text_pages: List[str] = []
        num_pages = 0
        metadata: Dict[str, str] = {}

        try:
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            num_pages = len(reader.pages)
            if reader.metadata:
                metadata = {str(k): str(v) for k, v in reader.metadata.items()}

            for page_idx, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                extracted_text_pages.append(page_text.strip())
        except Exception as e:
            logger.error(f"pypdf extraction encountered an issue: {e}")

        combined_text = "\n\n".join(p for p in extracted_text_pages if p)
        density = evaluate_text_density(combined_text, num_pages)
        is_scanned = is_scanned_document(combined_text, num_pages)

        # Fallback to OCR if scanned / non-searchable
        if is_scanned or num_pages == 0:
            logger.info(f"Document has low text density ({density:.1f} chars/pg). Routing to OCR fallback.")
            ocr_text = self._extract_ocr_from_pdf(reader, pdf_bytes)
            if ocr_text.strip():
                combined_text = ocr_text
                is_scanned = True

        sections = self._segment_sections(combined_text)

        return ParsedDocument(
            raw_text=combined_text,
            num_pages=num_pages,
            sections=sections,
            character_density=density,
            is_ocr_fallback=is_scanned,
            metadata=metadata,
        )

    def _extract_ocr_from_pdf(self, reader: Optional[pypdf.PdfReader], pdf_bytes: bytes) -> str:
        """Extracts images from PDF pages and routes them to OCR worker."""
        images: List[Image.Image] = []
        if reader:
            for page in reader.pages:
                for img_obj in page.images:
                    try:
                        img = Image.open(io.BytesIO(img_obj.data))
                        images.append(img)
                    except Exception as e:
                        logger.debug(f"Could not load embedded image: {e}")
        if images:
            return self.ocr_worker.extract_text_from_images(images)
        return ""

    def _segment_sections(self, text: str) -> Dict[str, str]:
        """Segments raw text into recognized logical sections using regex boundaries."""
        sections: Dict[str, str] = {}
        lines = text.splitlines()
        current_section = "general"
        section_buffer: List[str] = []

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue

            matched_sec = None
            for sec_name, pattern in self.section_headers:
                if len(trimmed) < 80 and pattern.search(trimmed):
                    matched_sec = sec_name
                    break

            if matched_sec:
                if section_buffer:
                    sections[current_section] = "\n".join(section_buffer).strip()
                current_section = matched_sec
                section_buffer = [trimmed]
            else:
                section_buffer.append(line)

        if section_buffer:
            sections[current_section] = "\n".join(section_buffer).strip()

        return sections
