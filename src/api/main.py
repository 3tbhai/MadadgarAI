"""FastAPI Main REST API Application for MadadgaarAI — Real-Time Live Opportunity Curation Platform."""
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, Query, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from src.ai.document_assistant import IntelligentDocumentAssistant
from src.ai.rag_engine import SaralSamjhautiRAG
from src.ai.session_store import ConversationalMemoryStore
from src.crawlers.pipeline import LiveOpportunityStore, LivePipelineOrchestrator, live_opportunity_to_foa
from src.dashboard.web_ui import render_dashboard_html
from src.embeddings.hybrid_search import HybridSearchEngine
from src.embeddings.vector_store import VectorStore
from src.extractor.normalizer import DatasetNormalizer
from src.matcher.calendar_sync import CalendarSyncGenerator
from src.matcher.compliance_checker import ComplianceChecker
from src.matcher.profile_matcher import ProfileGrantMatcher
from src.matcher.proposal_drafter import ProposalDrafter
from src.matcher.student_matcher import StudentScholarshipMatcher
from src.schemas.foa import (
    AgencyType,
    DocumentAnalysisResponse,
    DocumentCheckItem,
    EducationLevel,
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
vector_store = VectorStore()
hybrid_search = HybridSearchEngine(normalizer=normalizer, vector_store=vector_store)
compliance_checker = ComplianceChecker()
profile_matcher = ProfileGrantMatcher(hybrid_search=hybrid_search, compliance_checker=compliance_checker)
calendar_generator = CalendarSyncGenerator()
proposal_drafter = ProposalDrafter()
student_matcher = StudentScholarshipMatcher(normalizer=normalizer)
session_store = ConversationalMemoryStore()
rag_engine = SaralSamjhautiRAG(normalizer=normalizer, session_store=session_store)
document_assistant = IntelligentDocumentAssistant()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Refreshes live verified opportunities on startup if TTL cache is empty or expired."""
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
    yield


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return {
        "status": "healthy",
        "service": "MadadgaarAI Real-Time Opportunity Intelligence",
        "version": "3.0.0",
        "total_opportunities": live_store.count(),
        "last_refreshed_at": last_ts.isoformat() if last_ts else None,
        "cache_ttl_hours": live_store.cache_ttl_hours,
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
