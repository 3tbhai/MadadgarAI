"""OCR Fallback Worker and Document Density Evaluator."""
import io
import logging
import shutil
from typing import List, Optional
from PIL import Image
import pytesseract

from src.config import MIN_TEXT_DENSITY_CHARS_PER_PAGE, MAX_OCR_PAGES

logger = logging.getLogger("MadadgaarAI.Parser.OCR")


def evaluate_text_density(text: str, num_pages: int) -> float:
    """Calculates average characters extracted per page."""
    if num_pages <= 0:
        return 0.0
    clean_chars = len("".join(text.split()))
    return clean_chars / float(num_pages)


def is_scanned_document(text: str, num_pages: int) -> bool:
    """Determines whether a document is scanned or non-searchable raster PDF."""
    if num_pages <= 0:
        return True
    density = evaluate_text_density(text, num_pages)
    return density < MIN_TEXT_DENSITY_CHARS_PER_PAGE


class OCRWorker:
    def __init__(self):
        self.tesseract_available = shutil.which("tesseract") is not None
        if not self.tesseract_available:
            logger.warning(
                "Tesseract OCR binary not found in system PATH. Resilient fallback mode enabled."
            )

    def extract_text_from_images(self, images: List[Image.Image]) -> str:
        """Runs OCR across extracted image pages."""
        extracted_pages = []
        for idx, img in enumerate(images[:MAX_OCR_PAGES], start=1):
            try:
                if self.tesseract_available:
                    page_text = pytesseract.image_to_string(img, lang="eng+hin")
                else:
                    page_text = f"[OCR Raster Page {idx}: Tesseract binary unavailable on host. Pre-extracted metadata preserved.]"
                if page_text and page_text.strip():
                    extracted_pages.append(f"--- Page {idx} ---\n" + page_text.strip())
            except Exception as e:
                logger.error(f"OCR failed for page {idx}: {e}")
                extracted_pages.append(f"[OCR extraction failed for page {idx}]")
                
        return "\n\n".join(extracted_pages)

    def process_image_bytes(self, image_bytes: bytes) -> str:
        """Processes raw image bytes through OCR."""
        try:
            img = Image.open(io.BytesIO(image_bytes))
            return self.extract_text_from_images([img])
        except Exception as e:
            logger.error(f"Failed to decode image bytes for OCR: {e}")
            return ""
