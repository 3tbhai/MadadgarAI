"""Strategy/Registry Pattern for Role-Based User Modes (Student, Researcher, Educator)."""
from enum import Enum
from typing import Dict, List
from pydantic import BaseModel, Field


class UserMode(str, Enum):
    STUDENT = "student"
    RESEARCHER = "researcher"
    EDUCATOR = "educator"


class ModeConfig(BaseModel):
    mode: UserMode
    display_name: str
    short_label: str
    badge_bg: str
    badge_text: str
    description: str
    chunk_size_tokens: int = Field(default=800, ge=200, le=2000)
    chunk_overlap_tokens: int = Field(default=150, ge=20, le=500)
    retrieval_top_k: int = Field(default=5, ge=1, le=15)
    citation_format: str = "[Source: Document Name, Page/Section]"
    system_prompt: str


class UserModeRegistry:
    """
    Central Strategy Registry for User Modes.
    Adding a new mode only requires registering a ModeConfig without modifying core RAG pipelines.
    """

    _registry: Dict[UserMode, ModeConfig] = {}

    @classmethod
    def register(cls, config: ModeConfig) -> None:
        cls._registry[config.mode] = config

    @classmethod
    def get(cls, mode: str | UserMode) -> ModeConfig:
        try:
            key = mode if isinstance(mode, UserMode) else UserMode(str(mode).strip().lower())
        except ValueError:
            key = UserMode.STUDENT
        return cls._registry[key]

    @classmethod
    def list_all(cls) -> List[ModeConfig]:
        return list(cls._registry.values())


# Register built-in modes cleanly via Strategy Pattern
UserModeRegistry.register(
    ModeConfig(
        mode=UserMode.STUDENT,
        display_name="Student Mode",
        short_label="Student",
        badge_bg="#ffcc00",
        badge_text="#18181b",
        description="Step-by-step conceptual explanations, prerequisite breakdowns, exam-focused summaries, and strict inline citations.",
        chunk_size_tokens=800,
        chunk_overlap_tokens=150,
        retrieval_top_k=5,
        system_prompt=(
            "You are Saral AI in Student Mode — a patient, structured academic tutor.\n"
            "PEDAGOGICAL GUIDELINES:\n"
            "1. Break down complex ideas into clear, step-by-step conceptual explanations.\n"
            "2. Highlight key prerequisites, definitions, formulas (using LaTeX $...$ / $$...$$), and exam-ready takeaways.\n"
            "3. STRICT GROUNDING: Answer ONLY using the provided Retrieved Context Chunks from the student's private library.\n"
            "4. Attach inline citations immediately after every factual claim using exact format: [Source: <Document Name>, Page <N> / <Section>].\n"
            "5. If the uploaded documents do not contain enough evidence to answer the question, explicitly state that the uploaded materials do not cover this topic rather than guessing or hallucinating."
        ),
    )
)

UserModeRegistry.register(
    ModeConfig(
        mode=UserMode.RESEARCHER,
        display_name="Researcher Mode",
        short_label="Researcher",
        badge_bg="#0055ff",
        badge_text="#ffffff",
        description="Technical methodology synthesis, equation/ablation comparisons, literature gap analysis, and dense citation tracing.",
        chunk_size_tokens=900,
        chunk_overlap_tokens=180,
        retrieval_top_k=7,
        system_prompt=(
            "You are Saral AI in Researcher Mode — a rigorous scientific research assistant.\n"
            "RESEARCH GUIDELINES:\n"
            "1. Synthesize methodologies, experimental setups, quantitative metrics, mathematical formulations (in LaTeX), and limitations.\n"
            "2. Compare findings across retrieved chunks and surface open gaps or assumptions explicitly.\n"
            "3. STRICT GROUNDING: Ground every claim strictly in the provided Retrieved Context Chunks.\n"
            "4. Cite every claim inline as [Source: <Document Name>, Page <N> / <Section>].\n"
            "5. If the evidence in the uploaded corpus is insufficient, state so clearly and specify what section/data is missing."
        ),
    )
)

UserModeRegistry.register(
    ModeConfig(
        mode=UserMode.EDUCATOR,
        display_name="Educator Mode",
        short_label="Educator",
        badge_bg="#138808",
        badge_text="#ffffff",
        description="Lecture outlines, worked examples, rubric-ready quiz questions, and common student misconception checks.",
        chunk_size_tokens=800,
        chunk_overlap_tokens=150,
        retrieval_top_k=6,
        system_prompt=(
            "You are Saral AI in Educator Mode — an instructional design & curriculum assistant.\n"
            "INSTRUCTIONAL GUIDELINES:\n"
            "1. Organize responses into teachable modules: Learning Objectives, Core Explanation, Worked Example, and Quick Check Questions.\n"
            "2. Flag common student misconceptions and render equations cleanly in LaTeX.\n"
            "3. STRICT GROUNDING: Base all instructional content strictly on the Retrieved Context Chunks.\n"
            "4. Include inline citations [Source: <Document Name>, Page <N> / <Section>] for traceability.\n"
            "5. Explicitly state if the uploaded syllabus/documents lack sufficient detail for the requested topic."
        ),
    )
)
