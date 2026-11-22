"""Integration tests for RAG Chat, Session Isolation, Document Assistant, and Multi-ICS Calendar."""
import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_saral_samjhauti_rag_bilingual_and_citations(client):
    resp_hi = client.post(
        "/api/ai/chat",
        json={
            "query": "Aadhaar-NPCI DBT bank seeding kaise karwayein aur paisa kaise aata hai?",
            "language": "auto",
            "consent_to_remember": True,
        },
    )
    assert resp_hi.status_code == 200
    data_hi = resp_hi.json()
    assert data_hi["language_used"] == "hinglish"
    assert len(data_hi["citations"]) > 0

    resp_en = client.post(
        "/api/ai/chat",
        json={
            "query": "I am a female B.Tech student from Uttar Pradesh with 1.8 lakh family income. What are the validity rules for Income Certificate?",
            "session_id": data_hi["session_id"],
            "language": "en",
            "consent_to_remember": True,
        },
    )
    assert resp_en.status_code == 200
    data_en = resp_en.json()
    assert data_en["language_used"] == "en"
    assert data_en["remembered_profile_updates"].get("state_domicile") == "Uttar Pradesh"
    assert data_en["remembered_profile_updates"].get("gender") == "Female"


def test_session_isolation_and_checklist_progress(client):
    sess_a = "test-session-alpha-001"
    sess_b = "test-session-beta-002"

    client.post(
        f"/api/session/{sess_a}/profile",
        json={"consent_given": True, "student_profile": {"student_name": "SecretUserA"}},
    )
    resp_b = client.get(f"/api/session/{sess_b}")
    assert resp_b.status_code == 200
    assert resp_b.json()["student_profile"].get("student_name") is None

    resp_chk = client.post(
        f"/api/session/{sess_a}/checklist",
        json={"foa_id": "LIVE-OPP-01", "step_key": "step_0", "completed": True},
    )
    assert resp_chk.status_code == 200
    assert "step_0" in resp_chk.json()["checklist_progress"]["LIVE-OPP-01"]

    client.delete(f"/api/session/{sess_a}")
    client.delete(f"/api/session/{sess_b}")


def test_intelligent_document_assistant_analysis_and_disclaimer(client):
    sample_income_text = (
        "OFFICE OF THE TEHSILDAR, JAIPUR\n"
        "INCOME CERTIFICATE\n"
        "Certificate No: RAJ-2026-99102\n"
        "Date: 10-06-2026\n"
        "Certified that annual family income from all sources is Rs. 1,60,000 per annum."
    )
    resp = client.post(
        "/api/documents/analyze",
        json={"raw_text": sample_income_text, "document_type_hint": "INCOME_CERTIFICATE"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["document_type"] == "INCOME_CERTIFICATE"
    assert data["suggested_profile_updates"].get("family_annual_income_inr") == 160000.0
    assert "does NOT certify legal validity" in data["authenticity_disclaimer"]

    files = {"file": ("marksheet.txt", b"CBSE Class 12 Marksheet 2026\nAggregate Percentage: 92.50%\nPASS", "text/plain")}
    resp_up = client.post("/api/documents/upload", files=files, data={"document_type_hint": "ACADEMIC_MARKSHEET"})
    assert resp_up.status_code == 200
    assert resp_up.json()["suggested_profile_updates"].get("academic_percentage") == 92.5


def test_upcoming_deadlines_and_multi_ics_calendar(client):
    resp_dl = client.get("/api/deadlines/upcoming")
    assert resp_dl.status_code == 200
    assert len(resp_dl.json()) > 0

    resp_ics = client.get("/api/calendar/upcoming.ics")
    assert resp_ics.status_code == 200
    assert b"BEGIN:VCALENDAR" in resp_ics.content
    assert b"Asia/Kolkata" in resp_ics.content
