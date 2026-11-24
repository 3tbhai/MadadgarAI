"""Resume / CV Parser & Semantic Opportunity Matching Engine."""
import io
import logging
import re
from typing import List, Optional
import zipfile
from pydantic import BaseModel, Field
from rank_bm25 import BM25Okapi

from src.crawlers.pipeline import LiveOpportunityStore
from src.embeddings.embedder import TextEmbedder
from src.embeddings.hybrid_search import tokenize_text
from src.parser.pdf_parser import PDFLayoutParser
from src.schemas.opportunity import LiveOpportunity

logger = logging.getLogger("MadadgaarAI.Matcher.Resume")

SKILL_CATALOG = [
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "Go", "Rust", "SQL", "R", "MATLAB",
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP", "LLM", "Generative AI",
    "Computer Vision", "PyTorch", "TensorFlow", "Scikit-learn", "Data Science", "Data Analytics",
    "React", "Next.js", "Node.js", "FastAPI", "Django", "Flask", "Spring Boot", "GraphQL", "REST API",
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Linux", "Git", "CI/CD", "Distributed Systems",
    "Cybersecurity", "Blockchain", "Robotics", "ROS", "Embedded Systems", "IoT", "FPGA", "VLSI",
    "Semiconductor", "Aerospace", "Mechanical Design", "CAD", "SolidWorks", "ANSYS", "Signal Processing",
    "Biotechnology", "Bioinformatics", "Genomics", "Proteomics", "Molecular Biology", "Clinical Research",
    "Public Health", "Pharmacology", "Biomedical", "CRISPR", "Cell Culture",
    "Quantum Computing", "Physics", "Chemistry", "Mathematics", "Statistics", "Climate Science",
    "Renewable Energy", "Finance", "Accounting", "Economics", "Marketing", "Product Management",
    "UI/UX", "Figma", "Public Policy", "Research Writing", "LaTeX", "Publications",
]


class ResumeMatchItem(BaseModel):
    opportunity: LiveOpportunity
    fit_score: float = Field(ge=0.0, le=100.0)
    matched_skills: List[str] = Field(default_factory=list)
    missing_prerequisites: List[str] = Field(default_factory=list)
    match_summary: str


class ResumeMatchResponse(BaseModel):
    extraction_method: str
    detected_degree: str
    detected_domains: List[str] = Field(default_factory=list)
    detected_skills: List[str] = Field(default_factory=list)
    total_evaluated: int = 0
    matches: List[ResumeMatchItem] = Field(default_factory=list)


