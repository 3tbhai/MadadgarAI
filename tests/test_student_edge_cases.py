"""Edge-case Unit Tests for Student Scholarship Matching Engine."""
import pytest
from datetime import date
from src.extractor.normalizer import DatasetNormalizer
from src.matcher.student_matcher import StudentScholarshipMatcher
from src.schemas.foa import (
    AgencyType,
    BeneficiaryType,
    Deadlines,
    EducationLevel,
    EligibilityCriteria,
    FinancialCeiling,
    FundingOpportunity,
    SocialCategory,
    StudentProfileRequest,
)

def _build_mock_matcher(tmp_path) -> StudentScholarshipMatcher:
    norm = DatasetNormalizer(db_path=tmp_path / "edge_test.db")
    norm.save_opportunity(
        FundingOpportunity(
            foa_id="SCHOLARSHIP-EDGE-SC-01",
            title="Post-Matric Scholarship for SC Students",
            agency=AgencyType.NSP,
            source_url="https://scholarships.gov.in/sc",
            direct_apply_url="https://scholarships.gov.in/apply",
            portal_navigation_steps=["1. Open NSP", "2. Select Ministry of Social Justice", "3. Apply"],
            raw_document_hash="edge_hash_sc_01",
            brief_summary="Scholarship support for SC students with family income under 2.5 Lakhs.",
            thematic_areas=["Scholarship", "Scheduled Caste", "Post-Matric"],
            eligibility=EligibilityCriteria(
                target_beneficiaries=[BeneficiaryType.UG_PG_STUDENT],
                target_social_categories=[SocialCategory.SC],
                max_family_income_inr=250000.0,
                raw_eligibility_text="SC students with family income <= Rs. 2,50,000.",
            ),
            deadlines=Deadlines(closing_date=date(2027, 12, 31)),
            financials=FinancialCeiling(max_amount_inr=150000.0),
        )
    )
    return StudentScholarshipMatcher(normalizer=norm)

def test_zero_family_income_is_eligible(tmp_path):
    matcher = _build_mock_matcher(tmp_path)
    req = StudentProfileRequest(
        state_domicile="Uttar Pradesh",
        education_level=EducationLevel.UG_ENGINEERING,
        social_category=SocialCategory.SC,
        gender="Male",
        family_annual_income_inr=0.0,
        has_npci_dbt_seeded=True,
    )
    results = matcher.match_student(req)
    assert len(results) == 1
    assert results[0].eligibility_status in ["ELIGIBLE", "HIGH_PROBABILITY"]

def test_income_exceeding_ceiling_is_ineligible(tmp_path):
    matcher = _build_mock_matcher(tmp_path)
    req = StudentProfileRequest(
        state_domicile="Uttar Pradesh",
        education_level=EducationLevel.UG_ENGINEERING,
        social_category=SocialCategory.SC,
        gender="Male",
        family_annual_income_inr=500000.0,  # Exceeds 2.5 Lakh limit
    )
    results = matcher.match_student(req)
    assert len(results) == 1
    assert results[0].eligibility_status == "INELIGIBLE"

def test_category_mismatch_is_ineligible(tmp_path):
    matcher = _build_mock_matcher(tmp_path)
    req = StudentProfileRequest(
        state_domicile="Uttar Pradesh",
        education_level=EducationLevel.UG_ENGINEERING,
        social_category=SocialCategory.GENERAL,  # Scheme requires SC
        gender="Male",
        family_annual_income_inr=100000.0,
    )
    results = matcher.match_student(req)
    assert len(results) == 1
    assert results[0].eligibility_status == "INELIGIBLE"
