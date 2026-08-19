"""Pydantic schemas for MadadgaarAI Funding Opportunity Announcements (FOAs)."""
from datetime import date, datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator


class AgencyType(str, Enum):
    DST = "DST"
    ANRF = "ANRF/SERB"
    CSIR = "CSIR"
    AICTE = "AICTE"
    NSP = "NSP"
    DBT = "DBT"
    OTHER = "OTHER"


class BeneficiaryType(str, Enum):
    FACULTY = "Faculty / Principal Investigator"
    EARLY_CAREER = "Early Career Researcher"
    WOMEN_SCIENTIST = "Women Scientists"
    PHD_POSTDOC = "PhD Scholars & Postdoctoral Fellows"
    UG_PG_STUDENT = "UG / PG Students"
    STARTUP_INDUSTRY = "Startups & Industry Partners"
    INSTITUTE = "Academic / Research Institutions"


class ResearchDomain(str, Enum):
    COMPUTER_SCIENCE_AI = "Computer Science, AI & Data Science"
    ELECTRONICS_ELECTRICAL = "Electronics, VLSI & Electrical Engineering"
    MECHANICAL_CIVIL_INFRA = "Mechanical, Materials & Civil Engineering"
    BIOTECHNOLOGY_HEALTHCARE = "Biotechnology, Healthcare & Medical Tech"
    PHYSICAL_CHEMICAL_SCIENCES = "Physical, Chemical & Mathematical Sciences"
    ENERGY_ENVIRONMENT_SUSTAINABILITY = "Clean Energy, Climate & Sustainability"
    INTERDISCIPLINARY = "Interdisciplinary & Emerging Technologies"


class AcademicOntologyTag(BaseModel):
    domain: ResearchDomain
    thematic_thrust: str
    target_beneficiary: BeneficiaryType
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class FinancialCeiling(BaseModel):
    max_amount_inr: Optional[float] = Field(
        default=None, description="Maximum total grant value in INR"
    )
    stipend_monthly_inr: Optional[float] = Field(
        default=None, description="Monthly fellowship/stipend amount in INR"
    )
    institutional_overhead_pct: Optional[float] = Field(
        default=None, description="Overhead percentage allowed for host institute"
    )
    raw_budget_text: Optional[str] = Field(
        default=None, description="Original string describing financial terms"
    )


class Deadlines(BaseModel):
    open_date: Optional[date] = Field(
        default=None, description="Call opening date"
    )
    closing_date: Optional[date] = Field(
        default=None, description="Application submission deadline"
    )
    extended_closing_date: Optional[date] = Field(
        default=None, description="Extended deadline if applicable"
    )
    is_rolling: bool = Field(
        default=False, description="True if call accepts proposals year-round"
    )
    raw_deadline_text: Optional[str] = Field(
        default=None, description="Raw text representation of deadline"
    )

    @property
    def effective_deadline(self) -> Optional[date]:
        return self.extended_closing_date or self.closing_date


class EligibilityCriteria(BaseModel):
    target_beneficiaries: List[BeneficiaryType] = Field(default_factory=list)
    min_qualification: Optional[str] = Field(
        default=None, description="e.g., Ph.D. in Engineering / Sciences"
    )
    max_age_limit: Optional[int] = Field(
        default=None, description="Maximum age allowed in years"
    )
    eligible_institutions: List[str] = Field(
        default_factory=list,
        description="e.g., ['CFTI', 'UGC Recognized Universities', 'Private Universities with NAAC/NBA']",
    )
    requires_industry_partner: bool = Field(
        default=False, description="True if mandatory industry co-investigator"
    )
    raw_eligibility_text: Optional[str] = Field(
        default=None, description="Raw verbatim eligibility paragraph"
    )


class FundingOpportunity(BaseModel):
    foa_id: str = Field(
        ..., description="Unique deterministic FOA identifier (e.g. DST-CRG-2026-01)"
    )
    title: str = Field(..., description="Official title of the funding notice")
    agency: AgencyType = Field(..., description="Funding agency")
    scheme_name: Optional[str] = Field(
        default=None, description="Specific scheme under the agency"
    )
    source_url: str = Field(..., description="Direct link or portal URL")
    pdf_download_url: Optional[str] = Field(
        default=None, description="Direct download link to PDF circular"
    )
    raw_document_hash: str = Field(
        ..., description="SHA-256 hash of the circular content/file"
    )
    brief_summary: str = Field(
        ..., description="Standardized summary of the funding opportunity"
    )
    thematic_areas: List[str] = Field(
        default_factory=list, description="Keywords and thematic research topics"
    )
    ontology_tags: List[AcademicOntologyTag] = Field(
        default_factory=list, description="Categorized academic taxonomy mappings"
    )
    eligibility: EligibilityCriteria = Field(
        default_factory=EligibilityCriteria, description="Structured eligibility rules"
    )
    deadlines: Deadlines = Field(
        default_factory=Deadlines, description="Important dates"
    )
    financials: FinancialCeiling = Field(
        default_factory=FinancialCeiling, description="Financial guidelines"
    )
    full_text_content: Optional[str] = Field(
        default=None, description="Full extracted text from the circular"
    )
    is_ocr_extracted: bool = Field(
        default=False, description="True if parsed via OCR fallback"
    )
    ingested_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="Ingestion timestamp"
    )

    @field_validator("foa_id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("foa_id cannot be empty")
        return v.strip()


class ProfileMatchRequest(BaseModel):
    user_name: Optional[str] = "Researcher / Student"
    user_role: BeneficiaryType = BeneficiaryType.FACULTY
    research_summary: str = Field(
        ...,
        description="Abstract, research statement, project idea, or CV excerpt",
    )
    domain_interests: List[ResearchDomain] = Field(default_factory=list)
    applicant_age: Optional[int] = None
    institution_type: Optional[str] = None  # e.g., "CFTI", "Private", "State Govt"
    highest_degree: Optional[str] = None  # e.g., "Ph.D.", "M.Tech", "B.Tech"
    top_k: int = Field(default=5, ge=1, le=20)


class ComplianceCheckResult(BaseModel):
    is_compliant: bool
    status: str  # "ELIGIBLE", "INELIGIBLE", "WARNING"
    reasons: List[str] = Field(default_factory=list)
    age_check: Optional[str] = None
    qualification_check: Optional[str] = None
    institution_check: Optional[str] = None


class MatchResult(BaseModel):
    foa: FundingOpportunity
    relevance_score: float = Field(
        ..., ge=0.0, le=1.0, description="Combined hybrid similarity score"
    )
    bm25_score: Optional[float] = None
    dense_score: Optional[float] = None
    matching_keywords: List[str] = Field(default_factory=list)
    compliance: ComplianceCheckResult


class ProposalSection(BaseModel):
    section_title: str
    section_description: str
    drafted_content: str
    tips: List[str] = Field(default_factory=list)


class ProposalSkeleton(BaseModel):
    foa_id: str
    scheme_title: str
    agency: AgencyType
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    target_deadline: Optional[date] = None
    sections: List[ProposalSection] = Field(default_factory=list)
    suggested_budget_breakdown: Dict[str, str] = Field(default_factory=dict)
    compliance_checklist: List[str] = Field(default_factory=list)


class IngestionReport(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_crawled: int = 0
    new_opportunities_indexed: int = 0
    duplicates_skipped: int = 0
    ocr_fallback_used: int = 0
    errors_encountered: List[str] = Field(default_factory=list)
