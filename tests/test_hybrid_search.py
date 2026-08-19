"""Tests for Hybrid Search (BM25 + Dense RRF)."""
from src.crawlers.seed_data import get_seed_foa_dataset
from src.embeddings.hybrid_search import HybridSearchEngine
from src.embeddings.vector_store import VectorStore
from src.extractor.normalizer import DatasetNormalizer
from src.schemas.foa import AgencyType


def test_hybrid_search_rrf(tmp_path):
    db_path = tmp_path / "test_madadgaar.db"
    vec_path = tmp_path / "test_vec.json"

    normalizer = DatasetNormalizer(db_path=db_path)
    for s in get_seed_foa_dataset():
        normalizer.save_opportunity(s)

    vec_store = VectorStore(index_path=vec_path)
    engine = HybridSearchEngine(normalizer=normalizer, vector_store=vec_store)

    results = engine.search_hybrid(query="quantum computing semiconductor", top_k=3)
    assert len(results) > 0
    top_foa, rrf_score, bm25, dense = results[0]
    assert rrf_score > 0.0
    assert top_foa.foa_id == "DST-CRG-2026-01"


def test_hybrid_search_agency_filter(tmp_path):
    db_path = tmp_path / "test_madadgaar.db"
    vec_path = tmp_path / "test_vec.json"

    normalizer = DatasetNormalizer(db_path=db_path)
    for s in get_seed_foa_dataset():
        normalizer.save_opportunity(s)

    vec_store = VectorStore(index_path=vec_path)
    engine = HybridSearchEngine(normalizer=normalizer, vector_store=vec_store)

    results = engine.search_hybrid(query="scholarship", agency_filter=AgencyType.NSP, top_k=5)
    for foa, _, _, _ in results:
        assert foa.agency == AgencyType.NSP
