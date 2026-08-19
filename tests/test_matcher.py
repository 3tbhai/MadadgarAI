"""Tests for Profile Matching, Compliance Verification, Calendar, and Proposal Drafter."""
from src.crawlers.seed_data import get_seed_foa_dataset
from src.extractor.normalizer import DatasetNormalizer
from src.matcher.calendar_sync import CalendarSyncGenerator
from src.matcher.compliance_checker import ComplianceChecker
from src.matcher.profile_matcher import ProfileGrantMatcher
from src.matcher.proposal_drafter import ProposalDrafter
from src.schemas.foa import BeneficiaryType, ProfileMatchRequest


def test_compliance_checker():
    seeds = get_seed_foa_dataset()
    anrf_power = next(s for s in seeds if s.foa_id == "ANRF-POWER-2026-03")

    checker = ComplianceChecker()

    # Female researcher profile
    req_female = ProfileMatchRequest(
        user_role=BeneficiaryType.WOMEN_SCIENTIST,
        applicant_age=42,
        highest_degree="Ph.D. in Biotechnology",
        research_summary="Genomics and biomedical therapeutics",
    )
    res_female = checker.evaluate_compliance(req_female, anrf_power.eligibility)
    assert res_female.is_compliant is True
    assert res_female.status == "ELIGIBLE"

    # Profile exceeding age limit
    req_overage = ProfileMatchRequest(
        user_role=BeneficiaryType.WOMEN_SCIENTIST,
        applicant_age=62,
        highest_degree="Ph.D.",
        research_summary="Biomedical study",
    )
    res_overage = checker.evaluate_compliance(req_overage, anrf_power.eligibility)
    assert res_overage.is_compliant is False
    assert res_overage.status == "INELIGIBLE"


def test_calendar_sync():
    seeds = get_seed_foa_dataset()
    foa = seeds[0]
    gen = CalendarSyncGenerator()
    ics_bytes = gen.generate_ics_for_foa(foa)

    assert b"BEGIN:VCALENDAR" in ics_bytes
    assert b"BEGIN:VEVENT" in ics_bytes
    assert foa.foa_id.encode() in ics_bytes


def test_proposal_drafter():
    seeds = get_seed_foa_dataset()
    foa = seeds[0]
    drafter = ProposalDrafter()
    skeleton = drafter.draft_proposal_skeleton(foa, pi_name="Dr. Tester")

    assert skeleton.foa_id == foa.foa_id
    assert len(skeleton.sections) >= 5
    assert "Non-Recurring (Capital Equipment)" in skeleton.suggested_budget_breakdown
    assert len(skeleton.compliance_checklist) > 0
