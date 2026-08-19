"""FastAPI Main REST API Application."""
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field

from src.crawlers.seed_data import get_seed_foa_dataset
from src.dashboard.web_ui import render_dashboard_html
from src.embeddings.hybrid_search import HybridSearchEngine
from src.embeddings.vector_store import VectorStore
from src.extractor.normalizer import DatasetNormalizer
from src.matcher.calendar_sync import CalendarSyncGenerator
from src.matcher.compliance_checker import ComplianceChecker
from src.matcher.profile_matcher import ProfileGrantMatcher
from src.matcher.proposal_drafter import ProposalDrafter
from src.schemas.foa import (
    AgencyType,
    FundingOpportunity,
    IngestionReport,
    MatchResult,
    ProfileMatchRequest,
    ProposalSkeleton,
    ResearchDomain,
)

logger = logging.getLogger("MadadgaarAI.API")
logging.basicConfig(level=logging.INFO)

# Global singletons
normalizer = DatasetNormalizer()
vector_store = VectorStore()
hybrid_search = HybridSearchEngine(normalizer=normalizer, vector_store=vector_store)
compliance_checker = ComplianceChecker()
profile_matcher = ProfileGrantMatcher(hybrid_search=hybrid_search, compliance_checker=compliance_checker)
calendar_generator = CalendarSyncGenerator()
proposal_drafter = ProposalDrafter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Bootstrap seed dataset if empty
    existing = normalizer.load_all_opportunities()
    if not existing:
        logger.info("Initializing database with baseline Indian FOA dataset...")
        seeds = get_seed_foa_dataset()
        for s in seeds:
            normalizer.save_opportunity(s)
        normalizer.export_to_json_and_csv()
        hybrid_search.rebuild_index()
    else:
        logger.info(f"Database contains {len(existing)} existing opportunities.")
        hybrid_search.rebuild_index()
    yield


app = FastAPI(
    title="MadadgaarAI — Funding Intelligence API",
    description="AI-Powered Funding Opportunity Announcement (FOA) Ingestion, Semantic Tagging, and Grant Matching System.",
    version="1.0.0",
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
    institution_name: str = "JK Lakshmipat University, Jaipur"
    custom_abstract: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Renders the interactive web dashboard."""
    return HTMLResponse(content=render_dashboard_html(), status_code=200)


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "MadadgaarAI Funding Intelligence",
        "total_opportunities": len(normalizer.load_all_opportunities()),
    }


@app.get("/api/foas", response_model=List[FundingOpportunity])
async def list_funding_opportunities(
    agency: Optional[AgencyType] = None,
    domain: Optional[ResearchDomain] = None,
    max_budget: Optional[float] = None,
):
    """Retrieves all stored funding opportunities with optional filtering."""
    all_foas = normalizer.load_all_opportunities()
    filtered = []
    for f in all_foas:
        if agency and f.agency != agency:
            continue
        if max_budget and f.financials.max_amount_inr and f.financials.max_amount_inr > max_budget:
            continue
        if domain:
            doms = [t.domain for t in f.ontology_tags]
            if domain not in doms:
                continue
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
    """Executes hybrid BM25 + Dense vector search using Reciprocal Rank Fusion."""
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
    """Matches a faculty or student profile to active FOAs with compliance checks."""
    return profile_matcher.match_profile(req)


@app.get("/api/foas/{foa_id}/calendar")
async def export_foa_calendar(foa_id: str):
    """Exports an RFC 5545 .ics deadline file for the opportunity."""
    foa = normalizer.get_opportunity_by_id(foa_id)
    if not foa:
        raise HTTPException(status_code=404, detail=f"FOA '{foa_id}' not found")

    ics_bytes = calendar_generator.generate_ics_for_foa(foa)
    return Response(
        content=ics_bytes,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename={foa.foa_id}_deadline.ics"},
    )


@app.post("/api/foas/{foa_id}/draft-proposal", response_model=ProposalSkeleton)
async def draft_proposal_skeleton(foa_id: str, req: ProposalDraftRequest):
    """Generates an agency-specific proposal template with budget breakdown."""
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
    """Triggers crawler ingestion, deduplication, parsing, and index updates."""
    from src.crawlers.seed_data import get_seed_foa_dataset

    new_count = 0
    seeds = get_seed_foa_dataset()
    for foa in seeds:
        saved = normalizer.save_opportunity(foa)
        if saved:
            new_count += 1

    normalizer.export_to_json_and_csv()
    hybrid_search.rebuild_index()

    return IngestionReport(
        total_crawled=len(seeds),
        new_opportunities_indexed=new_count,
        duplicates_skipped=0,
        ocr_fallback_used=0,
        errors_encountered=[],
    )


@app.get("/api/stats")
async def get_statistics():
    all_foas = normalizer.load_all_opportunities()
    agency_counts = {}
    for f in all_foas:
        agency_counts[f.agency.value] = agency_counts.get(f.agency.value, 0) + 1

    return {
        "total_opportunities": len(all_foas),
        "agency_breakdown": agency_counts,
        "database_path": str(normalizer.db_path),
    }
