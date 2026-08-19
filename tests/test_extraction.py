"""Tests for Entity Recognition and Pattern Normalization."""
from datetime import date
from src.extractor.entity_extractor import FOAEntityExtractor
from src.schemas.foa import AgencyType, BeneficiaryType


def test_financial_extraction():
    extractor = FOAEntityExtractor()

    # Lakhs
    fin1 = extractor.extract_financials("Maximum financial assistance up to Rs. 60 Lakhs for 3 years with 10% overheads.")
    assert fin1.max_amount_inr == 6000000.0
    assert fin1.institutional_overhead_pct == 10.0

    # Crores
    fin2 = extractor.extract_financials("Budget ceiling is ₹ 1.5 Crore.")
    assert fin2.max_amount_inr == 15000000.0

    # Monthly Stipend
    fin3 = extractor.extract_financials("JRF fellowship of Rs. 37,000 per month.")
    assert fin3.stipend_monthly_inr == 37000.0


def test_deadline_extraction():
    extractor = FOAEntityExtractor()

    # DD-MM-YYYY format
    d1 = extractor.extract_dates("Opening date: 01-07-2026, Closing date: 30-09-2026, Extended: 15-10-2026.")
    assert d1.open_date == date(2026, 7, 1)
    assert d1.closing_date == date(2026, 9, 30)
    assert d1.extended_closing_date == date(2026, 10, 15)

    # Rolling call
    d2 = extractor.extract_dates("This is a rolling call open round the year.")
    assert d2.is_rolling is True


def test_eligibility_extraction():
    extractor = FOAEntityExtractor()
    sample = "Open to women scientists with Ph.D. in Engineering. Maximum age limit is 55 years in CFTIs and state universities."
    elig = extractor.extract_eligibility(sample)

    assert elig.max_age_limit == 55
    assert BeneficiaryType.WOMEN_SCIENTIST in elig.target_beneficiaries
    assert "Ph.D." in elig.min_qualification