class ResumeOpportunityMatcher:
    """Extracts skills/degree/domains from a CV or PDF resume and semantically ranks live opportunities."""

    def __init__(self, live_store: Optional[LiveOpportunityStore] = None, embedder: Optional[TextEmbedder] = None):
        self.live_store = live_store or LiveOpportunityStore()
        self.embedder = embedder or TextEmbedder()
        self.pdf_parser = PDFLayoutParser()

    def _extract_text(
        self,
        raw_text: Optional[str] = None,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None,
    ) -> tuple[str, str]:
        text = (raw_text or "").strip()
        method = "Direct Pasted Resume Text"

        if file_bytes:
            fname = (filename or "").lower()
            if fname.endswith(".pdf") or file_bytes[:4] == b"%PDF":
                parsed = self.pdf_parser.parse_pdf(file_bytes)
                text = (parsed.raw_text or "").strip() or text
                method = f"PDF Layout Parser ({parsed.num_pages} page{'s' if parsed.num_pages != 1 else ''})"
            elif fname.endswith(".docx"):
                try:
                    with zipfile.ZipFile(io.BytesIO(file_bytes)) as zf:
                        xml_data = zf.read("word/document.xml").decode("utf-8", errors="ignore")
                        cleaned = re.sub(r"<[^>]+>", " ", xml_data)
                        text = " ".join(cleaned.split()) or text
                        method = "DOCX XML Extractor"
                except Exception as exc:
                    logger.warning(f"DOCX extraction failed: {exc}")
            else:
                text = file_bytes.decode("utf-8", errors="ignore").strip() or text
                method = "Plain Text File Reader"

        return text, method

    @staticmethod
    def _detect_degree(low: str) -> str:
        if any(k in low for k in ["ph.d", "phd", "doctor of philosophy", "postdoc", "assistant professor", "faculty", "principal investigator"]):
            return "PhD / Faculty"
        if any(k in low for k in ["m.tech", "mtech", "m.sc", "msc", "master of", "mba", "mca", "postgraduate", "ms in "]):
            return "Postgraduate"
        if any(k in low for k in ["b.tech", "btech", "b.e.", "bachelor", "undergraduate", "b.sc", "bsc", "bca", "bba", "computer science student", "intern"]):
            return "Undergraduate"
        return "All Levels"

    @staticmethod
    def _detect_domains(low: str) -> List[str]:
        domain_rules = [
            ("Computer Science & AI", ["python", "machine learning", "artificial intelligence", "software", "react", "fastapi", "deep learning", "nlp", "llm", "computer science", "data science", "cloud", "aws", "backend", "frontend"]),
            ("Engineering", ["mechanical", "electrical", "electronics", "civil", "robotics", "embedded", "vlsi", "semiconductor", "aerospace", "cad", "hardware", "iot"]),
            ("Healthcare & Biotech", ["biotech", "biomedical", "bioinformatics", "genomics", "clinical", "medical", "pharma", "molecular biology", "public health", "healthcare"]),
            ("Business & Marketing", ["finance", "marketing", "economics", "mba", "product management", "sales", "accounting", "operations", "business"]),
            ("Science & Research", ["physics", "chemistry", "mathematics", "quantum", "climate", "renewable energy", "astronomy", "publications", "research"]),
            ("Design, Policy & Arts", ["ui/ux", "figma", "design", "public policy", "law", "journalism", "humanities", "graphic"]),
        ]
        hits = [dom for dom, kws in domain_rules if any(k in low for k in kws)]
        return hits or ["General"]

    @staticmethod
    def _detect_skills(text: str) -> List[str]:
        low = text.lower()
        found: List[str] = []
        for skill in SKILL_CATALOG:
            pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
            if re.search(pattern, low):
                found.append(skill)
        return found

    def match_resume(
        self,
        raw_text: Optional[str] = None,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None,
        category: Optional[str] = None,
        top_k: int = 10,
    ) -> ResumeMatchResponse:
        text, method = self._extract_text(raw_text=raw_text, file_bytes=file_bytes, filename=filename)
        if not text:
            return ResumeMatchResponse(
                extraction_method=method,
                detected_degree="All Levels",
                detected_domains=[],
                detected_skills=[],
                total_evaluated=0,
                matches=[],
            )

        low = text.lower()
        degree = self._detect_degree(low)
        domains = self._detect_domains(low)
        skills = self._detect_skills(text)

        opps = self.live_store.load_all(exclude_expired=True)
        if category and category.lower() != "all":
            opps = [o for o in opps if o.category.value.lower() == category.lower()]

        if not opps:
            return ResumeMatchResponse(
                extraction_method=method,
                detected_degree=degree,
                detected_domains=domains,
                detected_skills=skills,
                total_evaluated=0,
                matches=[],
            )

        query_summary = " ".join(skills + domains + [degree]) + " " + text[:800]
        q_tokens = tokenize_text(query_summary)
        corpus_texts = [
            f"{o.title} {o.organization} {o.category.value} {o.domain} {o.degree_level} {o.eligibility} {o.summary} {' '.join(o.tags)}"
            for o in opps
        ]
        corpus_toks = [tokenize_text(t) for t in corpus_texts]
        bm25 = BM25Okapi(corpus_toks) if any(corpus_toks) else None
        bm25_scores = bm25.get_scores(q_tokens) if (bm25 and q_tokens) else [0.0] * len(opps)
        max_bm25 = max([float(s) for s in bm25_scores], default=1.0) or 1.0

        q_vec = self.embedder.embed_text(query_summary)
        doc_vecs = self.embedder.embed_batch(corpus_texts)

        ranked: List[ResumeMatchItem] = []
        for idx, opp in enumerate(opps):
            doc_text = corpus_texts[idx]
            doc_low = doc_text.lower()
            cos_sim = max(0.0, TextEmbedder.cosine_similarity(q_vec, doc_vecs[idx]))
            norm_bm25 = max(0.0, float(bm25_scores[idx]) / max_bm25)
            base_rrf = min(1.0, 0.55 * norm_bm25 + 0.45 * cos_sim)
            sem_score = self.embedder.rerank_score(
                query=" ".join(skills[:10] + domains),
                candidate_text=doc_text,
                base_rrf_score=base_rrf,
            )

            # Domain & Degree alignment bonuses / gap flags
            domain_match = opp.domain in domains
            missing: List[str] = []
            degree_bonus = 0.0
            if opp.degree_level == "All Levels" or opp.degree_level == degree or degree == "All Levels":
                degree_bonus = 0.08
            elif opp.degree_level == "PhD / Faculty" and degree == "Undergraduate":
                missing.append("Listing targets PhD / Faculty level; resume appears Undergraduate")
                degree_bonus = -0.10
            elif opp.degree_level == "Postgraduate" and degree == "Undergraduate":
                missing.append("Listing prefers Postgraduate enrollment")
                degree_bonus = -0.04

            # Matched skills & opportunity-required skills not in CV
            matched_sk = [s for s in skills if re.search(r"(?<![a-z0-9])" + re.escape(s.lower()) + r"(?![a-z0-9])", doc_low)]
            opp_skills = [s for s in SKILL_CATALOG if re.search(r"(?<![a-z0-9])" + re.escape(s.lower()) + r"(?![a-z0-9])", doc_low)]
            for req_sk in opp_skills:
                if req_sk not in matched_sk and len(missing) < 3:
                    missing.append(f"Consider highlighting '{req_sk}' on your resume")

            if domain_match and not matched_sk:
                matched_sk = [opp.domain]

            final_pct = round(
                min(99.0, max(12.0, (sem_score * 78.0) + (14.0 if domain_match else 0.0) + (len(matched_sk) * 4.5) + (degree_bonus * 100.0))),
                1,
            )
            summary_line = (
                f"Matches your {degree} background in {opp.domain}"
                + (f" via {', '.join(matched_sk[:3])}." if matched_sk else ".")
            )

            ranked.append(
                ResumeMatchItem(
                    opportunity=opp,
                    fit_score=final_pct,
                    matched_skills=matched_sk[:6],
                    missing_prerequisites=missing[:3],
                    match_summary=summary_line,
                )
            )

        ranked.sort(key=lambda r: r.fit_score, reverse=True)
        return ResumeMatchResponse(
            extraction_method=method,
            detected_degree=degree,
            detected_domains=domains,
            detected_skills=skills[:18],
            total_evaluated=len(opps),
            matches=ranked[: max(1, min(top_k, 25))],
        )
