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
    UGC = "UGC"
    STATE_GOVT = "State Govt"
    CSR_FOUNDATION = "CSR / Foundation"
    OTHER = "OTHER"


class EducationLevel(str, Enum):
    CLASS_9_10 = "Class 9-10 (Pre-Matric)"
    CLASS_11_12 = "Class 11-12 (Higher Secondary)"
    DIPLOMA = "Diploma / Polytechnic"
    UG_ENGINEERING = "UG - Engineering / Technology (B.Tech/B.E.)"
    UG_MEDICAL = "UG - Medical / Paramedical (MBBS/BDS/B.Pharm/Nursing)"
    UG_GENERAL = "UG - General (B.Sc / B.Com / B.A. / BBA / BCA)"
    POSTGRADUATE = "Postgraduate (M.Tech / M.Sc / M.Com / M.A. / MBA / MCA)"
    PHD_DOCTORAL = "PhD / Doctoral Research"


class SocialCategory(str, Enum):
    GENERAL = "General / Open"
    OBC_NCL = "OBC (Non-Creamy Layer)"
    SC = "SC (Scheduled Caste)"
    ST = "ST (Scheduled Tribe)"
    EWS = "EWS (Economically Weaker Section)"
    MINORITY = "Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)"


class GenderOption(str, Enum):
    ALL = "All Genders (Male / Female / Transgender)"
    FEMALE_ONLY = "Female Only"
    MALE = "Male"
    TRANSGENDER = "Transgender"


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
    direct_apply_url: Optional[str] = Field(
        default=None, description="Direct URL to registration or online application form"
    )
    portal_navigation_steps: List[str] = Field(
        default_factory=list, description="Step-by-step click path to find the scheme on the portal"
    )
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


# -------------------------------------------------------------
# Student Scholarship Intelligence Schemas (Vidyarthi AI)
# -------------------------------------------------------------

class DocumentCheckItem(BaseModel):
    document_name: str
    issuing_authority: str
    validity_and_rules: str
    how_to_obtain: str
    is_mandatory: bool = True


class HinglishExplainer(BaseModel):
    kaun_apply_kar_sakta_hai: str
    kitne_paise_milenge: str
    zaruri_documents: List[str] = Field(default_factory=list)
    official_portal_name: str
    official_portal_url: str
    aadhaar_seeding_warning: str = (
        "महत्वपूर्ण: बैंक खाता आधार और NPCI (DBT) से लिंक होना अनिवार्य है। बिना NPCI मैपिंग छात्रवृत्ति का पैसा बैंक खाते में नहीं आएगा।"
    )
    scam_alert: str = (
        "सावधान: यह सरकारी/अधिकृत स्कॉलरशिप है। इसके लिए कोई भी आवेदन शुल्क नहीं लगता। किसी भी अनाधिकृत एजेंट या फर्जी वेबसाइट को पैसे न दें।"
    )
    is_govt_verified: bool = True


class StudentProfileRequest(BaseModel):
    student_name: Optional[str] = "Student Applicant"
    state_domicile: str = "All India"
    education_level: EducationLevel = EducationLevel.UG_ENGINEERING
    course_name: Optional[str] = "B.Tech / Computer Science"
    social_category: SocialCategory = SocialCategory.GENERAL
    minority_community: Optional[str] = None  # e.g., Muslim, Christian, Sikh, Buddhist, Jain, Parsi
    gender: str = "Female"  # "Female", "Male", "Transgender"
    family_annual_income_inr: float = 200000.0  # Default 2 Lakhs
    academic_percentage: Optional[float] = 85.0
    is_single_girl_child: bool = False
    is_differently_abled_pwd: bool = False
    is_orphan_or_ward_of_defense: bool = False
    institute_type: Optional[str] = "AICTE Approved / UGC Recognized"
    top_k: int = Field(default=10, ge=1, le=30)


class StudentScholarshipMatchResult(BaseModel):
    foa: FundingOpportunity
    eligibility_status: str  # "ELIGIBLE", "HIGH_PROBABILITY", "WARNING", "INELIGIBLE"
    match_percentage: float = Field(..., ge=0.0, le=100.0)
    match_reasons: List[str] = Field(default_factory=list)
    warning_reasons: List[str] = Field(default_factory=list)
    estimated_financial_benefit: str
    portal_name: str
    portal_url: str
    direct_apply_url: Optional[str] = None
    portal_navigation_steps: List[str] = Field(default_factory=list)
    is_govt_verified: bool = True
    document_checklist: List[DocumentCheckItem] = Field(default_factory=list)
    hinglish_guide: Optional[HinglishExplainer] = None

