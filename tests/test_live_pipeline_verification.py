"""Comprehensive End-to-End Automated Verification Suite for MadadgaarAI v3.0 (Zero Mock Data)."""
import asyncio
from datetime import date
from pathlib import Path
import re
import httpx
import pytest
from fastapi.testclient import TestClient

from src.api.main import app, live_store
from src.crawlers.link_verifier import is_specific_listing_url
from src.dashboard.web_ui import render_dashboard_html
from src.schemas.opportunity import LiveOpportunity, OpportunityCategory


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_1_zero_hardcoded_mock_opportunity_data():
    """Requirement 1: Verify zero hardcoded seed files or mock opportunity arrays remain in src/."""
    project_root = Path(__file__).resolve().parent.parent
    assert not (project_root / "src" / "crawlers" / "seed_data.py").exists(), "seed_data.py must be deleted"
    assert not (project_root / "src" / "crawlers" / "scholarship_seed_data.py").exists(), "scholarship_seed_data.py must be deleted"

    forbidden_markers = [
        "get_seed_foa_dataset",
        "get_seed_student_scholarships",
        "DST-CRG-2026-01",
        "SCHOLARSHIP-AICTE-PRAGATI-2026",
        "SCHOLARSHIP-KOTAK-KANYA-2026",
    ]
    for py_file in (project_root / "src").rglob("*.py"):
        content = py_file.read_text(encoding="utf-8", errors="ignore")
        for marker in forbidden_markers:
            assert marker not in content, f"Hardcoded marker '{marker}' still found in {py_file}"


def test_2_live_scrape_strict_schema_and_no_expired(client):
    """Requirement 2: Verify live opportunities conform to LiveOpportunity schema and none are expired."""
    resp = client.get("/api/opportunities?limit=100")
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_in_store"] >= 15, f"Expected live opportunities in store, got {data['total_in_store']}"
    assert len(data["items"]) >= 15

    today = date.today()
    categories_seen = set()
    for raw_item in data["items"]:
        opp = LiveOpportunity.model_validate(raw_item)
        categories_seen.add(opp.category)
        assert opp.http_status >= 200 and opp.http_status <= 399
        assert is_specific_listing_url(str(opp.source_url))
        if opp.deadline is not None:
            assert opp.deadline >= today, f"Expired opportunity leaked: {opp.title} ({opp.deadline})"

    assert OpportunityCategory.INTERNSHIP in categories_seen
    assert OpportunityCategory.FUNDING in categories_seen
    assert OpportunityCategory.SCHOLARSHIP in categories_seen


def test_3_sampled_live_urls_return_valid_http_status(client):
    """Requirement 3: Independently probe sampled source_urls from live API to confirm zero 404s."""
    resp = client.get("/api/opportunities?limit=100")
    items = resp.json()["items"]
    # Sample up to 6 distinct domains/listings across categories
    sampled = []
    seen_domains = set()
    for item in items:
        dom = item["source_domain"]
        if dom not in seen_domains:
            seen_domains.add(dom)
            sampled.append(item["source_url"])
        if len(sampled) >= 6:
            break

    assert len(sampled) >= 3

    async def _probe_all(urls):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36"}
        async with httpx.AsyncClient(verify=False, headers=headers, timeout=10.0, follow_redirects=True) as hc:
            statuses = []
            for u in urls:
                r = await hc.head(u)
                if r.status_code in (403, 405, 501) or r.status_code >= 400:
                    async with hc.stream("GET", u) as gr:
                        statuses.append((u, gr.status_code))
                else:
                    statuses.append((u, r.status_code))
            return statuses

    results = asyncio.run(_probe_all(sampled))
    for url, code in results:
        assert 200 <= code <= 399, f"Broken link detected in live output: {url} -> HTTP {code}"


def test_4_filter_accurate_distinct_retrieval(client):
    """Requirement 4: Verify different filter combinations return distinct, accurately matched results."""
    r_intern = client.get("/api/opportunities?category=Internship").json()
    r_funding = client.get("/api/opportunities?category=Funding").json()
    r_scholar = client.get("/api/opportunities?category=Scholarship").json()

    assert r_intern["total_matching"] > 0
    assert r_funding["total_matching"] > 0
    assert r_scholar["total_matching"] > 0

    assert all(i["category"] == "Internship" for i in r_intern["items"])
    assert all(i["category"] == "Funding" for i in r_funding["items"])
    assert all(i["category"] == "Scholarship" for i in r_scholar["items"])

    ids_intern = {i["id"] for i in r_intern["items"]}
    ids_funding = {i["id"] for i in r_funding["items"]}
    assert ids_intern.isdisjoint(ids_funding), "Category filters returned overlapping/static results!"

    # Search query filter produces targeted subset
    r_query = client.get("/api/opportunities?q=research").json()
    assert r_query["total_matching"] > 0
    assert r_query["total_matching"] <= r_query["total_in_store"]

    # Non-matching query returns clean empty state (zero mock fallback)
    r_empty = client.get("/api/opportunities?q=zzzznonexistentopportunity99999").json()
    assert r_empty["total_matching"] == 0
    assert r_empty["items"] == []

    # Source Type filter distinguishes Government Portals vs Companies
    r_govt = client.get("/api/opportunities?source_type=Government").json()
    r_corp = client.get("/api/opportunities?source_type=Company%20%2F%20Corporate").json()
    assert r_govt["total_matching"] > 0
    assert r_corp["total_matching"] > 0
    assert all(i["source_type"] == "Government" for i in r_govt["items"])
    assert all(i["source_type"] == "Company / Corporate" for i in r_corp["items"])


def test_5_frontend_html_and_health_endpoints(client):
    """Requirement 5: Verify frontend renders cleanly and backend health/calendar/RAG endpoints work."""
    r_home = client.get("/")
    assert r_home.status_code == 200
    html = r_home.text
    assert "Refresh Live Data" in html
    assert "Apply / View Official Source" in html
    assert "Last verified:" in html
    assert "no live results found" in html.lower()
    assert "/api/opportunities" in html

    r_health = client.get("/api/health")
    assert r_health.status_code == 200
    h = r_health.json()
    assert h["status"] == "healthy"
    assert h["zero_mock_data"] is True
    assert h["total_opportunities"] >= 15

    # Verify calendar export works for a live opportunity
    first_id = client.get("/api/opportunities?limit=1").json()["items"][0]["id"]
    r_ics = client.get(f"/api/opportunities/{first_id}/calendar")
    assert r_ics.status_code == 200
    assert b"BEGIN:VCALENDAR" in r_ics.content
