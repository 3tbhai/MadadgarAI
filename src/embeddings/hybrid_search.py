"""Hybrid Retrieval Engine combining Lexical BM25 and Dense Vectors via Reciprocal Rank Fusion (RRF)."""
import logging
from typing import Dict, List, Optional, Tuple
from rank_bm25 import BM25Okapi

from src.config import DEFAULT_TOP_K, RRF_K_CONSTANT
from src.embeddings.vector_store import VectorStore
from src.extractor.normalizer import DatasetNormalizer
from src.schemas.foa import AgencyType, FundingOpportunity, ResearchDomain

logger = logging.getLogger("MadadgaarAI.Embeddings.HybridSearch")


def tokenize_text(text: str) -> List[str]:
    """Simple alphanumeric tokenizer for BM25."""
    clean = "".join(c.lower() if c.isalnum() else " " for c in text)
    return [w for w in clean.split() if len(w) > 2]


class HybridSearchEngine:
    def __init__(self, normalizer: Optional[DatasetNormalizer] = None, vector_store: Optional[VectorStore] = None):
        self.normalizer = normalizer or DatasetNormalizer()
        self.vector_store = vector_store or VectorStore()
        self.opportunities: List[FundingOpportunity] = []
        self.bm25_index: Optional[BM25Okapi] = None
        self.corpus_tokens: List[List[str]] = []
        self.rebuild_index()

    def rebuild_index(self):
        """Indexes all current opportunities into BM25 and VectorStore."""
        self.opportunities = self.normalizer.load_all_opportunities()
        self.corpus_tokens = []

        for foa in self.opportunities:
            # Document text representation
            doc_repr = f"{foa.title} {foa.scheme_name or ''} {foa.brief_summary} {' '.join(foa.thematic_areas)} {foa.eligibility.min_qualification or ''} {foa.full_text_content or ''}"
            tokens = tokenize_text(doc_repr)
            self.corpus_tokens.append(tokens)
            self.vector_store.add_document(
                doc_id=foa.foa_id,
                text=f"{foa.title}. {foa.brief_summary}. Thematic areas: {', '.join(foa.thematic_areas)}",
                metadata={"title": foa.title, "agency": foa.agency.value},
            )

        if self.corpus_tokens:
            self.bm25_index = BM25Okapi(self.corpus_tokens)
            self.vector_store.save_index()
            logger.info(f"Hybrid index built with {len(self.opportunities)} opportunities.")

    def search_hybrid(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        agency_filter: Optional[AgencyType] = None,
        max_budget_filter: Optional[float] = None,
        domain_filter: Optional[ResearchDomain] = None,
    ) -> List[Tuple[FundingOpportunity, float, float, float]]:
        """
        Executes hybrid search via Reciprocal Rank Fusion (RRF).
        Returns list of (FundingOpportunity, rrf_score, bm25_raw_score, dense_sim_score).
        """
        if not self.opportunities:
            return []

        # 1. Lexical BM25 Ranking
        bm25_ranks: Dict[str, int] = {}
        bm25_scores: Dict[str, float] = {}
        if self.bm25_index:
            query_tokens = tokenize_text(query)
            if query_tokens:
                raw_bm25 = self.bm25_index.get_scores(query_tokens)
                sorted_bm25_indices = sorted(range(len(raw_bm25)), key=lambda i: raw_bm25[i], reverse=True)
                for rank, idx in enumerate(sorted_bm25_indices, start=1):
                    doc_id = self.opportunities[idx].foa_id
                    bm25_ranks[doc_id] = rank
                    bm25_scores[doc_id] = float(raw_bm25[idx])

        # 2. Dense Vector Ranking
        dense_results = self.vector_store.search_dense(query, top_k=len(self.opportunities))
        dense_ranks: Dict[str, int] = {}
        dense_scores: Dict[str, float] = {}
        for rank, (doc_id, sim) in enumerate(dense_results, start=1):
            dense_ranks[doc_id] = rank
            dense_scores[doc_id] = sim

        # 3. Reciprocal Rank Fusion (RRF)
        rrf_scores: Dict[str, float] = {}
        for foa in self.opportunities:
            doc_id = foa.foa_id
            
            # Apply Filters
            if agency_filter and foa.agency != agency_filter:
                continue
            if max_budget_filter and foa.financials.max_amount_inr:
                if foa.financials.max_amount_inr > max_budget_filter:
                    continue
            if domain_filter:
                domains = [t.domain for t in foa.ontology_tags]
                if domain_filter not in domains:
                    continue

            r_bm25 = bm25_ranks.get(doc_id, len(self.opportunities) + 1)
            r_dense = dense_ranks.get(doc_id, len(self.opportunities) + 1)

            # RRF Formula: sum(1 / (k + r))
            score = (1.0 / (RRF_K_CONSTANT + r_bm25)) + (1.0 / (RRF_K_CONSTANT + r_dense))
            rrf_scores[doc_id] = score

        # Sort and construct response
        sorted_foa_ids = sorted(rrf_scores.keys(), key=lambda d_id: rrf_scores[d_id], reverse=True)[:top_k]
        
        # Normalize RRF scores to [0.0, 1.0] for clear presentation
        max_possible_rrf = (2.0 / (RRF_K_CONSTANT + 1))
        results = []
        foa_map = {f.foa_id: f for f in self.opportunities}

        for d_id in sorted_foa_ids:
            foa = foa_map[d_id]
            norm_score = min(1.0, rrf_scores[d_id] / max_possible_rrf)
            b_score = bm25_scores.get(d_id, 0.0)
            d_score = dense_scores.get(d_id, 0.0)
            results.append((foa, round(norm_score, 4), round(b_score, 2), round(d_score, 4)))

        return results
