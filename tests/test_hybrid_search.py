"""Tests for Hybrid Search (BM25 + Dense RRF) using isolated test fixtures."""
from datetime import date
from src.embeddings.hybrid_search import HybridSearchEngine
from src.embeddings.vector_store import VectorStore
from src.extractor.normalizer import DatasetNormalizer
from src.schemas.foa import (
    AgencyType,
    Deadlines,
    EligibilityCriteria,
    FinancialCeiling,
    FundingOpportunity,
)


def _sample_foas():
    return [
        FundingOpportunity(
            foa_id="TEST-QUANTUM-01",
            title="Quantum Computing and Semiconductor Materials Grant",
            agency=AgencyType.DST,
            source_url="https://example.org/quantum-grant",
            raw_document_hash="hash_q_1",
            brief_summary="Research funding for quantum computing and semiconductor materials.",
            thematic_areas=["Quantum Computing", "Semiconductor Materials"],
            deadlines=Deadlines(closing_date=date(2027, 6, 30)),
            financials=FinancialCeiling(max_amount_inr=5000000.0),
            eligibility=EligibilityCriteria(),
        ),
        FundingOpportunity(
            foa_id="TEST-SCHOL-02",
            title="National Undergraduate Engineering Scholarship",
            agency=AgencyType.NSP,
            source_url="https://example.org/ug-scholarship",
            raw_document_hash="hash_s_2",
            brief_summary="Merit scholarship for undergraduate engineering students.",
            thematic_areas=["Scholarship", "Engineering"],
            deadlines=Deadlines(closing_date=date(2027, 8, 15)),
            financials=FinancialCeiling(max_amount_inr=100000.0),
            eligibility=EligibilityCriteria(),
        ),
        FundingOpportunity(
            foa_id="TEST-BIO-03",
            title="Clinical Genomics and Healthcare Innovation Fellowship",
            agency=AgencyType.CSIR,
            source_url="https://example.org/bio-fellowship",
            raw_document_hash="hash_b_3",
            brief_summary="Fellowship for translational healthcare diagnostics and molecular biology.",
            thematic_areas=["Biotechnology", "Healthcare"],
            deadlines=Deadlines(closing_date=date(2027, 9, 20)),
            financials=FinancialCeiling(max_amount_inr=2500000.0),
            eligibility=EligibilityCriteria(),
        ),
    ]


def test_hybrid_search_rrf(tmp_path):
    db_path = tmp_path / "test_madadgaar.db"
    vec_path = tmp_path / "test_vec.json"

    normalizer = DatasetNormalizer(db_path=db_path)
    for s in _sample_foas():
        normalizer.save_opportunity(s)

    vec_store = VectorStore(index_path=vec_path)
    engine = HybridSearchEngine(normalizer=normalizer, vector_store=vec_store)

    results = engine.search_hybrid(query="quantum computing semiconductor", top_k=2)
    assert len(results) > 0
    top_foa, rrf_score, bm25, dense = results[0]
    assert rrf_score > 0.0
    assert top_foa.foa_id == "TEST-QUANTUM-01"


def test_hybrid_search_agency_filter(tmp_path):
    db_path = tmp_path / "test_madadgaar.db"
    vec_path = tmp_path / "test_vec.json"

    normalizer = DatasetNormalizer(db_path=db_path)
    for s in _sample_foas():
        normalizer.save_opportunity(s)

    vec_store = VectorStore(index_path=vec_path)
    engine = HybridSearchEngine(normalizer=normalizer, vector_store=vec_store)

    results = engine.search_hybrid(query="scholarship", agency_filter=AgencyType.NSP, top_k=5)
    assert len(results) == 1
    assert results[0][0].agency == AgencyType.NSP
