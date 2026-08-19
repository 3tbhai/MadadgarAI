"""Tests for Pydantic data schemas."""
import pytest
from datetime import date
from src.schemas.foa import (
    AgencyType,
    BeneficiaryType,
    Deadlines,
    EligibilityCriteria,
    FinancialCeiling,
    FundingOpportunity,
    ResearchDomain,
    AcademicOntologyTag,
)


def test_funding_opportunity_schema():
    foa = FundingOpportunity(
        foa_id="TEST-DST-01",
        title="DST Research Scheme in Quantum Systems",
        agency=AgencyType.DST,
        source_url="https://dst.gov.in/test",
        raw_document_hash="dummyhash12345",
        brief_summary="A test funding opportunity.",
        thematic_areas=["Quantum", "Physics"],
        ontology_tags=[
            AcademicOntologyTag(
                domain=ResearchDomain.PHYSICAL_CHEMICAL_SCIENCES,
                thematic_thrust="Quantum Mechanics",
                target_beneficiary=BeneficiaryType.FACULTY,
            )
        ],
        deadlines=Deadlines(
            open_date=date(2026, 1, 1),
            closing_date=date(2026, 3, 31),
            extended_closing_date=date(2026, 4, 15),
        ),
        financials=FinancialCeiling(
            max_amount_inr=5000000.0,
            institutional_overhead_pct=10.0,
        ),
        eligibility=EligibilityCriteria(
            target_beneficiaries=[BeneficiaryType.FACULTY],
            min_qualification="Ph.D.",
            max_age_limit=50,
        ),
    )

    assert foa.foa_id == "TEST-DST-01"
    assert foa.deadlines.effective_deadline == date(2026, 4, 15)
    assert foa.financials.max_amount_inr == 5000000.0
    assert foa.eligibility.max_age_limit == 50


def test_invalid_foa_id_raises_error():
    with pytest.raises(ValueError):
        FundingOpportunity(
            foa_id="",
            title="Empty ID",
            agency=AgencyType.DST,
            source_url="https://dst.gov.in",
            raw_document_hash="h123",
            brief_summary="Summary",
        )
