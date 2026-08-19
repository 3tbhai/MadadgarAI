"""Structured Entity Extractor for Indian Funding Opportunities."""
import hashlib
import logging
import re
from datetime import date, datetime, timezone
from typing import List, Optional

from src.extractor.patterns import (
    AGE_LIMIT_PATTERN,
    BENEFICIARY_KEYWORDS,
    BUDGET_CRORES_PATTERN,
    BUDGET_LAKHS_PATTERN,
    BUDGET_NUMERIC_PATTERN,
    DATE_DD_MM_YYYY_PATTERN,
    DATE_TEXTUAL_PATTERN,
    INSTITUTION_KEYWORDS,
    OVERHEAD_PCT_PATTERN,
    QUALIFICATION_KEYWORDS,
    ROLLING_CALL_PATTERN,
    STIPEND_MONTHLY_PATTERN,
)
from src.schemas.foa import (
    AcademicOntologyTag,
    AgencyType,
    BeneficiaryType,
    Deadlines,
    EligibilityCriteria,
    FinancialCeiling,
    FundingOpportunity,
    ResearchDomain,
)

logger = logging.getLogger("MadadgaarAI.Extractor.Entity")

MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


class FOAEntityExtractor:
    def __init__(self):
        pass

    def extract_financials(self, text: str) -> FinancialCeiling:
        max_amount: Optional[float] = None
        stipend: Optional[float] = None
        overhead: Optional[float] = None

        # Check Crores
        cr_match = BUDGET_CRORES_PATTERN.search(text)
        if cr_match:
            try:
                max_amount = float(cr_match.group(1)) * 10000000.0
            except ValueError:
                pass

        # Check Lakhs
        if max_amount is None:
            lakh_match = BUDGET_LAKHS_PATTERN.search(text)
            if lakh_match:
                try:
                    max_amount = float(lakh_match.group(1)) * 100000.0
                except ValueError:
                    pass

        # Check Numeric standard
        if max_amount is None:
            num_match = BUDGET_NUMERIC_PATTERN.search(text)
            if num_match:
                try:
                    val_str = num_match.group(1).replace(",", "")
                    val = float(val_str)
                    if val >= 10000:  # Exclude tiny numbers
                        max_amount = val
                except ValueError:
                    pass

        # Check Monthly Stipend
        stipend_match = STIPEND_MONTHLY_PATTERN.search(text)
        if stipend_match:
            try:
                stipend = float(stipend_match.group(1).replace(",", ""))
            except ValueError:
                pass

        # Check Overhead
        overhead_match = OVERHEAD_PCT_PATTERN.search(text)
        if overhead_match:
            try:
                overhead = float(overhead_match.group(1))
            except ValueError:
                pass

        return FinancialCeiling(
            max_amount_inr=max_amount,
            stipend_monthly_inr=stipend,
            institutional_overhead_pct=overhead,
            raw_budget_text=text[:300] if max_amount else None,
        )

    def extract_dates(self, text: str) -> Deadlines:
        dates_found: List[date] = []
        is_rolling = bool(ROLLING_CALL_PATTERN.search(text))

        # Check numeric DD-MM-YYYY
        for match in DATE_DD_MM_YYYY_PATTERN.finditer(text):
            try:
                day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
                if 1 <= day <= 31 and 1 <= month <= 12 and 2024 <= year <= 2030:
                    dates_found.append(date(year, month, day))
            except ValueError:
                continue

        # Check textual dates (e.g., 30 September 2026)
        for match in DATE_TEXTUAL_PATTERN.finditer(text):
            try:
                day_str = re.sub(r"\D", "", match.group(1))
                day = int(day_str)
                month_str = match.group(2).lower()[:3]
                month = MONTH_MAP.get(month_str, 1)
                year = int(match.group(3))
                if 1 <= day <= 31 and 2024 <= year <= 2030:
                    dates_found.append(date(year, month, day))
            except ValueError:
                continue

        # Remove duplicate dates and sort
        unique_dates = sorted(list(set(dates_found)))
        open_d: Optional[date] = None
        close_d: Optional[date] = None
        ext_d: Optional[date] = None

        if len(unique_dates) == 1:
            close_d = unique_dates[0]
        elif len(unique_dates) == 2:
            open_d = unique_dates[0]
            close_d = unique_dates[1]
        elif len(unique_dates) >= 3:
            open_d = unique_dates[0]
            close_d = unique_dates[1]
            ext_d = unique_dates[2]

        return Deadlines(
            open_date=open_d,
            closing_date=close_d,
            extended_closing_date=ext_d,
            is_rolling=is_rolling,
            raw_deadline_text=f"Closing Date: {close_d.isoformat() if close_d else ('Rolling' if is_rolling else 'Not specified')}",
        )

    def extract_eligibility(self, text: str) -> EligibilityCriteria:
        age_limit: Optional[int] = None
        age_match = AGE_LIMIT_PATTERN.search(text)
        if age_match:
            try:
                age_val = int(age_match.group(1))
                if 20 <= age_val <= 75:
                    age_limit = age_val
            except ValueError:
                pass

        # Target Beneficiaries
        beneficiaries: List[BeneficiaryType] = []
        for ben_name, pat in BENEFICIARY_KEYWORDS:
            if pat.search(text):
                try:
                    beneficiaries.append(BeneficiaryType(ben_name))
                except ValueError:
                    pass
        if not beneficiaries:
            beneficiaries.append(BeneficiaryType.FACULTY)

        # Min Qualifications
        qualifications: List[str] = []
        for qual_name, pat in QUALIFICATION_KEYWORDS:
            if pat.search(text):
                qualifications.append(qual_name)
        min_qual = qualifications[0] if qualifications else "Relevant Graduate/Postgraduate Degree"

        # Eligible Institutions
        institutions: List[str] = []
        for inst_name, pat in INSTITUTION_KEYWORDS:
            if pat.search(text):
                institutions.append(inst_name)
        if not institutions:
            institutions = ["Recognized Indian Universities and Research Institutes"]

        return EligibilityCriteria(
            target_beneficiaries=beneficiaries,
            min_qualification=min_qual,
            max_age_limit=age_limit,
            eligible_institutions=institutions,
            raw_eligibility_text=text[:400],
        )

    def extract_from_raw_notice(
        self,
        notice_id: str,
        title: str,
        agency: AgencyType,
        source_url: str,
        full_text: str,
        pdf_url: Optional[str] = None,
        is_ocr: bool = False,
    ) -> FundingOpportunity:
        """Parses and validates a raw notice into a FundingOpportunity Pydantic model."""
        content_hash = hashlib.sha256(f"{title}|{full_text}".encode("utf-8")).hexdigest()
        financials = self.extract_financials(full_text)
        deadlines = self.extract_dates(full_text)
        eligibility = self.extract_eligibility(full_text)

        # Domain classification heuristic fallback
        domain = ResearchDomain.INTERDISCIPLINARY
        text_lower = full_text.lower() + " " + title.lower()
        if any(k in text_lower for k in ["computer", "ai", "artificial intelligence", "data science", "software", "machine learning", "quantum"]):
            domain = ResearchDomain.COMPUTER_SCIENCE_AI
        elif any(k in text_lower for k in ["biotech", "bio", "healthcare", "medical", "genom", "pharma", "clinical"]):
            domain = ResearchDomain.BIOTECHNOLOGY_HEALTHCARE
        elif any(k in text_lower for k in ["electronics", "vlsi", "electrical", "semiconductor", "robotics", "iot"]):
            domain = ResearchDomain.ELECTRONICS_ELECTRICAL
        elif any(k in text_lower for k in ["energy", "solar", "battery", "climate", "environment", "clean energy", "ev"]):
            domain = ResearchDomain.ENERGY_ENVIRONMENT_SUSTAINABILITY
        elif any(k in text_lower for k in ["physics", "chemistry", "mathematics", "materials", "nanotechnology"]):
            domain = ResearchDomain.PHYSICAL_CHEMICAL_SCIENCES

        # Brief summary extraction
        lines = [line.strip() for line in full_text.splitlines() if len(line.strip()) > 30]
        brief = " ".join(lines[:3])[:400] if lines else f"Funding Opportunity from {agency.value}: {title}"

        ontology_tag = AcademicOntologyTag(
            domain=domain,
            thematic_thrust=title,
            target_beneficiary=eligibility.target_beneficiaries[0] if eligibility.target_beneficiaries else BeneficiaryType.FACULTY,
            confidence=0.9,
        )

        return FundingOpportunity(
            foa_id=notice_id,
            title=title,
            agency=agency,
            scheme_name=title.split(":")[0] if ":" in title else title,
            source_url=source_url,
            pdf_download_url=pdf_url,
            raw_document_hash=content_hash,
            brief_summary=brief,
            thematic_areas=[w.capitalize() for w in re.findall(r"\b[A-Za-z]{5,}\b", title)[:5]],
            ontology_tags=[ontology_tag],
            eligibility=eligibility,
            deadlines=deadlines,
            financials=financials,
            full_text_content=full_text,
            is_ocr_extracted=is_ocr,
            ingested_at=datetime.now(timezone.utc),
        )
