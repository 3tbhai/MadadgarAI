"""Edge-case Unit Tests for Hybrid Retrieval Engine."""
import pytest
from src.embeddings.hybrid_search import HybridSearchEngine, tokenize_text
from src.schemas.foa import AgencyType

def test_tokenize_text_special_characters_and_empty():
    assert tokenize_text("") == []
    assert tokenize_text("   ") == []
    assert tokenize_text("!!!@@@###$$$%%%^^^") == []
    # Words <= 2 characters are filtered
    assert tokenize_text("ai ml to be or") == []
    assert tokenize_text("quantum computing artificial intelligence") == [
        "quantum", "computing", "artificial", "intelligence"
    ]

def test_search_empty_and_whitespace_query():
    engine = HybridSearchEngine()
    results = engine.search_hybrid(query="", top_k=5)
    # Empty query should return graceful empty or fallback results without exceptions
    assert isinstance(results, list)

def test_search_special_characters_no_crash():
    engine = HybridSearchEngine()
    results = engine.search_hybrid(query="!@#$%^&*()_+{}[]:;<>?,./~`", top_k=3)
    assert isinstance(results, list)

def test_search_with_strict_agency_filter():
    engine = HybridSearchEngine()
    results = engine.search_hybrid(query="research", agency_filter=AgencyType.DST, top_k=5)
    assert isinstance(results, list)
    for foa, _, _, _ in results:
        assert foa.agency == AgencyType.DST
