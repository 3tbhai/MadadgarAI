"""Tests for Profile Matching, Compliance Verification, Calendar, and Proposal Drafter."""
from datetime import date
from src.matcher.calendar_sync import CalendarSyncGenerator
from src.matcher.compliance_checker import ComplianceChecker
from src.matcher.proposal_drafter import ProposalDrafter
from src.schemas.foa import (
    AgencyType,
    BeneficiaryType,
    Deadlines,
    EligibilityCriteria,
    FinancialCeiling,
    FundingOpportunity,
    ProfileMatchRequest,
)


def _sample_grant() -> FundingOpportunity:
    return FundingOpportunity(
        foa_id="UNIT-GRANT-01",
        title="Exploratory Women in STEM Research Grant",
        agency=AgencyType.ANRF,
        source_url="https://example.org/grant-01",
        raw_document_hash="unit_hash_01",
        brief_summary="Funding for women scientists conducting exploratory STEM research.",
        thematic_areas=["Biomedical Devices", "AI"],
        eligibility=EligibilityCriteria(
            target_beneficiaries=[BeneficiaryType.WOMEN_SCIENTIST],
            min_qualification="Ph.D. in Science or Engineering",
            max_age_limit=55,
        ),
        deadlines=Deadlines(closing_date=date(2027, 10, 31)),
        financials=FinancialCeiling(max_amount_inr=3000000.0, institutional_overhead_pct=10.0),
    )


def test_compliance_checker():
    foa = _sample_grant()
    checker = ComplianceChecker()

    req_ok = ProfileMatchRequest(
        user_role=BeneficiaryType.WOMEN_SCIENTIST,
        applicant_age=42,
        highest_degree="Ph.D. in Biotechnology",
        research_summary="Genomics and biomedical therapeutics",
    )
    res_ok = checker.evaluate_compliance(req_ok, foa.eligibility, foa=foa)
    assert res_ok.is_compliant is True
    assert res_ok.status == "ELIGIBLE"

    req_overage = ProfileMatchRequest(
        user_role=BeneficiaryType.WOMEN_SCIENTIST,
        applicant_age=62,
        highest_degree="Ph.D.",
        research_summary="Biomedical study",
    )
    res_overage = checker.evaluate_compliance(req_overage, foa.eligibility, foa=foa)
    assert res_overage.is_compliant is False
    assert res_overage.status == "INELIGIBLE"


def test_calendar_sync():
    foa = _sample_grant()
    gen = CalendarSyncGenerator()
    ics_bytes = gen.generate_ics_for_foa(foa)
    assert b"BEGIN:VCALENDAR" in ics_bytes
    assert b"BEGIN:VEVENT" in ics_bytes
    assert foa.foa_id.encode() in ics_bytes


def test_proposal_drafter():
    foa = _sample_grant()
    drafter = ProposalDrafter()
    skeleton = drafter.draft_proposal_skeleton(foa, pi_name="Dr. Tester")
    assert skeleton.foa_id == foa.foa_id
    assert len(skeleton.sections) == 11
    assert "Non-Recurring (Capital Equipment)" in skeleton.suggested_budget_breakdown
    assert len(skeleton.compliance_checklist) > 0
