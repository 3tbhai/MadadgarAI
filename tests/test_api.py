"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_check():
    with TestClient(app) as c:
        resp = c.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"


def test_list_foas():
    with TestClient(app) as c:
        resp = c.get("/api/foas")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 6


def test_search_api():
    with TestClient(app) as c:
        resp = c.post(
            "/api/search",
            json={"query": "quantum materials AI grant", "top_k": 3},
        )
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) > 0
        assert "foa" in results[0]
        assert "relevance_score" in results[0]


def test_match_profile_api():
    with TestClient(app) as c:
        resp = c.post(
            "/api/match-profile",
            json={
                "research_summary": "Biomedical diagnostic microfluidic devices for affordable diagnostics",
                "user_role": "Faculty / Principal Investigator",
                "applicant_age": 40,
                "highest_degree": "Ph.D.",
                "top_k": 3,
            },
        )
        assert resp.status_code == 200
        matches = resp.json()
        assert len(matches) > 0
        assert "compliance" in matches[0]


def test_calendar_export_api():
    with TestClient(app) as c:
        resp = c.get("/api/foas/DST-CRG-2026-01/calendar")
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/calendar")
        assert b"BEGIN:VCALENDAR" in resp.content


def test_draft_proposal_api():
    with TestClient(app) as c:
        resp = c.post(
            "/api/foas/DST-CRG-2026-01/draft-proposal",
            json={
                "pi_name": "Dr. Anjisht",
                "institution_name": "JK Lakshmipat University",
            },
        )
        assert resp.status_code == 200
        skeleton = resp.json()
        assert skeleton["foa_id"] == "DST-CRG-2026-01"
        assert len(skeleton["sections"]) > 0
