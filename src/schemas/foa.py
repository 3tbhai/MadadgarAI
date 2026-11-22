"""Pydantic schemas for MadadgaarAI Funding Opportunity Announcements (FOAs), Explainable Matching, RAG, and Document Intelligence."""
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


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
        ..., description="Unique deterministic opportunity identifier"
    )
    title: str = Field(..., description="Official title of the funding notice")
    agency: AgencyType = Field(..., description="Funding agency")
    issuing_authority: Optional[str] = Field(
        default=None, description="Official Ministry, Statutory Council, State Department, or CSR Foundation"
    )
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
    field_of_study: List[str] = Field(
        default_factory=list, description="Academic disciplines or fields eligible for the opportunity"
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
    duration_months: Optional[int] = Field(
        default=36, description="Standard project or scholarship tenure in months"
    )
    renewal_requirements: Optional[str] = Field(
        default=None, description="Annual continuation or renewal conditions"
    )
    common_mistakes: List[str] = Field(
        default_factory=list, description="Common application errors that lead to rejection"
    )
    official_source_references: List[str] = Field(
        default_factory=list, description="Official statutory guidelines and notification references"
    )
    last_verified_date: date = Field(
        default_factory=lambda: date(2026, 10, 15), description="Date when official guideline was last verified"
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
    publications_count: Optional[int] = Field(default=None, ge=0, description="Total peer-reviewed publications")
    sci_publications_count: Optional[int] = Field(default=None, ge=0, description="SCI/Scopus indexed journal papers")
    research_experience_years: Optional[int] = Field(default=None, ge=0, description="Years of post-degree research/teaching experience")
    research_methodologies: List[str] = Field(default_factory=list, description="Experimental or computational methods")
    previous_grants: List[str] = Field(default_factory=list, description="Prior extramural or seed grants managed")
    available_facilities: List[str] = Field(default_factory=list, description="Lab equipment, compute clusters, or clinical access")
    requested_funding_inr: Optional[float] = Field(default=None, ge=0, description="Target project budget in INR")
    preferred_duration_months: Optional[int] = Field(default=None, ge=1, description="Target project duration in months")
    has_industry_partner: Optional[bool] = Field(default=None, description="Whether an industry collaborator is onboarded")
    has_dsir_siro_recognition: Optional[bool] = Field(default=None, description="Whether host institution holds valid DSIR SIRO recognition")
    top_k: int = Field(default=5, ge=1, le=20)

    @field_validator("user_role", mode="before")
    @classmethod
    def normalize_user_role(cls, v: Any) -> Any:
        if isinstance(v, str):
            mapping = {
                "Faculty / PI": BeneficiaryType.FACULTY,
                "Faculty": BeneficiaryType.FACULTY,
                "Faculty / Principal Investigator": BeneficiaryType.FACULTY,
                "Early Career Researcher": BeneficiaryType.EARLY_CAREER,
                "Early Career": BeneficiaryType.EARLY_CAREER,
                "Women Scientists": BeneficiaryType.WOMEN_SCIENTIST,
                "Women Scientist": BeneficiaryType.WOMEN_SCIENTIST,
                "Women Scientists (WOS-A / WOS-B)": BeneficiaryType.WOMEN_SCIENTIST,
                "PhD / Postdocs": BeneficiaryType.PHD_POSTDOC,
                "PhD / Postdoc": BeneficiaryType.PHD_POSTDOC,
                "PhD Scholars & Postdoctoral Fellows": BeneficiaryType.PHD_POSTDOC,
                "UG / PG Students": BeneficiaryType.UG_PG_STUDENT,
                "UG / PG Student Researchers": BeneficiaryType.UG_PG_STUDENT,
                "Student": BeneficiaryType.UG_PG_STUDENT,
                "Startups & Industry Partners": BeneficiaryType.STARTUP_INDUSTRY,
                "Startup / Industry": BeneficiaryType.STARTUP_INDUSTRY,
            }
            if v in mapping:
                return mapping[v]
            if not v.strip():
                return BeneficiaryType.FACULTY
        return v or BeneficiaryType.FACULTY


class GrantMatchExplanation(BaseModel):
    why_grant_matches: str
    overlapping_interests: List[str] = Field(default_factory=list)
    satisfied_requirements: List[str] = Field(default_factory=list)
    unverified_requirements: List[str] = Field(default_factory=list)
    potential_disqualifiers: List[str] = Field(default_factory=list)
    actionable_improvements: List[str] = Field(default_factory=list)


class ComplianceCheckResult(BaseModel):
    is_compliant: bool
    status: str  # "ELIGIBLE", "INELIGIBLE", "WARNING"
    reasons: List[str] = Field(default_factory=list)
    age_check: Optional[str] = None
    qualification_check: Optional[str] = None
    institution_check: Optional[str] = None
    budget_compatibility_check: Optional[str] = None
    duration_compatibility_check: Optional[str] = None
    satisfied_criteria: List[str] = Field(default_factory=list)
    unverified_criteria: List[str] = Field(default_factory=list)
    disqualifying_factors: List[str] = Field(default_factory=list)
    improvement_suggestions: List[str] = Field(default_factory=list)


class MatchResult(BaseModel):
    foa: FundingOpportunity
    relevance_score: float = Field(
        ..., ge=0.0, le=1.0, description="Combined hybrid similarity score"
    )
    bm25_score: Optional[float] = None
    dense_score: Optional[float] = None
    domain_similarity_score: float = Field(default=0.0, ge=0.0, le=1.0)
    matching_keywords: List[str] = Field(default_factory=list)
    compliance: ComplianceCheckResult
    explanation: Optional[GrantMatchExplanation] = None
    deadline_proximity_days: Optional[int] = None
    deadline_status: str = "OPEN"
    non_probability_disclaimer: str = (
        "Alignment score reflects semantic and rule-based fit with call guidelines; it does not represent a statistical probability of grant award."
    )


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
    suggested_titles: List[str] = Field(default_factory=list)
    sections: List[ProposalSection] = Field(default_factory=list)
    suggested_budget_breakdown: Dict[str, str] = Field(default_factory=dict)
    compliance_checklist: List[str] = Field(default_factory=list)
    key_references: List[str] = Field(default_factory=list)
    guideline_verification_status: str = Field(
        default=(
            "Structurally formatted per statutory agency call conventions and Ministry of Finance OM norms. "
            "Applicant must verify call-specific annexures, institutional DSIR/PFMS registration, and exact equipment ceiling caps prior to submission."
        )
    )


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
    verification_status: str = "UNVERIFIED"  # "VERIFIED", "UNVERIFIED"


class HinglishExplainer(BaseModel):
    kaun_apply_kar_sakta_hai: str
    kitne_paise_milenge: str
    zaruri_documents: List[str] = Field(default_factory=list)
    official_portal_name: str
    official_portal_url: str
    renewal_kैसे_hoga: str = (
        "नवीनीकरण (Renewal): प्रत्येक वर्ष न्यूनतम 60% अंक (या 6.0 CGPA), 75% उपस्थिति और बिना किसी बैकलॉग के अगली कक्षा में प्रमोशन प्रमाण पत्र अपलोड करना अनिवार्य है।"
    )
    common_galatiyan: List[str] = Field(default_factory=list)
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
    field_of_study: Optional[str] = None
    year_of_study: Optional[int] = 1
    social_category: SocialCategory = SocialCategory.GENERAL
    minority_community: Optional[str] = None  # e.g., Muslim, Christian, Sikh, Buddhist, Jain, Parsi
    gender: str = "Female"  # "Female", "Male", "Transgender"
    family_annual_income_inr: float = 200000.0  # Default 2 Lakhs
    academic_percentage: Optional[float] = 85.0
    is_single_girl_child: bool = False
    is_differently_abled_pwd: bool = False
    is_orphan_or_ward_of_defense: bool = False
    institute_type: Optional[str] = "AICTE Approved / UGC Recognized"
    verified_documents: List[str] = Field(default_factory=list)
    has_npci_dbt_seeded: Optional[bool] = None
    min_scholarship_amount_inr: Optional[float] = None
    top_k: int = Field(default=15, ge=1, le=30)

    @field_validator("social_category", mode="before")
    @classmethod
    def normalize_social_category(cls, v: Any) -> Any:
        if isinstance(v, str):
            mapping = {
                "General": SocialCategory.GENERAL,
                "General / Open": SocialCategory.GENERAL,
                "GEN": SocialCategory.GENERAL,
                "OBC": SocialCategory.OBC_NCL,
                "OBC-NCL": SocialCategory.OBC_NCL,
                "OBC (Non-Creamy Layer)": SocialCategory.OBC_NCL,
                "SC": SocialCategory.SC,
                "SC (Scheduled Caste)": SocialCategory.SC,
                "Scheduled Caste": SocialCategory.SC,
                "ST": SocialCategory.ST,
                "ST (Scheduled Tribe)": SocialCategory.ST,
                "Scheduled Tribe": SocialCategory.ST,
                "EWS": SocialCategory.EWS,
                "EWS (Economically Weaker Section)": SocialCategory.EWS,
                "Minority": SocialCategory.MINORITY,
                "Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)": SocialCategory.MINORITY,
            }
            if v in mapping:
                return mapping[v]
        return v

    @field_validator("education_level", mode="before")
    @classmethod
    def normalize_education_level(cls, v: Any) -> Any:
        if isinstance(v, str):
            for level in EducationLevel:
                if v.lower() in level.value.lower() or level.value.lower() in v.lower():
                    return level
        return v


class StudentScholarshipMatchResult(BaseModel):
    foa: FundingOpportunity
    eligibility_status: str  # "ELIGIBLE", "HIGH_PROBABILITY", "WARNING", "INELIGIBLE"
    eligibility_confidence: str = "PRELIMINARY_ELIGIBLE"  # "VERIFIED_ELIGIBLE", "PRELIMINARY_ELIGIBLE", "CONDITIONAL_WARNING", "DISQUALIFIED"
    match_percentage: float = Field(..., ge=0.0, le=100.0)
    match_reasons: List[str] = Field(default_factory=list)
    warning_reasons: List[str] = Field(default_factory=list)
    missing_requirements: List[str] = Field(default_factory=list)
    disqualifying_conditions: List[str] = Field(default_factory=list)
    why_you_qualify_explanation: str = ""
    estimated_financial_benefit: str
    issuing_authority: str = "Statutory Portal"
    portal_name: str
    portal_url: str
    direct_apply_url: Optional[str] = None
    portal_navigation_steps: List[str] = Field(default_factory=list)
    renewal_requirements: str = ""
    common_mistakes_to_avoid: List[str] = Field(default_factory=list)
    last_verified_date: Optional[date] = None
    official_source_references: List[str] = Field(default_factory=list)
    deadline_proximity_days: Optional[int] = None
    deadline_urgency: str = "OPEN"
    score_breakdown: Dict[str, float] = Field(default_factory=dict)
    is_govt_verified: bool = True
    document_checklist: List[DocumentCheckItem] = Field(default_factory=list)
    hinglish_guide: Optional[HinglishExplainer] = None


# -------------------------------------------------------------
# Conversational RAG, Session Memory & Document Assistant Schemas
# -------------------------------------------------------------

class RAGCitation(BaseModel):
    source_id: str
    title: str
    issuing_authority: str
    official_url: str
    snippet: str
    relevance_score: float = Field(default=0.9, ge=0.0, le=1.0)


class RAGChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    language: str = "auto"  # "auto", "en", "hinglish"
    consent_to_remember: bool = True
    student_profile: Optional[Dict[str, Any]] = None
    researcher_profile: Optional[Dict[str, Any]] = None


class RAGChatResponse(BaseModel):
    answer: str
    language_used: str
    confidence_level: str  # "HIGH", "MEDIUM", "LOW"
    uncertainty_notice: Optional[str] = None
    citations: List[RAGCitation] = Field(default_factory=list)
    follow_up_suggestions: List[str] = Field(default_factory=list)
    session_id: str
    remembered_profile_updates: Dict[str, Any] = Field(default_factory=dict)


class DocumentFieldResult(BaseModel):
    field_name: str
    extracted_value: Optional[str] = None
    status: str  # "DETECTED", "MISSING", "WARNING"
    note: str


class DocumentAnalysisResponse(BaseModel):
    document_type: str
    detected_language: str = "en"
    extraction_method: str
    extracted_fields: List[DocumentFieldResult] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)
    checklist_recommendations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    suggested_profile_updates: Dict[str, Any] = Field(default_factory=dict)
    authenticity_disclaimer: str = (
        "IMPORTANT: Automated OCR/text analysis only checks field presence and formatting completeness. "
        "It does NOT certify legal validity or official authenticity. Final verification is performed by the issuing authority, DigiLocker, or Portal Nodal Officer."
    )
