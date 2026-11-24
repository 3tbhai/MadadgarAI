"""FastAPI Main REST API Application for MadadgaarAI — Real-Time Live Opportunity Curation Platform."""
import asyncio
from contextlib import asynccontextmanager
import csv
from datetime import date, datetime
import io
import logging
import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, Query, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from src.ai.document_assistant import IntelligentDocumentAssistant
from src.ai.rag_engine import SaralSamjhautiRAG
from src.ai.session_store import ConversationalMemoryStore
from src.api.saral_router import router as saral_v2_router, saral_gemini
from src.auth.security import get_google_client_id
from src.crawlers.deep_analyzer import DeepPageAnalysis, DeepPageAnalyzer
from src.crawlers.link_verifier import PLAYWRIGHT_AVAILABLE
from src.crawlers.pipeline import LiveOpportunityStore, LivePipelineOrchestrator, live_opportunity_to_foa
from src.dashboard.web_ui import render_dashboard_html
from src.embeddings.hybrid_search import HybridSearchEngine
from src.embeddings.vector_store import VectorStore
from src.extractor.normalizer import DatasetNormalizer
from src.matcher.calendar_sync import CalendarSyncGenerator
from src.matcher.compliance_checker import ComplianceChecker
from src.matcher.profile_matcher import ProfileGrantMatcher
from src.matcher.proposal_drafter import ProposalDrafter
from src.matcher.resume_matcher import ResumeMatchResponse, ResumeOpportunityMatcher
from src.matcher.student_matcher import StudentScholarshipMatcher
from src.schemas.foa import (
    AgencyType,
    Deadlines,
    DocumentAnalysisResponse,
    DocumentCheckItem,
    EducationLevel,
    EligibilityCriteria,
    FinancialCeiling,
    FundingOpportunity,
    HinglishExplainer,
    IngestionReport,
    MatchResult,
    ProfileMatchRequest,
    ProposalSkeleton,
    RAGChatRequest,
    RAGChatResponse,
    ResearchDomain,
    SocialCategory,
    StudentProfileRequest,
    StudentScholarshipMatchResult,
)
from src.schemas.opportunity import (
    LiveOpportunity,
    LiveRefreshReport,
    OpportunityListResponse,
)

logger = logging.getLogger("MadadgaarAI.API")
logging.basicConfig(level=logging.INFO)

# Global singletons (strictly backed by live scraped data — zero hardcoded/mock datasets)
normalizer = DatasetNormalizer()
live_store = LiveOpportunityStore()
live_pipeline = LivePipelineOrchestrator(store=live_store, normalizer=normalizer)
deep_analyzer = DeepPageAnalyzer()
vector_store = VectorStore()
hybrid_search = HybridSearchEngine(normalizer=normalizer, vector_store=vector_store)
compliance_checker = ComplianceChecker()
profile_matcher = ProfileGrantMatcher(hybrid_search=hybrid_search, compliance_checker=compliance_checker)
calendar_generator = CalendarSyncGenerator()
proposal_drafter = ProposalDrafter()
resume_matcher = ResumeOpportunityMatcher(live_store=live_store, embedder=vector_store.embedder)
student_matcher = StudentScholarshipMatcher(normalizer=normalizer)
session_store = ConversationalMemoryStore()
rag_engine = SaralSamjhautiRAG(normalizer=normalizer, session_store=session_store)
document_assistant = IntelligentDocumentAssistant()

_background_cron_task: Optional[asyncio.Task] = None


