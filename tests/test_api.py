"""Tests for FastAPI endpoints backed by live curated opportunities."""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["zero_mock_data"] is True


def test_list_foas(client):
    resp = client.get("/api/foas")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0


def test_search_api(client):
    resp = client.post(
        "/api/search",
        json={"query": "research science engineering internship", "top_k": 3},
    )
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) > 0
    assert "foa" in results[0]
    assert "relevance_score" in results[0]


def test_match_profile_api(client):
    resp = client.post(
        "/api/match-profile",
        json={
            "research_summary": "Biomedical diagnostic devices and machine learning research",
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


def test_calendar_export_api(client):
    foas = client.get("/api/foas").json()
    assert len(foas) > 0
    foa_id = foas[0]["foa_id"]
    resp = client.get(f"/api/foas/{foa_id}/calendar")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/calendar")
    assert b"BEGIN:VCALENDAR" in resp.content


def test_draft_proposal_api(client):
    foas = client.get("/api/foas").json()
    assert len(foas) > 0
    foa_id = foas[0]["foa_id"]
    resp = client.post(
        f"/api/foas/{foa_id}/draft-proposal",
        json={
            "pi_name": "Dr. Anjisht",
            "institution_name": "JK Lakshmipat University",
        },
    )
    assert resp.status_code == 200
    skeleton = resp.json()
    assert skeleton["foa_id"] == foa_id
    assert len(skeleton["sections"]) > 0
