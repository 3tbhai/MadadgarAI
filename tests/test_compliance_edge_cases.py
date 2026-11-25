"""Edge-case Unit Tests for Grant Compliance Checker."""
import pytest
from datetime import date
from src.matcher.compliance_checker import ComplianceChecker
from src.schemas.foa import (
    AgencyType,
    BeneficiaryType,
    Deadlines,
    EligibilityCriteria,
    FinancialCeiling,
    FundingOpportunity,
    ProfileMatchRequest,
)

def _create_test_foa() -> FundingOpportunity:
    return FundingOpportunity(
        foa_id="UNIT-COMPLIANCE-02",
        title="Early Career Advanced Quantum Research Fellowship",
        agency=AgencyType.DST,
        source_url="https://dst.gov.in/ecr-quantum",
        raw_document_hash="compliance_hash_02",
        brief_summary="Early career research grants for doctoral degree holders under 35.",
        thematic_areas=["Quantum Computing", "Physics"],
        eligibility=EligibilityCriteria(
            target_beneficiaries=[BeneficiaryType.EARLY_CAREER],
            min_qualification="Ph.D.",
            max_age_limit=35,
        ),
        deadlines=Deadlines(closing_date=date(2027, 8, 31)),
        financials=FinancialCeiling(max_amount_inr=5000000.0),
    )

def test_applicant_exceeding_age_limit():
    checker = ComplianceChecker()
    foa = _create_test_foa()
    req = ProfileMatchRequest(
        user_role=BeneficiaryType.EARLY_CAREER,
        applicant_age=45,  # Exceeds max 35 limit
        highest_degree="Ph.D. in Physics",
        research_summary="Quantum optics and superconducting circuits",
    )
    result = checker.evaluate_compliance(req, foa.eligibility, foa=foa)
    assert result.is_compliant is False
    assert result.status == "INELIGIBLE"
    assert any("age" in r.lower() for r in result.reasons or [])

def test_applicant_compliant_qualifications():
    checker = ComplianceChecker()
    foa = _create_test_foa()
    req = ProfileMatchRequest(
        user_role=BeneficiaryType.EARLY_CAREER,
        applicant_age=31,  # Under 35
        highest_degree="Ph.D. in Quantum Information",
        research_summary="Quantum algorithms and error correction",
    )
    result = checker.evaluate_compliance(req, foa.eligibility, foa=foa)
    assert result.is_compliant is True
    assert result.status == "ELIGIBLE"