async def _background_auto_refresh_loop():
    """Periodically crawls & verifies live opportunities every CACHE_TTL_HOURS in the background."""
    interval_sec = max(300.0, float(live_store.cache_ttl_hours) * 3600.0)
    while True:
        try:
            await asyncio.sleep(interval_sec)
            logger.info("Background auto-refresh cron triggered: refreshing live opportunities...")
            report = await live_pipeline.refresh_live_data(force=True)
            hybrid_search.rebuild_index()
            rag_engine.rebuild_knowledge_base()
            logger.info(
                f"Background auto-refresh complete: {report.total_live_opportunities} live opportunities synced."
            )
        except asyncio.CancelledError:
            logger.info("Background auto-refresh cron cancelled cleanly.")
            break
        except Exception as exc:
            logger.error(f"Background auto-refresh cron error: {exc}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Refreshes live verified opportunities on startup and starts the periodic background cron."""
    global _background_cron_task
    try:
        report = await live_pipeline.refresh_live_data(force=False)
        logger.info(
            f"Startup live cache ready: {report.total_live_opportunities} verified opportunities "
            f"(from_cache={report.from_cache})."
        )
        hybrid_search.rebuild_index()
        rag_engine.rebuild_knowledge_base()
    except Exception as exc:
        logger.error(f"Startup live refresh encountered an error (no mock fallback used): {exc}")

    _background_cron_task = asyncio.create_task(_background_auto_refresh_loop())
    try:
        yield
    finally:
        if _background_cron_task and not _background_cron_task.done():
            _background_cron_task.cancel()
            try:
                await _background_cron_task
            except asyncio.CancelledError:
                pass


app = FastAPI(
    title="MadadgaarAI — Real-Time Scholarship, Internship & Research Funding Intelligence API",
    description=(
        "Real-time curated opportunity intelligence platform with async web scraping, "
        "Anti-404 link verification, expiration filtering, TTL caching, Hybrid BM25 + Dense RRF search, "
        "Saral Samjhauti RAG, and Document Intelligence."
    ),
    version="3.0.0",
    lifespan=lifespan,
)

_cors_origins_env = (os.getenv("MADADGAAR_CORS_ORIGINS") or "").strip()
_cors_origins = (
    [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
    if _cors_origins_env
    else ["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:3000"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)

app.include_router(saral_v2_router)


class SearchRequest(BaseModel):
    query: str
    agency_filter: Optional[AgencyType] = None
    max_budget_filter: Optional[float] = None
    domain_filter: Optional[ResearchDomain] = None
    top_k: int = Field(default=10, ge=1, le=50)


class SearchResponseItem(BaseModel):
    foa: FundingOpportunity
    relevance_score: float
    bm25_score: float
    dense_score: float


class ProposalDraftRequest(BaseModel):
    project_title: Optional[str] = None
    pi_name: str = "Dr. Principal Investigator"
    institution_name: str = "Recognized Academic / Research Institution"
    custom_abstract: Optional[str] = None


class SessionProfileUpdateRequest(BaseModel):
    consent_given: bool = True
    student_profile: Optional[Dict[str, Any]] = None
    researcher_profile: Optional[Dict[str, Any]] = None


class ChecklistToggleRequest(BaseModel):
    foa_id: str
    step_key: str
    completed: bool = True


class DocumentTextAnalyzeRequest(BaseModel):
    raw_text: str
    document_type_hint: Optional[str] = "AUTO"


class KanbanUpsertRequest(BaseModel):
    opp_id: str
    stage: str = "Saved"
    notes: str = ""
    title: Optional[str] = None
    organization: Optional[str] = None
    category: Optional[str] = None
    source_type: Optional[str] = None
    stipend_or_amount: Optional[str] = None
    deadline: Optional[str] = None
    source_url: Optional[str] = None


class KanbanStageUpdateRequest(BaseModel):
    stage: str
    notes: Optional[str] = None


class ReminderCreateRequest(BaseModel):
    channel: str = Field(default="browser", description="browser | email | webhook")
    target: str = Field(default="Browser Notification", description="Email address, webhook URL, or label")
    lead_days: int = Field(default=7, ge=1, le=60)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serves an inline SVG favicon to prevent 404 logs."""
    svg_icon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <rect width="100" height="100" rx="22" fill="#0f172a"/>
        <path d="M50 18 L86 36 L50 54 L14 36 Z" fill="#6366f1"/>
        <path d="M26 44 L26 65 Q50 82 74 65 L74 44" fill="none" stroke="#10b981" stroke-width="6" stroke-linecap="round"/>
        <circle cx="50" cy="54" r="4.5" fill="#38bdf8"/>
    </svg>"""
    return Response(content=svg_icon, media_type="image/svg+xml")


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Renders the live interactive web dashboard."""
    return HTMLResponse(content=render_dashboard_html(), status_code=200)


@app.get("/api/health")
async def health_check():
    last_ts = live_store.get_last_refreshed_at()
    cron_running = bool(_background_cron_task is not None and not _background_cron_task.done())
    return {
        "status": "healthy",
        "service": "MadadgaarAI Real-Time Opportunity Intelligence",
        "version": "4.0.0",
        "total_opportunities": live_store.count(),
        "last_refreshed_at": last_ts.isoformat() if last_ts else None,
        "cache_ttl_hours": live_store.cache_ttl_hours,
        "background_cron_active": cron_running,
        "embedding_backend": vector_store.embedder.backend_name,
        "llm_synthesis_backend": rag_engine.llm_adapter.active_backend,
        "saral_multitenant_rag_backend": saral_gemini.backend_label,
        "google_oauth_configured": bool(get_google_client_id()),
        "playwright_fallback_available": PLAYWRIGHT_AVAILABLE,
        "zero_mock_data": True,
    }


# -------------------------------------------------------------
# Real-Time Live Opportunity Endpoints (Primary v3.0 API)
# -------------------------------------------------------------

@app.get("/api/opportunities", response_model=OpportunityListResponse)
async def list_live_opportunities(
    category: Optional[str] = Query(default=None, description="Internship | Scholarship | Funding | All"),
    source_type: Optional[str] = Query(default=None, description="Government | Company / Corporate | Foundation / University | All"),
    domain: Optional[str] = Query(default=None, description="Academic or industry domain"),
    degree_level: Optional[str] = Query(default=None, description="Undergraduate | Postgraduate | PhD / Faculty | All"),
    funding_type: Optional[str] = Query(default=None, description="Paid / Stipend | Fully Funded | Grant-in-Aid | All"),
    deadline_window: Optional[str] = Query(default=None, description="urgent_14d | 30d | 90d | rolling | all"),
    q: Optional[str] = Query(default=None, description="Search query across title, org, domain, eligibility, summary"),
    sort: str = Query(default="deadline_asc", description="deadline_asc | recent_desc | title_asc"),
    limit: int = Query(default=120, ge=1, le=200),
):
    """Dynamically queries and filters the live verified opportunity store. Zero mock fallbacks."""
    return live_store.query(
        category=category,
        source_type=source_type,
        domain=domain,
        degree_level=degree_level,
        funding_type=funding_type,
        deadline_window=deadline_window,
        q=q,
        sort=sort,
        limit=limit,
    )


@app.post("/api/opportunities/refresh", response_model=LiveRefreshReport)
async def refresh_live_opportunities(force: bool = Query(default=True)):
    """Triggers a live async crawl, expiration filter, deduplication, and Anti-404 link verification."""
    report = await live_pipeline.refresh_live_data(force=force)
    hybrid_search.rebuild_index()
    rag_engine.rebuild_knowledge_base()
    return report


@app.get("/api/opportunities/export.csv")
async def export_filtered_opportunities_csv(
    category: Optional[str] = Query(default=None),
    source_type: Optional[str] = Query(default=None),
    domain: Optional[str] = Query(default=None),
    degree_level: Optional[str] = Query(default=None),
    funding_type: Optional[str] = Query(default=None),
    deadline_window: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None),
    sort: str = Query(default="deadline_asc"),
    limit: int = Query(default=200, ge=1, le=500),
):
    """Exports the currently filtered live opportunities as a UTF-8 CSV file."""
    result = live_store.query(
        category=category,
        source_type=source_type,
        domain=domain,
        degree_level=degree_level,
        funding_type=funding_type,
        deadline_window=deadline_window,
        q=q,
        sort=sort,
        limit=limit,
    )
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "ID", "Title", "Organization", "Category", "Source Type", "Domain",
        "Degree Level", "Stipend / Amount", "Funding Type", "Deadline",
        "Is Rolling", "Location", "Eligibility", "HTTP Status", "Source URL",
    ])
    for o in result.items:
        writer.writerow([
            o.id, o.title, o.organization, o.category.value, o.source_type,
            o.domain, o.degree_level, o.stipend_or_amount, o.funding_type,
            o.deadline.isoformat() if o.deadline else "Rolling",
            "Yes" if o.is_rolling else "No",
            o.location or "Global / India",
            o.eligibility, o.http_status, str(o.source_url),
        ])
    return Response(
        content=buf.getvalue().encode("utf-8-sig"),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=madadgaarai_filtered_opportunities.csv"},
    )


@app.get("/api/opportunities/{opp_id}", response_model=LiveOpportunity)
async def get_live_opportunity(opp_id: str):
    for opp in live_store.load_all(exclude_expired=False):
        if opp.id == opp_id:
            return opp
    raise HTTPException(status_code=404, detail=f"Opportunity '{opp_id}' not found")


@app.get("/api/opportunities/{opp_id}/calendar")
async def export_live_opportunity_calendar(opp_id: str):
    for opp in live_store.load_all(exclude_expired=False):
        if opp.id == opp_id:
            foa = live_opportunity_to_foa(opp)
            ics_bytes = calendar_generator.generate_ics_for_foa(foa)
            return Response(
                content=ics_bytes,
                media_type="text/calendar",
                headers={"Content-Disposition": f"attachment; filename={opp.id}_deadline.ics"},
            )
    raise HTTPException(status_code=404, detail=f"Opportunity '{opp_id}' not found")


@app.post("/api/opportunities/{opp_id}/deep-analyze", response_model=DeepPageAnalysis)
async def deep_analyze_live_opportunity(opp_id: str):
    """Fetches the live destination HTML/PDF circular on demand and extracts structured details."""
    for opp in live_store.load_all(exclude_expired=False):
        if opp.id == opp_id:
            return await deep_analyzer.analyze_opportunity(opp)
    raise HTTPException(status_code=404, detail=f"Opportunity '{opp_id}' not found")


# -------------------------------------------------------------
# Personal Application Kanban Tracker & Saved Deadlines (.ics)
# -------------------------------------------------------------

@app.get("/api/tracker/{session_id}")
async def get_kanban_tracker(session_id: str):
    """Returns all saved Kanban application items for a user session."""
    items = session_store.get_kanban_items(session_id)
    return {
        "session_id": session_id,
        "total": len(items),
        "items": items,
    }


@app.post("/api/tracker/{session_id}")
async def add_or_update_kanban_item(session_id: str, req: KanbanUpsertRequest):
    """Saves an opportunity into the user's Personal Application Kanban Tracker."""
    matched_opp: Optional[LiveOpportunity] = None
    for opp in live_store.load_all(exclude_expired=False):
        if opp.id == req.opp_id:
            matched_opp = opp
            break

    if matched_opp:
        opp_data = {
            "id": matched_opp.id,
            "title": matched_opp.title,
            "organization": matched_opp.organization,
            "category": matched_opp.category.value,
            "source_type": matched_opp.source_type,
            "stipend_or_amount": matched_opp.stipend_or_amount,
            "deadline": matched_opp.deadline.isoformat() if matched_opp.deadline else None,
            "source_url": str(matched_opp.source_url),
        }
    else:
        if not req.title or not req.source_url:
            raise HTTPException(status_code=404, detail=f"Opportunity '{req.opp_id}' not found in live store")
        opp_data = {
            "id": req.opp_id,
            "title": req.title,
            "organization": req.organization or "Official Portal",
            "category": req.category or "Scholarship",
            "source_type": req.source_type or "Government",
            "stipend_or_amount": req.stipend_or_amount or "See portal",
            "deadline": req.deadline,
            "source_url": req.source_url,
        }

    items = session_store.upsert_kanban_item(
        session_id=session_id,
        opp_data=opp_data,
        stage=req.stage,
        notes=req.notes,
    )
    return {"session_id": session_id, "total": len(items), "items": items}


@app.patch("/api/tracker/{session_id}/{opp_id}")
async def move_kanban_item_stage(session_id: str, opp_id: str, req: KanbanStageUpdateRequest):
    """Moves a saved application card across Kanban stages (Saved -> Preparing Docs -> Applied -> Result)."""
    items = session_store.update_kanban_stage(
        session_id=session_id,
        opp_id=opp_id,
        stage=req.stage,
        notes=req.notes,
    )
    return {"session_id": session_id, "total": len(items), "items": items}


@app.delete("/api/tracker/{session_id}/{opp_id}")
async def remove_kanban_tracker_item(session_id: str, opp_id: str):
    """Removes an opportunity from the user's Kanban tracker."""
    items = session_store.remove_kanban_item(session_id=session_id, opp_id=opp_id)
    return {"session_id": session_id, "total": len(items), "items": items}


@app.get("/api/tracker/{session_id}/calendar.ics")
async def export_saved_kanban_calendar(session_id: str):
    """Exports an iCalendar (.ics) bundle containing only the user's saved Kanban opportunities."""
    items = session_store.get_kanban_items(session_id)
    live_lookup = {o.id: o for o in live_store.load_all(exclude_expired=False)}
    saved_foas: List[FundingOpportunity] = []

    for item in items:
        oid = item["opp_id"]
        if oid in live_lookup:
            saved_foas.append(live_opportunity_to_foa(live_lookup[oid]))
        else:
            parsed_dl = None
            if item.get("deadline"):
                try:
                    parsed_dl = date.fromisoformat(str(item["deadline"])[:10])
                except ValueError:
                    parsed_dl = None
            saved_foas.append(
                FundingOpportunity(
                    foa_id=oid,
                    title=item["title"],
                    agency=AgencyType.DST,
                    issuing_authority=item["organization"],
                    source_url=item["source_url"],
                    direct_apply_url=item["source_url"],
                    brief_summary=f"Saved Kanban Opportunity ({item['stage']})",
                    financials=FinancialCeiling(raw_budget_text=item.get("stipend_or_amount") or "See portal"),
                    eligibility=EligibilityCriteria(raw_eligibility_text="Saved in Personal Tracker"),
                    deadlines=Deadlines(closing_date=parsed_dl, is_rolling=parsed_dl is None),
                )
            )

    ics_bytes = calendar_generator.generate_multi_foa_ics(saved_foas)
    return Response(
        content=ics_bytes,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename=madadgaar_saved_deadlines_{session_id[:8]}.ics"},
    )


def _compute_due_kanban_alerts(session_id: str, max_lead_days: int = 14) -> List[Dict[str, Any]]:
    today = date.today()
    due: List[Dict[str, Any]] = []
    for item in session_store.get_kanban_items(session_id):
        dl_raw = item.get("deadline")
        if not dl_raw:
            continue
        try:
            dl_date = date.fromisoformat(str(dl_raw)[:10])
            days_left = (dl_date - today).days
            if 0 <= days_left <= max_lead_days:
                due.append({
                    "opp_id": item["opp_id"],
                    "title": item["title"],
                    "organization": item["organization"],
                    "stage": item["stage"],
                    "deadline": dl_date.isoformat(),
                    "days_left": days_left,
                    "source_url": item["source_url"],
                })
        except ValueError:
            continue
    due.sort(key=lambda x: x["days_left"])
    return due


@app.get("/api/tracker/{session_id}/reminders")
async def get_tracker_reminders(session_id: str):
    """Returns configured reminder subscriptions and currently approaching saved deadlines."""
    reminders = session_store.list_reminders(session_id)
    max_lead = max([r["lead_days"] for r in reminders], default=14)
    return {
        "session_id": session_id,
        "reminders": reminders,
        "due_alerts": _compute_due_kanban_alerts(session_id, max_lead_days=max_lead),
    }


@app.post("/api/tracker/{session_id}/reminders")
async def add_tracker_reminder(session_id: str, req: ReminderCreateRequest):
    """Creates a deadline reminder subscription (Browser, Email, or Discord/Slack Webhook)."""
    reminders = session_store.add_reminder(
        session_id=session_id,
        channel=req.channel,
        target=req.target or "Browser Alert",
        lead_days=req.lead_days,
    )
    return {
        "session_id": session_id,
        "reminders": reminders,
        "due_alerts": _compute_due_kanban_alerts(session_id, max_lead_days=req.lead_days),
    }


@app.delete("/api/tracker/{session_id}/reminders/{reminder_id}")
async def delete_tracker_reminder(session_id: str, reminder_id: int):
    reminders = session_store.delete_reminder(session_id=session_id, reminder_id=reminder_id)
    return {"session_id": session_id, "reminders": reminders}


@app.post("/api/tracker/{session_id}/reminders/dispatch")
async def dispatch_tracker_reminders(session_id: str):
    """Evaluates approaching deadlines and dispatches webhook alerts (or returns email/browser summary)."""
    import httpx as _httpx

    reminders = session_store.list_reminders(session_id)
    dispatched: List[Dict[str, Any]] = []
    for rem in reminders:
        due = _compute_due_kanban_alerts(session_id, max_lead_days=rem["lead_days"])
        summary_lines = [
            f"- {d['title']} ({d['days_left']}d left, closes {d['deadline']}): {d['source_url']}"
            for d in due[:5]
        ]
        msg_text = (
            f"MadadgaarAI Deadline Alert ({len(due)} saved opportunities closing within {rem['lead_days']} days):\n"
            + ("\n".join(summary_lines) if summary_lines else "No saved items closing within your alert window right now.")
        )
        status = "queued_preview"
        if rem["channel"] == "webhook" and rem["target"].startswith(("http://", "https://")):
            try:
                async with _httpx.AsyncClient(timeout=6.0) as hc:
                    wr = await hc.post(rem["target"], json={"content": msg_text, "text": msg_text, "alerts": due})
                    status = f"webhook_http_{wr.status_code}"
            except Exception as exc:
                status = f"webhook_error:{type(exc).__name__}"
        dispatched.append({
            "reminder_id": rem["id"],
            "channel": rem["channel"],
            "target": rem["target"],
            "due_count": len(due),
            "status": status,
            "preview": msg_text,
        })
    return {"session_id": session_id, "dispatched": dispatched}


# -------------------------------------------------------------
# Backward-Compatible FOA, Search, Calendar & Proposal Endpoints
# -------------------------------------------------------------

@app.get("/api/foas", response_model=List[FundingOpportunity])
async def list_funding_opportunities(
    agency: Optional[AgencyType] = None,
    domain: Optional[ResearchDomain] = None,
    max_budget: Optional[float] = None,
):
    """Retrieves all live-indexed opportunities in FOA format."""
    all_foas = normalizer.load_all_opportunities()
    filtered = []
    seen_ids = set()
    for f in all_foas:
        if f.foa_id in seen_ids:
            continue
        if agency and f.agency != agency:
            continue
        if max_budget and f.financials.max_amount_inr and f.financials.max_amount_inr > max_budget:
            continue
        if domain:
            doms = [t.domain for t in f.ontology_tags]
            if domain not in doms:
                continue
        seen_ids.add(f.foa_id)
        filtered.append(f)
    return filtered


@app.get("/api/foas/{foa_id}", response_model=FundingOpportunity)
async def get_foa_by_id(foa_id: str):
    foa = normalizer.get_opportunity_by_id(foa_id)
    if not foa:
        raise HTTPException(status_code=404, detail=f"FOA '{foa_id}' not found")
    return foa


@app.post("/api/search", response_model=List[SearchResponseItem])
async def search_opportunities(req: SearchRequest):
    """Executes hybrid BM25 + Dense vector search using Reciprocal Rank Fusion on live data."""
    results = hybrid_search.search_hybrid(
        query=req.query,
        top_k=req.top_k,
        agency_filter=req.agency_filter,
        max_budget_filter=req.max_budget_filter,
        domain_filter=req.domain_filter,
    )
    return [
        SearchResponseItem(
            foa=foa,
            relevance_score=r_score,
            bm25_score=b_score,
            dense_score=d_score,
        )
        for foa, r_score, b_score, d_score in results
    ]


@app.post("/api/match-profile", response_model=List[MatchResult])
async def match_profile(req: ProfileMatchRequest):
    """Matches a researcher profile against live-indexed opportunities with explainable compliance checks."""
    return profile_matcher.match_profile(req)


@app.get("/api/foas/{foa_id}/calendar")
async def export_foa_calendar(foa_id: str):
    foa = normalizer.get_opportunity_by_id(foa_id)
    if not foa:
        raise HTTPException(status_code=404, detail=f"FOA '{foa_id}' not found")
    ics_bytes = calendar_generator.generate_ics_for_foa(foa)
    return Response(
        content=ics_bytes,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename={foa.foa_id}_deadline.ics"},
    )


@app.get("/api/calendar/upcoming.ics")
async def export_all_upcoming_calendars():
    all_foas = normalizer.load_all_opportunities()
    ics_bytes = calendar_generator.generate_multi_foa_ics(all_foas)
    return Response(
        content=ics_bytes,
        media_type="text/calendar",
        headers={"Content-Disposition": "attachment; filename=madadgaarai_live_deadlines.ics"},
    )


@app.get("/api/deadlines/upcoming")
async def get_upcoming_deadlines():
    all_foas = normalizer.load_all_opportunities()
    return calendar_generator.get_upcoming_deadlines(all_foas)


@app.post("/api/foas/{foa_id}/draft-proposal", response_model=ProposalSkeleton)
async def draft_proposal_skeleton(foa_id: str, req: ProposalDraftRequest):
    foa = normalizer.get_opportunity_by_id(foa_id)
    if not foa:
        for opp in live_store.load_all(exclude_expired=False):
            if opp.id == foa_id:
                foa = live_opportunity_to_foa(opp)
                break
    if not foa:
        raise HTTPException(status_code=404, detail=f"FOA '{foa_id}' not found")
    return proposal_drafter.draft_proposal_skeleton(
        foa=foa,
        project_title=req.project_title,
        pi_name=req.pi_name,
        institution_name=req.institution_name,
        custom_abstract=req.custom_abstract,
    )


@app.post("/api/ingest/trigger", response_model=IngestionReport)
async def trigger_ingestion():
    """Triggers a live real-time crawl & Anti-404 verification pipeline (zero seed data)."""
    report = await live_pipeline.refresh_live_data(force=True)
    hybrid_search.rebuild_index()
    rag_engine.rebuild_knowledge_base()
    return IngestionReport(
        total_crawled=sum(s.fetched_raw for s in report.sources),
        new_opportunities_indexed=report.total_live_opportunities,
        duplicates_skipped=report.duplicates_removed,
        ocr_fallback_used=0,
        errors_encountered=report.source_errors,
    )


@app.get("/api/stats")
async def get_statistics():
    opps = live_store.load_all(exclude_expired=True)
    cat_counts: Dict[str, int] = {}
    domain_counts: Dict[str, int] = {}
    source_type_counts: Dict[str, int] = {}
    for o in opps:
        cat_counts[o.category.value] = cat_counts.get(o.category.value, 0) + 1
        domain_counts[o.domain] = domain_counts.get(o.domain, 0) + 1
        source_type_counts[o.source_type] = source_type_counts.get(o.source_type, 0) + 1
    return {
        "total_opportunities": len(opps),
        "category_breakdown": cat_counts,
        "source_type_breakdown": source_type_counts,
        "domain_breakdown": domain_counts,
        "last_refreshed_at": live_store.get_last_refreshed_at(),
        "database_path": str(live_store.db_path),
    }


# -------------------------------------------------------------
# Student Scholarship Endpoints
# -------------------------------------------------------------

@app.post("/api/student/match", response_model=List[StudentScholarshipMatchResult])
async def match_student_profile(req: StudentProfileRequest):
    return student_matcher.match_student(req)


@app.get("/api/student/scholarships", response_model=List[FundingOpportunity])
async def list_student_scholarships(agency: Optional[AgencyType] = None):
    all_student_foas = student_matcher.get_all_student_scholarships()
    if agency:
        all_student_foas = [f for f in all_student_foas if f.agency == agency]
    return all_student_foas


@app.get("/api/student/scholarships/{foa_id}/checklist", response_model=List[DocumentCheckItem])
async def get_scholarship_document_checklist(foa_id: str):
    foa = normalizer.get_opportunity_by_id(foa_id)
    if not foa:
        raise HTTPException(status_code=404, detail=f"Opportunity '{foa_id}' not found")
    return student_matcher.generate_document_checklist(foa)


@app.get("/api/student/scholarships/{foa_id}/hinglish", response_model=HinglishExplainer)
async def get_scholarship_hinglish_guide(foa_id: str):
    foa = normalizer.get_opportunity_by_id(foa_id)
    if not foa:
        raise HTTPException(status_code=404, detail=f"Opportunity '{foa_id}' not found")
    return student_matcher.generate_hinglish_guide(foa)


@app.get("/api/student/meta")
async def get_student_meta_options():
    return {
        "states": [
            "All India", "Uttar Pradesh", "Maharashtra", "Bihar", "Rajasthan",
            "Madhya Pradesh", "West Bengal", "Karnataka", "Tamil Nadu",
            "Andhra Pradesh", "Telangana", "Kerala", "Gujarat", "Punjab",
            "Haryana", "Odisha", "Assam / North Eastern States", "Delhi NCR", "Jammu & Kashmir",
        ],
        "education_levels": [e.value for e in EducationLevel],
        "social_categories": [c.value for c in SocialCategory],
        "genders": ["Female", "Male", "Transgender"],
    }


# -------------------------------------------------------------
# Advanced AI Endpoints: RAG Chat, Session Memory & Document Assistant
# -------------------------------------------------------------

@app.post("/api/ai/chat", response_model=RAGChatResponse)
async def chat_with_saral_samjhauti(req: RAGChatRequest):
    return rag_engine.chat(req)


@app.get("/api/session/{session_id}")
async def get_session_memory(session_id: str):
    return session_store.get_or_create_session(session_id=session_id)


@app.post("/api/session/{session_id}/profile")
async def update_session_profile(session_id: str, req: SessionProfileUpdateRequest):
    return session_store.save_session(
        session_id=session_id,
        consent_given=req.consent_given,
        student_profile=req.student_profile,
        researcher_profile=req.researcher_profile,
    )


@app.post("/api/session/{session_id}/checklist")
async def update_session_checklist(session_id: str, req: ChecklistToggleRequest):
    return session_store.update_checklist_step(
        session_id=session_id,
        foa_id=req.foa_id,
        step_key=req.step_key,
        completed=req.completed,
    )


@app.delete("/api/session/{session_id}")
async def delete_session_memory(session_id: str):
    session_store.clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}


@app.post("/api/documents/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document_text(req: DocumentTextAnalyzeRequest):
    return document_assistant.analyze_document(
        raw_text=req.raw_text,
        document_type_hint=req.document_type_hint,
    )


@app.post("/api/documents/upload", response_model=DocumentAnalysisResponse)
async def analyze_uploaded_document(
    file: UploadFile = File(...),
    document_type_hint: str = Form("AUTO"),
):
    file_bytes = await file.read()
    return document_assistant.analyze_document(
        file_bytes=file_bytes,
        filename=file.filename,
        document_type_hint=document_type_hint,
    )


@app.post("/api/resume/match", response_model=ResumeMatchResponse)
async def match_resume_to_live_opportunities(
    file: Optional[UploadFile] = File(default=None),
    raw_text: Optional[str] = Form(default=None),
    category: Optional[str] = Form(default="All"),
    top_k: int = Form(default=10),
):
    """Parses an uploaded PDF/DOCX/TXT resume or pasted CV text and semantically ranks live opportunities."""
    file_bytes = await file.read() if file else None
    filename = file.filename if file else None
    if not file_bytes and not (raw_text and raw_text.strip()):
        raise HTTPException(status_code=400, detail="Provide a resume file or pasted resume text.")
    return resume_matcher.match_resume(
        raw_text=raw_text,
        file_bytes=file_bytes,
        filename=filename,
        category=category,
        top_k=top_k,
    )
