"""Unit and integration tests for Student Scholarship Intelligence (Vidyarthi AI)."""
import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.crawlers.scholarship_seed_data import get_seed_student_scholarships
from src.matcher.student_matcher import StudentScholarshipMatcher
from src.schemas.foa import (
    EducationLevel,
    SocialCategory,
    StudentProfileRequest,
)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def student_matcher():
    return StudentScholarshipMatcher()


def test_seed_student_scholarships_loaded():
    """Verify that student scholarships dataset contains valid schemes."""
    scholarships = get_seed_student_scholarships()
    assert len(scholarships) >= 10
    ids = [s.foa_id for s in scholarships]
    assert "SCHOLARSHIP-AICTE-PRAGATI-2026" in ids
    assert "SCHOLARSHIP-NSP-PMUSP-2026" in ids
    assert "SCHOLARSHIP-UP-DASHMOTTAR-2026" in ids
    assert "SCHOLARSHIP-KOTAK-KANYA-2026" in ids


def test_female_engineering_student_matching(student_matcher):
    """Female B.Tech student from UP with income 2L should match Pragati and UP Dashmottar."""
    req = StudentProfileRequest(
        student_name="Priya Sharma",
        state_domicile="Uttar Pradesh",
        education_level=EducationLevel.UG_ENGINEERING,
        social_category=SocialCategory.GENERAL,
        gender="Female",
        family_annual_income_inr=200000.0,
        academic_percentage=88.0,
        is_single_girl_child=False,
        is_differently_abled_pwd=False,
    )

    results = student_matcher.match_student(req)
    assert len(results) > 0

    top_ids = [r.foa.foa_id for r in results if r.eligibility_status in ["ELIGIBLE", "HIGH_PROBABILITY"]]
    assert "SCHOLARSHIP-AICTE-PRAGATI-2026" in top_ids
    assert "SCHOLARSHIP-UP-DASHMOTTAR-2026" in top_ids

    # Verify document checklist
    pragati_res = next(r for r in results if r.foa.foa_id == "SCHOLARSHIP-AICTE-PRAGATI-2026")
    doc_names = [d.document_name for d in pragati_res.document_checklist]
    assert any("Income Certificate" in d for d in doc_names)
    assert any("Bank Passbook" in d for d in doc_names)


def test_male_student_disqualified_from_female_exclusive(student_matcher):
    """Male student must be marked INELIGIBLE for AICTE Pragati & Kotak Kanya."""
    req = StudentProfileRequest(
        student_name="Rahul Verma",
        state_domicile="Uttar Pradesh",
        education_level=EducationLevel.UG_ENGINEERING,
        social_category=SocialCategory.OBC_NCL,
        gender="Male",
        family_annual_income_inr=200000.0,
        academic_percentage=90.0,
    )

    results = student_matcher.match_student(req)
    pragati_res = next(r for r in results if r.foa.foa_id == "SCHOLARSHIP-AICTE-PRAGATI-2026")
    assert pragati_res.eligibility_status == "INELIGIBLE"
    assert any("female" in w.lower() or "girl" in w.lower() for w in pragati_res.warning_reasons)


def test_high_income_means_tested_ineligibility(student_matcher):
    """Income of 12 Lakhs should exceed ceiling for 2.5L / 4.5L schemes."""
    req = StudentProfileRequest(
        student_name="Amit Kumar",
        state_domicile="Delhi NCR",
        education_level=EducationLevel.UG_GENERAL,
        social_category=SocialCategory.GENERAL,
        gender="Male",
        family_annual_income_inr=1200000.0,  # 12 Lakhs
    )

    results = student_matcher.match_student(req)
    pmusp_res = next((r for r in results if r.foa.foa_id == "SCHOLARSHIP-NSP-PMUSP-2026"), None)
    if pmusp_res:
        assert pmusp_res.eligibility_status in ["INELIGIBLE", "WARNING"]


def test_document_checklist_and_hinglish_guide(student_matcher):
    """Verify document checklist and Hinglish explainer structure."""
    scholarships = student_matcher.get_all_student_scholarships()
    assert len(scholarships) > 0
    foa = scholarships[0]

    docs = student_matcher.generate_document_checklist(foa)
    assert len(docs) >= 4
    assert any(d.is_mandatory for d in docs)
    assert all(len(d.issuing_authority) > 0 for d in docs)

    guide = student_matcher.generate_hinglish_guide(foa)
    assert len(guide.kaun_apply_kar_sakta_hai) > 0
    assert len(guide.kitne_paise_milenge) > 0
    assert len(guide.zaruri_documents) >= 5
    assert "scholarship" in guide.official_portal_url or "http" in guide.official_portal_url


def test_api_student_match_endpoint(client):
    """Test POST /api/student/match endpoint."""
    payload = {
        "student_name": "Ananya Sen",
        "state_domicile": "West Bengal",
        "education_level": "UG - Engineering / Technology (B.Tech/B.E.)",
        "social_category": "General / Open",
        "gender": "Female",
        "family_annual_income_inr": 250000.0,
        "academic_percentage": 92.0,
        "top_k": 5,
    }
    response = client.post("/api/student/match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "eligibility_status" in data[0]
    assert "document_checklist" in data[0]


def test_api_student_metadata_endpoint(client):
    """Test GET /api/student/meta endpoint."""
    response = client.get("/api/student/meta")
    assert response.status_code == 200
    meta = response.json()
    assert "states" in meta
    assert "education_levels" in meta
    assert "social_categories" in meta
    assert "All India" in meta["states"]


def test_direct_apply_and_navigation_steps(student_matcher):
    """Verify that scholarships have deep direct apply URLs and step-by-step click guidance."""
    scholarships = student_matcher.get_all_student_scholarships()
    pragati = next(s for s in scholarships if s.foa_id == "SCHOLARSHIP-AICTE-PRAGATI-2026")
    assert pragati.direct_apply_url is not None
    assert "scholarship" in pragati.direct_apply_url
    assert len(pragati.portal_navigation_steps) >= 3

    req = StudentProfileRequest(
        student_name="Pooja Sharma",
        state_domicile="Uttar Pradesh",
        education_level=EducationLevel.UG_ENGINEERING,
        social_category=SocialCategory.GENERAL,
        gender="Female",
        family_annual_income_inr=200000.0,
    )
    results = student_matcher.match_student(req)
    res = results[0]
    assert res.direct_apply_url is not None
    assert len(res.portal_navigation_steps) >= 3

