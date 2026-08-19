"""Tests for Layout Parser, Density Evaluator, and OCR Fallback."""
from src.parser.ocr_worker import evaluate_text_density, is_scanned_document
from src.parser.pdf_parser import PDFLayoutParser


def test_text_density_evaluation():
    high_density_text = "A " * 400  # 400 chars on 1 page
    low_density_text = "Hi"  # 2 chars on 1 page

    assert evaluate_text_density(high_density_text, 1) > 100
    assert evaluate_text_density(low_density_text, 1) < 10

    assert not is_scanned_document(high_density_text, 1)
    assert is_scanned_document(low_density_text, 1)


def test_section_segmentation():
    parser = PDFLayoutParser()
    sample_text = (
        "1. Objectives\nTo promote advanced research in clean energy.\n\n"
        "2. Eligibility\nOpen to regular faculty holding Ph.D.\n\n"
        "3. Financial Support\nGrant of Rs. 40 Lakhs.\n\n"
        "4. Important Dates\nClosing Date: 30-09-2026."
    )
    sections = parser._segment_sections(sample_text)
    assert "objectives" in sections
    assert "eligibility" in sections
    assert "financials" in sections
    assert "deadlines" in sections
