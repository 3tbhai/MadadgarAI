"""Profile-to-Grant Semantic Matching Engine with Explainable AI (XAI)."""
from datetime import date
import logging
from typing import List, Optional

from src.embeddings.hybrid_search import HybridSearchEngine
from src.embeddings.ontology import AcademicOntologyEngine
from src.matcher.compliance_checker import ComplianceChecker
from src.schemas.foa import (
    GrantMatchExplanation,
    MatchResult,
    ProfileMatchRequest,
)

logger = logging.getLogger("MadadgaarAI.Matcher.Profile")


class ProfileGrantMatcher:
    def __init__(
        self,
        hybrid_search: Optional[HybridSearchEngine] = None,
        compliance_checker: Optional[ComplianceChecker] = None,
    ):
        self.hybrid_search = hybrid_search or HybridSearchEngine()
        self.compliance_checker = compliance_checker or ComplianceChecker()
        self.ontology_engine = AcademicOntologyEngine()

    def match_profile(self, profile: ProfileMatchRequest) -> List[MatchResult]:
        """Matches researcher/student profile to top funding opportunities with 6-part explainability."""
        domains_str = " ".join([d.value for d in profile.domain_interests])
        methods_str = " ".join(profile.research_methodologies or [])
        facilities_str = " ".join(profile.available_facilities or [])
        query_text = f"{profile.research_summary} {domains_str} {methods_str} {facilities_str} {profile.user_role.value}"

        # Classify researcher profile against Indian Academic Ontology
        inferred_tags = self.ontology_engine.classify_text(query_text)
        inferred_domains = {t.domain for t in inferred_tags}
        if profile.domain_interests:
            inferred_domains.update(profile.domain_interests)

        raw_results = self.hybrid_search.search_hybrid(
            query=query_text,
            top_k=max(profile.top_k + 4, 10),
        )

        ref_today = date.today()
        match_results: List[MatchResult] = []

        for foa, rrf_score, bm25_score, dense_sim in raw_results:
            compliance = self.compliance_checker.evaluate_compliance(
                profile=profile,
                eligibility=foa.eligibility,
                foa=foa,
            )

            # Extract overlapping research keywords and thematic phrases
            stop_words = {
                "research", "project", "proposal", "using", "based", "study",
                "system", "systems", "development", "analysis", "faculty",
                "principal", "investigator", "india", "indian", "scheme",
                "grant", "support", "across", "under", "through", "their",
            }
            query_words = {
                w.strip(".,;:()[]")
                for w in query_text.lower().split()
                if len(w.strip(".,;:()[]")) >= 4 and w.strip(".,;:()[]") not in stop_words
            }
            doc_text_lower = (
                f"{foa.title} {foa.brief_summary} {' '.join(foa.thematic_areas)} "
                f"{' '.join(foa.field_of_study)} {foa.full_text_content or ''}"
            ).lower()
            doc_words = {
                w.strip(".,;:()[]")
                for w in doc_text_lower.split()
                if len(w.strip(".,;:()[]")) >= 4
            }

            overlap_words = [w.capitalize() for w in sorted(query_words.intersection(doc_words))][:6]
            thematic_overlaps = [
                area for area in foa.thematic_areas
                if any(tok in query_text.lower() for tok in area.lower().split() if len(tok) >= 3)
            ]
            combined_overlaps = list(dict.fromkeys(thematic_overlaps + overlap_words))[:6]
            if not combined_overlaps and foa.thematic_areas:
                combined_overlaps = foa.thematic_areas[:3]

            # Calculate Domain Similarity Score
            foa_domains = {t.domain for t in foa.ontology_tags}
            if foa_domains.intersection(inferred_domains):
                domain_sim = 0.95
            elif any("Interdisciplinary" in d.value for d in foa_domains):
                domain_sim = 0.80
            else:
                domain_sim = 0.60

            # Deadline awareness
            eff_deadline = foa.deadlines.effective_deadline
            proximity_days: Optional[int] = None
            deadline_status = "OPEN"
            if foa.deadlines.is_rolling:
                deadline_status = "ROLLING (OPEN YEAR-ROUND)"
            elif eff_deadline:
                proximity_days = (eff_deadline - ref_today).days
                if proximity_days < 0:
                    deadline_status = f"CLOSED ({eff_deadline.isoformat()})"
                elif proximity_days <= 30:
                    deadline_status = f"CLOSING SOON ({proximity_days} days left)"
                else:
                    deadline_status = f"OPEN (Closes {eff_deadline.isoformat()})"

            # Build 6-part Explainable Matching Object
            why_matches = (
                f"{foa.title} ({foa.agency.value}) aligns with your research profile via Hybrid BM25 + Dense Vector RRF "
                f"(score: {rrf_score:.2f}, domain similarity: {domain_sim:.0%}). "
                f"The call specifically funds work in {', '.join(foa.thematic_areas[:3])}, with a budget ceiling of "
                f"₹{(foa.financials.max_amount_inr or 0):,.0f} over {foa.duration_months or 36} months."
            )

            explanation = GrantMatchExplanation(
                why_grant_matches=why_matches,
                overlapping_interests=combined_overlaps,
                satisfied_requirements=compliance.satisfied_criteria,
                unverified_requirements=compliance.unverified_criteria,
                potential_disqualifiers=compliance.disqualifying_factors or (
                    foa.common_mistakes[:2] if foa.common_mistakes else [
                        "Missing Head of Institution Endorsement or exceeding the statutory age/budget cap."
                    ]
                ),
                actionable_improvements=compliance.improvement_suggestions,
            )

            match_results.append(
                MatchResult(
                    foa=foa,
                    relevance_score=rrf_score,
                    bm25_score=bm25_score,
                    dense_score=dense_sim,
                    domain_similarity_score=domain_sim,
                    matching_keywords=combined_overlaps,
                    compliance=compliance,
                    explanation=explanation,
                    deadline_proximity_days=proximity_days,
                    deadline_status=deadline_status,
                )
            )

        sorted_matches = sorted(
            match_results,
            key=lambda m: (m.compliance.is_compliant, m.relevance_score, m.domain_similarity_score),
            reverse=True,
        )
        return sorted_matches[: profile.top_k]
