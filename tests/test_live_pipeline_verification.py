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
    assert h["background_cron_active"] is True


def test_6_deep_page_analyzer_and_kanban_tracker_and_reranker(client):
    """Verify Features 1.4 (Deep-Page Analyzer), 1.5 (Kanban Tracker + .ics), 2.1-2.3 (New Scrapers), 3.1 (Reranker)."""
    from src.crawlers.live_scrapers import build_live_scrapers
    from src.embeddings.embedder import TextEmbedder

    # 1. Verify all 15 live scrapers are registered (including AICTE, ISRO, Tata Trusts, Ashby, Lever)
    scraper_classes = {s.__class__.__name__ for s in build_live_scrapers()}
    assert "AICTEIndiaInternshipScraper" in scraper_classes
    assert "ISRORespondScraper" in scraper_classes
    assert "TataTrustsCSRScraper" in scraper_classes
    assert "AshbyCompaniesScraper" in scraper_classes
    assert "LeverCompaniesScraper" in scraper_classes

    # 2. Verify Semantic Reranker (3.1) ranks relevant candidates above unrelated ones
    emb = TextEmbedder()
    s_rel = emb.rerank_score("AICTE engineering internship stipend", "AICTE National Internship Portal for B.Tech engineering students with monthly stipend", 0.5)
    s_irrel = emb.rerank_score("AICTE engineering internship stipend", " Biomedical clinical pathology laboratory mice experiment", 0.5)
    assert s_rel > s_irrel

    # 3. Verify Deep-Page Detail Enrichment (1.4) on a live opportunity
    items = client.get("/api/opportunities?limit=5").json()["items"]
    assert len(items) > 0
    target_opp = items[0]
    r_deep = client.post(f"/api/opportunities/{target_opp['id']}/deep-analyze")
    assert r_deep.status_code == 200
    deep_data = r_deep.json()
    assert deep_data["opp_id"] == target_opp["id"]
    assert "http_status" in deep_data
    assert "extracted_deadline" in deep_data
    assert "direct_attachments" in deep_data
    assert len(deep_data["eligibility_highlights"]) >= 1
    assert len(deep_data["required_documents"]) >= 1
    assert len(deep_data["application_steps"]) >= 1
    assert not re.match(r"^\d+\.\s", deep_data["application_steps"][0]), "Steps should not double-number inside <ol>"

    # 4. Verify Personal Application Kanban Tracker & Saved Deadlines .ics Export (1.5)
    test_sid = "pytest-kanban-session-001"
    r_add = client.post(
        f"/api/tracker/{test_sid}",
        json={"opp_id": target_opp["id"], "stage": "Saved", "notes": "Priority application"},
    )
    assert r_add.status_code == 200
    assert r_add.json()["total"] >= 1

    r_move = client.patch(
        f"/api/tracker/{test_sid}/{target_opp['id']}",
        json={"stage": "Preparing Docs", "notes": "Collecting marksheets"},
    )
    assert r_move.status_code == 200
    moved_item = [i for i in r_move.json()["items"] if i["opp_id"] == target_opp["id"]][0]
    assert moved_item["stage"] == "Preparing Docs"

    r_saved_ics = client.get(f"/api/tracker/{test_sid}/calendar.ics")
    assert r_saved_ics.status_code == 200
    assert b"BEGIN:VCALENDAR" in r_saved_ics.content

    r_del = client.delete(f"/api/tracker/{test_sid}/{target_opp['id']}")
    assert r_del.status_code == 200
    assert all(i["opp_id"] != target_opp["id"] for i in r_del.json()["items"])

    # 5. Verify filtered CSV export endpoint (Part 3)
    r_csv = client.get("/api/opportunities/export.csv?category=Internship")
    assert r_csv.status_code == 200
    assert "text/csv" in r_csv.headers.get("content-type", "")
    assert "Source URL" in r_csv.text
    assert "Internship" in r_csv.text

    # 6. Verify Resume / CV Semantic Opportunity Matcher (Part 2)
    r_res = client.post(
        "/api/resume/match",
        data={
            "raw_text": "B.Tech Computer Science student skilled in Python, Machine Learning, PyTorch, FastAPI, React, Data Science.",
            "category": "Internship",
            "top_k": "5",
        },
    )
    assert r_res.status_code == 200
    res_json = r_res.json()
    assert res_json["detected_degree"] == "Undergraduate"
    assert "Python" in res_json["detected_skills"]
    assert len(res_json["matches"]) >= 1
    assert res_json["matches"][0]["fit_score"] > 0

    # 7. Verify legacy unused crawler files remain deleted (3.3)
    project_root = Path(__file__).resolve().parent.parent
    for legacy_file in ("aicte_crawler.py", "anrf_crawler.py", "csir_crawler.py", "dst_crawler.py", "nsp_crawler.py"):
        assert not (project_root / "src" / "crawlers" / legacy_file).exists()
