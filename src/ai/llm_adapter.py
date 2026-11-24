"""Optional Multi-Provider LLM Synthesis Adapter (Gemini / OpenAI / Ollama) with Strict RAG Grounding."""
import logging
import os
from typing import Any, Dict, List, Optional, Tuple
import httpx

logger = logging.getLogger("MadadgaarAI.AI.LLM")


class LLMSynthesisAdapter:
    """
    Optional LLM synthesis layer for Saral Samjhauti RAG.
    Activates automatically if GEMINI_API_KEY, OPENAI_API_KEY, or OLLAMA_BASE_URL is configured.
    Returns None gracefully when unconfigured or unreachable so deterministic bilingual RAG handles synthesis.
    """

    def __init__(self, timeout_seconds: float = 12.0):
        self.timeout_seconds = timeout_seconds

    @property
    def gemini_api_key(self) -> str:
        return (os.getenv("GEMINI_API_KEY") or "").strip()

    @property
    def openai_api_key(self) -> str:
        return (os.getenv("OPENAI_API_KEY") or "").strip()

    @property
    def ollama_base_url(self) -> str:
        return (os.getenv("OLLAMA_BASE_URL") or "").strip().rstrip("/")

    @property
    def active_backend(self) -> str:
        if self.gemini_api_key:
            model = os.getenv("MADADGAAR_GEMINI_MODEL", "gemini-2.0-flash")
            return f"Gemini ({model})"
        if self.openai_api_key:
            model = os.getenv("MADADGAAR_OPENAI_MODEL", "gpt-4o-mini")
            return f"OpenAI ({model})"
        if self.ollama_base_url:
            model = os.getenv("MADADGAAR_OLLAMA_MODEL", "llama3.2")
            return f"Ollama ({model})"
        return "Deterministic Grounded RAG (Offline)"

    @property
    def is_enabled(self) -> bool:
        return bool(self.gemini_api_key or self.openai_api_key or self.ollama_base_url)

    def build_grounded_prompt(
        self,
        query: str,
        lang: str,
        retrieved: List[Tuple[Dict[str, Any], float]],
        student_profile: Dict[str, Any],
    ) -> str:
        context_blocks: List[str] = []
        for idx, (item, score) in enumerate(retrieved[:4], start=1):
            summary = item["hinglish_summary"] if lang == "hinglish" else item["en_summary"]
            context_blocks.append(
                f"[{idx}] {item['title']} | Authority: {item['authority']} | URL: {item['official_url']}\n"
                f"Facts: {summary[:480]}"
            )
        profile_txt = ", ".join(f"{k}={v}" for k, v in (student_profile or {}).items() if v) or "None provided"
        lang_instruction = (
            "Respond in clear, friendly Hinglish (Hindi + English) using simple bullet points."
            if lang == "hinglish"
            else "Respond in clear, concise English using crisp bullet points."
        )
        return (
            "You are MadadgaarAI (Saral Samjhauti), an authoritative assistant for Indian scholarships, internships, and research grants.\n"
            f"{lang_instruction}\n"
            "STRICT GROUNDING RULES:\n"
            "1. Only state facts, deadlines, stipends, and URLs present in the Verified Sources below.\n"
            "2. Cite source numbers inline like [1], [2]. Never invent URLs or financial figures.\n"
            "3. Keep the answer concise (max 180 words) and actionable.\n\n"
            f"User Profile Context: {profile_txt}\n\n"
            "Verified Sources:\n"
            + "\n\n".join(context_blocks)
            + f"\n\nUser Question: {query}\nAnswer:"
        )

    def synthesize_grounded(
        self,
        query: str,
        lang: str,
        retrieved: List[Tuple[Dict[str, Any], float]],
        student_profile: Dict[str, Any],
    ) -> Optional[str]:
        """Attempts LLM synthesis using the configured provider; returns None to fall back safely."""
        if not self.is_enabled or not retrieved:
            return None

        prompt = self.build_grounded_prompt(query, lang, retrieved, student_profile)
        try:
            if self.gemini_api_key:
                model = os.getenv("MADADGAAR_GEMINI_MODEL", "gemini-2.0-flash")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.2, "maxOutputTokens": 420},
                }
                resp = httpx.post(url, json=payload, timeout=self.timeout_seconds)
                resp.raise_for_status()
                cands = resp.json().get("candidates") or []
                if cands:
                    parts = (cands[0].get("content") or {}).get("parts") or []
                    text = "".join(p.get("text", "") for p in parts).strip()
                    if text:
                        return text

            elif self.openai_api_key:
                base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
                model = os.getenv("MADADGAAR_OPENAI_MODEL", "gpt-4o-mini")
                resp = httpx.post(
                    f"{base}/chat/completions",
                    headers={"Authorization": f"Bearer {self.openai_api_key}"},
                    json={
                        "model": model,
                        "temperature": 0.2,
                        "max_tokens": 420,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                    timeout=self.timeout_seconds,
                )
                resp.raise_for_status()
                choices = resp.json().get("choices") or []
                if choices:
                    text = ((choices[0].get("message") or {}).get("content") or "").strip()
                    if text:
                        return text

            elif self.ollama_base_url:
                model = os.getenv("MADADGAAR_OLLAMA_MODEL", "llama3.2")
                resp = httpx.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={"model": model, "prompt": prompt, "stream": False},
                    timeout=self.timeout_seconds,
                )
                resp.raise_for_status()
                text = (resp.json().get("response") or "").strip()
                if text:
                    return text
        except Exception as exc:
            logger.warning(f"Optional LLM synthesis fallback triggered ({self.active_backend}): {exc}")
        return None
