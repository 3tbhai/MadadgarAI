"""Unit tests for Student Scholarship Matcher & Document Checklist Generator (isolated fixtures)."""
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


def _build_test_matcher(tmp_path) -> StudentScholarshipMatcher:
    norm = DatasetNormalizer(db_path=tmp_path / "stu_test.db")
    norm.save_opportunity(
        FundingOpportunity(
            foa_id="SCHOLARSHIP-UNIT-GIRLS-01",
            title="Technical Engineering Scholarship for Girl Students",
            agency=AgencyType.AICTE,
            source_url="https://example.org/girls-tech",
            direct_apply_url="https://example.org/girls-tech/apply",
            portal_navigation_steps=["1. Open Portal", "2. Register", "3. Submit"],
            raw_document_hash="unit_stu_1",
            brief_summary="Financial support for female engineering students with family income up to 8 Lakhs.",
            thematic_areas=["Scholarship", "Girl Students", "Technical Education"],
            eligibility=EligibilityCriteria(
                target_beneficiaries=[BeneficiaryType.UG_PG_STUDENT],
                raw_eligibility_text="Female student in engineering, annual family income <= Rs. 8 Lakhs.",
            ),
            deadlines=Deadlines(closing_date=date(2027, 11, 30)),
            financials=FinancialCeiling(max_amount_inr=200000.0),
        )
    )
    return StudentScholarshipMatcher(normalizer=norm)


def test_female_student_eligible_and_male_disqualified(tmp_path):
    matcher = _build_test_matcher(tmp_path)

    req_f = StudentProfileRequest(
        state_domicile="Maharashtra",
        education_level=EducationLevel.UG_ENGINEERING,
        social_category=SocialCategory.GENERAL,
        gender="Female",
        family_annual_income_inr=250000.0,
        verified_documents=["income_certificate", "bonafide", "npci_dbt"],
        has_npci_dbt_seeded=True,
    )
    res_f = matcher.match_student(req_f)
    assert len(res_f) == 1
    assert res_f[0].eligibility_status == "ELIGIBLE"
    assert res_f[0].eligibility_confidence == "VERIFIED_ELIGIBLE"

    req_m = StudentProfileRequest(
        state_domicile="Maharashtra",
        education_level=EducationLevel.UG_ENGINEERING,
        social_category=SocialCategory.GENERAL,
        gender="Male",
        family_annual_income_inr=250000.0,
    )
    res_m = matcher.match_student(req_m)
    assert res_m[0].eligibility_status == "INELIGIBLE"


def test_document_checklist_and_hinglish_guide(tmp_path):
    matcher = _build_test_matcher(tmp_path)
    foa = matcher.get_all_student_scholarships()[0]
    docs = matcher.generate_document_checklist(foa)
    assert len(docs) >= 4
    guide = matcher.generate_hinglish_guide(foa)
    assert len(guide.kaun_apply_kar_sakta_hai) > 0
    assert len(guide.zaruri_documents) >= 5
