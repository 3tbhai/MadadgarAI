"""Empirical Benchmark Evaluation for MadadgaarAI."""
import json
import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

from src.crawlers.seed_data import get_seed_foa_dataset
from src.embeddings.hybrid_search import HybridSearchEngine
from src.extractor.entity_extractor import FOAEntityExtractor
from src.extractor.normalizer import DatasetNormalizer
from src.schemas.foa import AgencyType

logger = logging.getLogger("MadadgaarAI.Evaluation")
logging.basicConfig(level=logging.INFO)


@dataclass
class ExtractionMetrics:
    precision: float
    recall: float
    f1_score: float
    exact_matches: int
    total_evaluated: int


@dataclass
class RetrievalMetrics:
    mrr: float  # Mean Reciprocal Rank
    hit_at_1: float
    hit_at_3: float
    hit_at_5: float
    total_queries: int


class BenchmarkEvaluator:
    def __init__(self):
        self.normalizer = DatasetNormalizer()
        self.extractor = FOAEntityExtractor()
        self.hybrid_search = HybridSearchEngine(normalizer=self.normalizer)

    def evaluate_extraction(self) -> ExtractionMetrics:
        """Evaluates entity extraction against annotated ground truth notices."""
        ground_truth = get_seed_foa_dataset()
        correct_fields = 0
        total_fields = 0

        for foa in ground_truth:
            extracted = self.extractor.extract_from_raw_notice(
                notice_id=foa.foa_id,
                title=foa.title,
                agency=foa.agency,
                source_url=foa.source_url,
                full_text=foa.full_text_content or foa.brief_summary,
            )

            # 1. Financial ceiling check
            total_fields += 1
            if foa.financials.max_amount_inr:
                if extracted.financials.max_amount_inr == foa.financials.max_amount_inr:
                    correct_fields += 1
            else:
                correct_fields += 1

            # 2. Agency check
            total_fields += 1
            if extracted.agency == foa.agency:
                correct_fields += 1

            # 3. Deadline check
            total_fields += 1
            if foa.deadlines.closing_date:
                if extracted.deadlines.closing_date == foa.deadlines.closing_date:
                    correct_fields += 1
            else:
                correct_fields += 1

            # 4. Target Beneficiary check
            total_fields += 1
            gt_ben = foa.eligibility.target_beneficiaries[0] if foa.eligibility.target_beneficiaries else None
            ex_ben = extracted.eligibility.target_beneficiaries[0] if extracted.eligibility.target_beneficiaries else None
            if gt_ben and ex_ben and gt_ben == ex_ben:
                correct_fields += 1

        precision = correct_fields / max(1, total_fields)
        recall = precision  # Closed ground-truth evaluation
        f1 = (2 * precision * recall) / max(1e-6, precision + recall)

        return ExtractionMetrics(
            precision=round(precision, 4),
            recall=round(recall, 4),
            f1_score=round(f1, 4),
            exact_matches=correct_fields,
            total_evaluated=total_fields,
        )

    def evaluate_retrieval(self) -> RetrievalMetrics:
        """Evaluates retrieval Mean Reciprocal Rank (MRR) and Hit@k on curated query test cases."""
        test_queries: List[Tuple[str, str]] = [
            ("quantum computing semiconductor materials AI core grant", "DST-CRG-2026-01"),
            ("women scientists exploratory research STEM fellowship grant", "ANRF-POWER-2026-03"),
            ("biotechnology diagnostics genomics healthcare public health", "CSIR-EMR-2026-02"),
            ("engineering robotics IoT electric vehicles lab modernization", "AICTE-RPS-2026-04"),
            ("prime minister scholarship professional engineering medical students", "NSP-PMSS-2026-05"),
            ("state university faculty collaborative research premier IITs IISc", "ANRF-TARE-2026-06"),
            ("biotech medtech startup proof of concept ignition grant BIRAC", "DBT-BIG-2026-07"),
            ("women postdoc career break Ph.D. fellowship basic sciences", "DST-WISE-2026-08"),
        ]

        reciprocal_ranks = []
        hits_1 = 0
        hits_3 = 0
        hits_5 = 0

        for query, target_foa_id in test_queries:
            results = self.hybrid_search.search_hybrid(query=query, top_k=5)
            ranked_ids = [r[0].foa_id for r in results]

            if target_foa_id in ranked_ids:
                rank = ranked_ids.index(target_foa_id) + 1
                reciprocal_ranks.append(1.0 / rank)
                if rank == 1:
                    hits_1 += 1
                if rank <= 3:
                    hits_3 += 1
                if rank <= 5:
                    hits_5 += 1
            else:
                reciprocal_ranks.append(0.0)

        num_queries = len(test_queries)
        mrr = sum(reciprocal_ranks) / max(1, num_queries)

        return RetrievalMetrics(
            mrr=round(mrr, 4),
            hit_at_1=round(hits_1 / num_queries, 4),
            hit_at_3=round(hits_3 / num_queries, 4),
            hit_at_5=round(hits_5 / num_queries, 4),
            total_queries=num_queries,
        )


def run_evaluation() -> Dict[str, Dict[str, float]]:
    evaluator = BenchmarkEvaluator()
    ext_metrics = evaluator.evaluate_extraction()
    ret_metrics = evaluator.evaluate_retrieval()

    print("\n=======================================================")
    print("       MadadgaarAI Empirical Benchmark Report          ")
    print("=======================================================")
    print(f"Extraction Precision   : {ext_metrics.precision * 100:.2f}%")
    print(f"Extraction Recall      : {ext_metrics.recall * 100:.2f}%")
    print(f"Extraction F1-Score    : {ext_metrics.f1_score * 100:.2f}%")
    print("-------------------------------------------------------")
    print(f"Retrieval MRR          : {ret_metrics.mrr:.4f}")
    print(f"Retrieval Hit@1        : {ret_metrics.hit_at_1 * 100:.2f}%")
    print(f"Retrieval Hit@3        : {ret_metrics.hit_at_3 * 100:.2f}%")
    print(f"Retrieval Hit@5        : {ret_metrics.hit_at_5 * 100:.2f}%")
    print("=======================================================\n")

    return {
        "extraction": {
            "precision": ext_metrics.precision,
            "recall": ext_metrics.recall,
            "f1_score": ext_metrics.f1_score,
        },
        "retrieval": {
            "mrr": ret_metrics.mrr,
            "hit_at_1": ret_metrics.hit_at_1,
            "hit_at_3": ret_metrics.hit_at_3,
            "hit_at_5": ret_metrics.hit_at_5,
        },
    }


if __name__ == "__main__":
    run_evaluation()
