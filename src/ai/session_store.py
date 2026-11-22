"""Session-Aware Conversational Memory and Application Progress Store with Privacy & Consent Controls."""
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import re
import sqlite3
from typing import Any, Dict, List, Optional
import uuid

from src.config import DATABASE_PATH

logger = logging.getLogger("MadadgaarAI.AI.SessionStore")


class ConversationalMemoryStore:
    """Manages isolated per-session profiles, chat history, and checklist completion with explicit user consent."""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    consent_given INTEGER DEFAULT 1,
                    student_profile_json TEXT DEFAULT '{}',
                    researcher_profile_json TEXT DEFAULT '{}',
                    checklist_progress_json TEXT DEFAULT '{}',
                    messages_json TEXT DEFAULT '[]',
                    updated_at TEXT
                )
                """
            )
            conn.commit()

    def get_or_create_session(
        self, session_id: Optional[str] = None, consent_given: bool = True
    ) -> Dict[str, Any]:
        sid = (session_id or "").strip() or str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_sessions WHERE session_id = ?", (sid,))
            row = cursor.fetchall()
            if row:
                r = row[0]
                return {
                    "session_id": r["session_id"],
                    "consent_given": bool(r["consent_given"]),
                    "student_profile": json.loads(r["student_profile_json"] or "{}"),
                    "researcher_profile": json.loads(r["researcher_profile_json"] or "{}"),
                    "checklist_progress": json.loads(r["checklist_progress_json"] or "{}"),
                    "messages": json.loads(r["messages_json"] or "[]"),
                    "updated_at": r["updated_at"],
                }

            now_iso = datetime.now(timezone.utc).isoformat()
            cursor.execute(
                """
                INSERT INTO user_sessions (
                    session_id, consent_given, student_profile_json,
                    researcher_profile_json, checklist_progress_json, messages_json, updated_at
                ) VALUES (?, ?, '{}', '{}', '{}', '[]', ?)
                """,
                (sid, 1 if consent_given else 0, now_iso),
            )
            conn.commit()
            return {
                "session_id": sid,
                "consent_given": consent_given,
                "student_profile": {},
                "researcher_profile": {},
                "checklist_progress": {},
                "messages": [],
                "updated_at": now_iso,
            }

    def save_session(
        self,
        session_id: str,
        consent_given: Optional[bool] = None,
        student_profile: Optional[Dict[str, Any]] = None,
        researcher_profile: Optional[Dict[str, Any]] = None,
        checklist_progress: Optional[Dict[str, Any]] = None,
        messages: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        current = self.get_or_create_session(session_id)
        effective_consent = current["consent_given"] if consent_given is None else consent_given

        if not effective_consent:
            # When user revokes consent, clear stored profile attributes
            new_stu = {}
            new_res = {}
        else:
            new_stu = {**current["student_profile"], **(student_profile or {})}
            new_res = {**current["researcher_profile"], **(researcher_profile or {})}

        new_chk = {**current["checklist_progress"], **(checklist_progress or {})}
        new_msgs = current["messages"] if messages is None else messages[-20:]
        now_iso = datetime.now(timezone.utc).isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE user_sessions SET
                    consent_given = ?,
                    student_profile_json = ?,
                    researcher_profile_json = ?,
                    checklist_progress_json = ?,
                    messages_json = ?,
                    updated_at = ?
                WHERE session_id = ?
                """,
                (
                    1 if effective_consent else 0,
                    json.dumps(new_stu),
                    json.dumps(new_res),
                    json.dumps(new_chk),
                    json.dumps(new_msgs),
                    now_iso,
                    current["session_id"],
                ),
            )
            conn.commit()

        return {
            "session_id": current["session_id"],
            "consent_given": effective_consent,
            "student_profile": new_stu,
            "researcher_profile": new_res,
            "checklist_progress": new_chk,
            "messages": new_msgs,
            "updated_at": now_iso,
        }

    def update_checklist_step(
        self, session_id: str, foa_id: str, step_key: str, completed: bool
    ) -> Dict[str, Any]:
        session = self.get_or_create_session(session_id)
        progress = session.get("checklist_progress", {})
        foa_steps: List[str] = list(progress.get(foa_id, []))
        if completed and step_key not in foa_steps:
            foa_steps.append(step_key)
        elif not completed and step_key in foa_steps:
            foa_steps.remove(step_key)
        progress[foa_id] = foa_steps
        return self.save_session(session_id=session["session_id"], checklist_progress=progress)

    def clear_session(self, session_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_sessions WHERE session_id = ?", (session_id,))
            conn.commit()
        return True

    @staticmethod
    def extract_profile_facts_from_message(text: str) -> Dict[str, Any]:
        """Extracts natural-language profile facts mentioned by a user in conversation."""
        extracted: Dict[str, Any] = {}
        low = text.lower()

        # State detection
        states = [
            "Uttar Pradesh", "Maharashtra", "Rajasthan", "Bihar", "Madhya Pradesh",
            "West Bengal", "Karnataka", "Tamil Nadu", "Gujarat", "Kerala",
            "Assam", "Meghalaya", "Manipur", "Tripura", "Sikkim", "Nagaland",
            "Arunachal Pradesh", "Mizoram", "Delhi NCR", "Punjab", "Haryana", "Odisha", "Telangana",
        ]
        for st in states:
            if st.lower() in low:
                extracted["state_domicile"] = st
                break
        if "state_domicile" not in extracted and re.search(r"\bup\b", low) and ("scholarship" in low or "dashmottar" in low or "from up" in low):
            extracted["state_domicile"] = "Uttar Pradesh"

        # Gender detection
        if any(w in low for w in ["girl", "female", "woman", "ladki", "kanya", "daughter"]):
            extracted["gender"] = "Female"
        elif any(w in low for w in ["boy", "male", "ladka", "son"]):
            extracted["gender"] = "Male"

        # Category detection
        if re.search(r"\bobc\b", low):
            extracted["social_category"] = "OBC (Non-Creamy Layer)"
        elif re.search(r"\bsc\b|scheduled\s+caste", low):
            extracted["social_category"] = "SC (Scheduled Caste)"
        elif re.search(r"\bst\b|scheduled\s+tribe", low):
            extracted["social_category"] = "ST (Scheduled Tribe)"
        elif re.search(r"\bews\b", low):
            extracted["social_category"] = "EWS (Economically Weaker Section)"
        elif re.search(r"\bgeneral\b", low):
            extracted["social_category"] = "General / Open"

        # Education level detection
        if any(w in low for w in ["b.tech", "btech", "b.e.", "engineering"]):
            extracted["education_level"] = "UG - Engineering / Technology (B.Tech/B.E.)"
        elif any(w in low for w in ["mbbs", "bds", "medical", "nursing", "b.pharm"]):
            extracted["education_level"] = "UG - Medical / Paramedical (MBBS/BDS/B.Pharm/Nursing)"
        elif any(w in low for w in ["m.tech", "m.sc", "m.a", "mba", "mca", "postgraduate", "master"]):
            extracted["education_level"] = "Postgraduate (M.Tech / M.Sc / M.Com / M.A. / MBA / MCA)"
        elif any(w in low for w in ["phd", "ph.d", "doctoral"]):
            extracted["education_level"] = "PhD / Doctoral Research"
        elif any(w in low for w in ["diploma", "polytechnic"]):
            extracted["education_level"] = "Diploma / Polytechnic"
        elif any(w in low for w in ["b.sc", "b.com", "b.a.", "bba", "bca"]):
            extracted["education_level"] = "UG - General (B.Sc / B.Com / B.A. / BBA / BCA)"

        # Income detection (e.g., "1.8 lakh", "2.5 lakhs", "Rs 150000")
        lakh_m = re.search(r"(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs|l\b)", low)
        if lakh_m:
            try:
                val = float(lakh_m.group(1))
                if 0.2 <= val <= 25.0:
                    extracted["family_annual_income_inr"] = val * 100000.0
            except ValueError:
                pass

        # Percentage detection (e.g., "88%", "91.5%")
        pct_m = re.search(r"(\d{2}(?:\.\d+)?)\s*%", low)
        if pct_m:
            try:
                pct = float(pct_m.group(1))
                if 35.0 <= pct <= 100.0:
                    extracted["academic_percentage"] = pct
            except ValueError:
                pass

        # Single girl child / PwD
        if "single girl" in low or "ekal putri" in low or "only child" in low:
            extracted["is_single_girl_child"] = True
        if "pwd" in low or "disability" in low or "divyang" in low or "differently abled" in low:
            extracted["is_differently_abled_pwd"] = True

        return extracted

