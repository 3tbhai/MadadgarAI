"""Strict Pydantic v2 Schemas for Live Curated Opportunities (Internships, Scholarships, Research Funding)."""
from datetime import date, datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from urllib.parse import urlparse
from pydantic import BaseModel, Field, HttpUrl, field_validator


class OpportunityCategory(str, Enum):
    INTERNSHIP = "Internship"
    SCHOLARSHIP = "Scholarship"
    FUNDING = "Funding"


class LiveOpportunity(BaseModel):
    """Strict, validated schema for every live-scraped opportunity."""
    id: str = Field(..., min_length=6, description="Deterministic SHA-256 ID from canonical URL + normalized title")
    title: str = Field(..., min_length=4, description="Opportunity title")
    organization: str = Field(..., min_length=2, description="Issuing organization, university, company, or agency")
    category: OpportunityCategory = Field(..., description="Internship | Scholarship | Funding")
    source_type: str = Field(default="Government", description="Government | Company / Corporate | Foundation / University")
    domain: str = Field(default="General", description="Academic or industry domain")
    eligibility: str = Field(..., min_length=3, description="Eligibility requirements summary")
    degree_level: str = Field(default="All Levels", description="Undergraduate | Postgraduate | PhD / Faculty | All Levels")
    deadline: Optional[date] = Field(default=None, description="Parsed ISO closing date (expired dates are filtered out)")
    is_rolling: bool = Field(default=False, description="True if rolling or ongoing with no fixed closing date")
    stipend_or_amount: str = Field(default="See Official Listing", description="Stipend, scholarship amount, or grant ceiling")
    funding_type: str = Field(default="Merit / Competitive", description="Paid / Stipend | Fully Funded | Grant-in-Aid | Merit / Competitive")
    source_url: HttpUrl = Field(..., description="Verified reachable direct listing URL (HTTP 200-399)")
    source_domain: str = Field(default="", description="Canonical domain of the verified source URL")
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_verified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    http_status: int = Field(default=200, ge=200, le=399)
    summary: str = Field(..., min_length=10, description="Clean concise summary of the opportunity")
    tags: List[str] = Field(default_factory=list)
    location: Optional[str] = Field(default=None, description="Location or Remote / Global / India")

    @field_validator("title", "organization", "eligibility", "summary")
    @classmethod
    def strip_text(cls, v: str) -> str:
        cleaned = " ".join(v.split()).strip()
        if not cleaned:
            raise ValueError("Field cannot be empty")
        return cleaned

    @field_validator("source_domain", mode="before")
    @classmethod
    def derive_domain(cls, v: str, info) -> str:
        if v and str(v).strip():
            return str(v).strip().lower()
        src = info.data.get("source_url")
        if src:
            netloc = urlparse(str(src)).netloc.lower()
            return netloc.replace("www.", "")
        return ""

    @property
    def days_until_deadline(self) -> Optional[int]:
        if not self.deadline:
            return None
        return (self.deadline - date.today()).days


class ScrapeSourceTelemetry(BaseModel):
    source_name: str
    category: str
    fetched_raw: int = 0
    verified_saved: int = 0
    expired_filtered: int = 0
    broken_links_discarded: int = 0
    duplicates_removed: int = 0
    error: Optional[str] = None
    duration_ms: int = 0


class LiveRefreshReport(BaseModel):
    refreshed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_live_opportunities: int = 0
    newly_verified: int = 0
    expired_filtered: int = 0
    broken_links_discarded: int = 0
    duplicates_removed: int = 0
    cache_ttl_hours: int = 6
    from_cache: bool = False
    sources: List[ScrapeSourceTelemetry] = Field(default_factory=list)
    source_errors: List[str] = Field(default_factory=list)
    category_counts: Dict[str, int] = Field(default_factory=dict)


class OpportunityListResponse(BaseModel):
    items: List[LiveOpportunity]
    total_matching: int
    total_in_store: int
    last_refreshed_at: Optional[datetime] = None
    cache_age_minutes: Optional[int] = None
    cache_ttl_hours: int = 6
    source_errors: List[str] = Field(default_factory=list)
    facets: Dict[str, List[str]] = Field(default_factory=dict)
