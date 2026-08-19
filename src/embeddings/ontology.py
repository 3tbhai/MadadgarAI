"""Hierarchical Indian Academic and Research Ontology."""
from dataclasses import dataclass
from typing import Dict, List, Optional
from src.schemas.foa import BeneficiaryType, ResearchDomain, AcademicOntologyTag


@dataclass
class OntologyNode:
    domain: ResearchDomain
    thematic_thrust: str
    keywords: List[str]
    target_beneficiaries: List[BeneficiaryType]


INDIAN_ACADEMIC_ONTOLOGY: List[OntologyNode] = [
    OntologyNode(
        domain=ResearchDomain.COMPUTER_SCIENCE_AI,
        thematic_thrust="AI, High-Performance Computing and Data Engineering",
        keywords=[
            "artificial intelligence", "machine learning", "deep learning", "nlp",
            "computer vision", "llm", "quantum computing", "cybersecurity", "cloud computing"
        ],
        target_beneficiaries=[BeneficiaryType.FACULTY, BeneficiaryType.PHD_POSTDOC, BeneficiaryType.STARTUP_INDUSTRY],
    ),
    OntologyNode(
        domain=ResearchDomain.ELECTRONICS_ELECTRICAL,
        thematic_thrust="VLSI Design, Embedded Systems, IoT and Robotics",
        keywords=[
            "semiconductor", "vlsi", "fpga", "robotics", "iot", "internet of things",
            "embedded systems", "electric vehicle", "battery management", "power electronics"
        ],
        target_beneficiaries=[BeneficiaryType.FACULTY, BeneficiaryType.STARTUP_INDUSTRY],
    ),
    OntologyNode(
        domain=ResearchDomain.BIOTECHNOLOGY_HEALTHCARE,
        thematic_thrust="Translational Healthcare, Genomics & Medical Devices",
        keywords=[
            "biotechnology", "genomics", "bioinformatics", "medical devices", "diagnostics",
            "therapeutics", "drug discovery", "vaccine", "biomedical", "agritech"
        ],
        target_beneficiaries=[BeneficiaryType.FACULTY, BeneficiaryType.WOMEN_SCIENTIST, BeneficiaryType.STARTUP_INDUSTRY],
    ),
    OntologyNode(
        domain=ResearchDomain.PHYSICAL_CHEMICAL_SCIENCES,
        thematic_thrust="Advanced Materials, Quantum Systems & Chemical Synthesis",
        keywords=[
            "condensed matter", "polymers", "nanotechnology", "chemical catalysis", "quantum physics",
            "spectroscopy", "optics", "theoretical physics", "synthetic chemistry"
        ],
        target_beneficiaries=[BeneficiaryType.FACULTY, BeneficiaryType.PHD_POSTDOC],
    ),
    OntologyNode(
        domain=ResearchDomain.ENERGY_ENVIRONMENT_SUSTAINABILITY,
        thematic_thrust="Clean Energy, Decarbonization & Climate Resilience",
        keywords=[
            "solar energy", "green hydrogen", "fuel cells", "carbon capture", "water purification",
            "waste to wealth", "circular economy", "climate change", "pollution control"
        ],
        target_beneficiaries=[BeneficiaryType.FACULTY, BeneficiaryType.STARTUP_INDUSTRY, BeneficiaryType.INSTITUTE],
    ),
    OntologyNode(
        domain=ResearchDomain.INTERDISCIPLINARY,
        thematic_thrust="Inclusive STEM Fellowships, Women Scientists & Higher Education",
        keywords=[
            "women scientists", "gender diversity", "fellowship", "scholarship", "capacity building",
            "ug pg students", "faculty mobility", "interdisciplinary"
        ],
        target_beneficiaries=[BeneficiaryType.WOMEN_SCIENTIST, BeneficiaryType.UG_PG_STUDENT, BeneficiaryType.EARLY_CAREER],
    ),
]


class AcademicOntologyEngine:
    def __init__(self, ontology: List[OntologyNode] = INDIAN_ACADEMIC_ONTOLOGY):
        self.ontology = ontology

    def classify_text(self, text: str) -> List[AcademicOntologyTag]:
        """Maps input text to matching ontology categories with confidence scores."""
        text_lower = text.lower()
        matched_tags: List[AcademicOntologyTag] = []

        for node in self.ontology:
            hit_count = sum(1 for kw in node.keywords if kw in text_lower)
            if hit_count > 0:
                confidence = min(0.99, 0.4 + (hit_count * 0.15))
                matched_tags.append(
                    AcademicOntologyTag(
                        domain=node.domain,
                        thematic_thrust=node.thematic_thrust,
                        target_beneficiary=node.target_beneficiaries[0],
                        confidence=round(confidence, 2),
                    )
                )

        if not matched_tags:
            matched_tags.append(
                AcademicOntologyTag(
                    domain=ResearchDomain.INTERDISCIPLINARY,
                    thematic_thrust="General Scientific & Technological Research",
                    target_beneficiary=BeneficiaryType.FACULTY,
                    confidence=0.5,
                )
            )

        return sorted(matched_tags, key=lambda t: t.confidence, reverse=True)
