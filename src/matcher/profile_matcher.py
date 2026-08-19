"""Profile-to-Grant Semantic Matching Engine."""
import logging
from typing import List, Optional

from src.embeddings.hybrid_search import HybridSearchEngine
from src.matcher.compliance_checker import ComplianceChecker
from src.schemas.foa import MatchResult, ProfileMatchRequest

logger = logging.getLogger("MadadgaarAI.Matcher.Profile")


class ProfileGrantMatcher:
    def __init__(
        self,
        hybrid_search: Optional[HybridSearchEngine] = None,
        compliance_checker: Optional[ComplianceChecker] = None,
    ):
        self.hybrid_search = hybrid_search or HybridSearchEngine()
        self.compliance_checker = compliance_checker or ComplianceChecker()

    def match_profile(self, profile: ProfileMatchRequest) -> List[MatchResult]:
        """Matches researcher/student profile to top funding opportunities."""
        # Synthesize query
        domains_str = " ".join([d.value for d in profile.domain_interests])
        query_text = f"{profile.research_summary} {domains_str} {profile.user_role.value}"

        raw_results = self.hybrid_search.search_hybrid(
            query=query_text,
            top_k=profile.top_k,
        )

        match_results: List[MatchResult] = []
        for foa, rrf_score, bm25_score, dense_sim in raw_results:
            compliance = self.compliance_checker.evaluate_compliance(profile, foa.eligibility)
            
            # Extract common matching words
            query_words = set(query_text.lower().split())
            doc_words = set((foa.title + " " + foa.brief_summary).lower().split())
            matching_kws = [w.capitalize() for w in list(query_words.intersection(doc_words)) if len(w) > 4][:5]

            match_results.append(
                MatchResult(
                    foa=foa,
                    relevance_score=rrf_score,
                    bm25_score=bm25_score,
                    dense_score=dense_sim,
                    matching_keywords=matching_kws,
                    compliance=compliance,
                )
            )

        return sorted(match_results, key=lambda m: (m.compliance.is_compliant, m.relevance_score), reverse=True)
