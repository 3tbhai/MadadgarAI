"""Database Persistence, Schema Normalizer, and JSON/CSV Exporter."""
from datetime import date
import csv
import json
import logging
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional

from src.config import CSV_EXPORT_PATH, DATABASE_PATH, JSON_EXPORT_PATH
from src.schemas.foa import FundingOpportunity

logger = logging.getLogger("MadadgaarAI.Extractor.Normalizer")


class DatasetNormalizer:
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._init_sqlite_db()

    def _init_sqlite_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS funding_opportunities (
                    foa_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    agency TEXT NOT NULL,
                    issuing_authority TEXT,
                    scheme_name TEXT,
                    source_url TEXT,
                    direct_apply_url TEXT,
                    portal_navigation_steps_json TEXT,
                    pdf_download_url TEXT,
                    raw_document_hash TEXT UNIQUE,
                    brief_summary TEXT,
                    thematic_areas_json TEXT,
                    field_of_study_json TEXT,
                    ontology_tags_json TEXT,
                    eligibility_json TEXT,
                    deadlines_json TEXT,
                    financials_json TEXT,
                    duration_months INTEGER,
                    renewal_requirements TEXT,
                    common_mistakes_json TEXT,
                    official_source_references_json TEXT,
                    last_verified_date TEXT,
                    full_text_content TEXT,
                    is_ocr_extracted INTEGER,
                    ingested_at TEXT
                )
                """
            )
            # Automatic schema migration for existing databases
            migration_columns = [
                ("direct_apply_url", "TEXT"),
                ("portal_navigation_steps_json", "TEXT"),
                ("issuing_authority", "TEXT"),
                ("field_of_study_json", "TEXT"),
                ("duration_months", "INTEGER"),
                ("renewal_requirements", "TEXT"),
                ("common_mistakes_json", "TEXT"),
                ("official_source_references_json", "TEXT"),
                ("last_verified_date", "TEXT"),
            ]
            for col_name, col_type in migration_columns:
                try:
                    cursor.execute(f"ALTER TABLE funding_opportunities ADD COLUMN {col_name} {col_type}")
                except Exception:
                    pass

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_agency ON funding_opportunities(agency);
                """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_hash ON funding_opportunities(raw_document_hash);
                """
            )
            conn.commit()

    def save_opportunity(self, foa: FundingOpportunity) -> bool:
        """Upserts a single FundingOpportunity into SQLite."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO funding_opportunities (
                        foa_id, title, agency, issuing_authority, scheme_name, source_url,
                        direct_apply_url, portal_navigation_steps_json, pdf_download_url,
                        raw_document_hash, brief_summary, thematic_areas_json, field_of_study_json,
                        ontology_tags_json, eligibility_json, deadlines_json, financials_json,
                        duration_months, renewal_requirements, common_mistakes_json,
                        official_source_references_json, last_verified_date, full_text_content,
                        is_ocr_extracted, ingested_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(foa_id) DO UPDATE SET
                        title = excluded.title,
                        issuing_authority = excluded.issuing_authority,
                        scheme_name = excluded.scheme_name,
                        brief_summary = excluded.brief_summary,
                        source_url = excluded.source_url,
                        direct_apply_url = excluded.direct_apply_url,
                        portal_navigation_steps_json = excluded.portal_navigation_steps_json,
                        thematic_areas_json = excluded.thematic_areas_json,
                        field_of_study_json = excluded.field_of_study_json,
                        deadlines_json = excluded.deadlines_json,
                        financials_json = excluded.financials_json,
                        eligibility_json = excluded.eligibility_json,
                        duration_months = excluded.duration_months,
                        renewal_requirements = excluded.renewal_requirements,
                        common_mistakes_json = excluded.common_mistakes_json,
                        official_source_references_json = excluded.official_source_references_json,
                        last_verified_date = excluded.last_verified_date,
                        full_text_content = excluded.full_text_content
                    """,
                    (
                        foa.foa_id,
                        foa.title,
                        foa.agency.value,
                        foa.issuing_authority,
                        foa.scheme_name,
                        foa.source_url,
                        foa.direct_apply_url or foa.source_url,
                        json.dumps(foa.portal_navigation_steps),
                        foa.pdf_download_url,
                        foa.raw_document_hash,
                        foa.brief_summary,
                        json.dumps(foa.thematic_areas),
                        json.dumps(foa.field_of_study),
                        json.dumps([t.model_dump() for t in foa.ontology_tags]),
                        json.dumps(foa.eligibility.model_dump()),
                        json.dumps(foa.deadlines.model_dump(), default=str),
                        json.dumps(foa.financials.model_dump()),
                        foa.duration_months,
                        foa.renewal_requirements,
                        json.dumps(foa.common_mistakes),
                        json.dumps(foa.official_source_references),
                        foa.last_verified_date.isoformat() if foa.last_verified_date else date.today().isoformat(),
                        foa.full_text_content,
                        1 if foa.is_ocr_extracted else 0,
                        foa.ingested_at.isoformat(),
                    ),
                )
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save FOA {foa.foa_id} to DB: {e}")
            return False

    def load_all_opportunities(self) -> List[FundingOpportunity]:
        """Loads all stored opportunities from SQLite."""
        opportunities: List[FundingOpportunity] = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM funding_opportunities ORDER BY ingested_at DESC")
                rows = cursor.fetchall()
                for r in rows:
                    keys = r.keys()
                    direct_apply = r["direct_apply_url"] if "direct_apply_url" in keys else r["source_url"]
                    nav_steps = json.loads(r["portal_navigation_steps_json"] or "[]") if "portal_navigation_steps_json" in keys and r["portal_navigation_steps_json"] else []
                    issuing_auth = r["issuing_authority"] if "issuing_authority" in keys else None
                    fields_study = json.loads(r["field_of_study_json"] or "[]") if "field_of_study_json" in keys and r["field_of_study_json"] else []
                    duration_m = r["duration_months"] if "duration_months" in keys else 36
                    renewal_req = r["renewal_requirements"] if "renewal_requirements" in keys else None
                    common_err = json.loads(r["common_mistakes_json"] or "[]") if "common_mistakes_json" in keys and r["common_mistakes_json"] else []
                    source_refs = json.loads(r["official_source_references_json"] or "[]") if "official_source_references_json" in keys and r["official_source_references_json"] else []
                    verified_dt = r["last_verified_date"] if "last_verified_date" in keys and r["last_verified_date"] else date.today().isoformat()

                    foa_dict = {
                        "foa_id": r["foa_id"],
                        "title": r["title"],
                        "agency": r["agency"],
                        "issuing_authority": issuing_auth,
                        "scheme_name": r["scheme_name"],
                        "source_url": r["source_url"],
                        "direct_apply_url": direct_apply or r["source_url"],
                        "portal_navigation_steps": nav_steps,
                        "pdf_download_url": r["pdf_download_url"],
                        "raw_document_hash": r["raw_document_hash"],
                        "brief_summary": r["brief_summary"],
                        "thematic_areas": json.loads(r["thematic_areas_json"] or "[]"),
                        "field_of_study": fields_study,
                        "ontology_tags": json.loads(r["ontology_tags_json"] or "[]"),
                        "eligibility": json.loads(r["eligibility_json"] or "{}"),
                        "deadlines": json.loads(r["deadlines_json"] or "{}"),
                        "financials": json.loads(r["financials_json"] or "{}"),
                        "duration_months": duration_m,
                        "renewal_requirements": renewal_req,
                        "common_mistakes": common_err,
                        "official_source_references": source_refs,
                        "last_verified_date": verified_dt,
                        "full_text_content": r["full_text_content"],
                        "is_ocr_extracted": bool(r["is_ocr_extracted"]),
                        "ingested_at": r["ingested_at"],
                    }
                    opportunities.append(FundingOpportunity.model_validate(foa_dict))
        except Exception as e:
            logger.error(f"Failed to load opportunities from DB: {e}")
        return opportunities

    def get_opportunity_by_id(self, foa_id: str) -> Optional[FundingOpportunity]:
        all_foas = self.load_all_opportunities()
        for f in all_foas:
            if f.foa_id.lower() == foa_id.lower():
                return f
        return None

    def export_to_json_and_csv(
        self,
        opportunities: Optional[List[FundingOpportunity]] = None,
        json_path: Path = JSON_EXPORT_PATH,
        csv_path: Path = CSV_EXPORT_PATH,
    ) -> Dict[str, str]:
        """Exports normalized FOAs to standard JSON and CSV files."""
        if opportunities is None:
            opportunities = self.load_all_opportunities()

        target_json = Path(json_path).resolve()
        target_csv = Path(csv_path).resolve()
        target_json.parent.mkdir(parents=True, exist_ok=True)
        target_csv.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Export JSON
            json_data = [foa.model_dump(mode="json") for foa in opportunities]
            with open(str(target_json), "w", encoding="utf-8") as jf:
                json.dump(json_data, jf, indent=2, default=str)

            # Export CSV
            with open(str(target_csv), "w", newline="", encoding="utf-8") as cf:
                writer = csv.writer(cf)
                writer.writerow([
                    "FOA ID",
                    "Title",
                    "Agency",
                    "Issuing Authority",
                    "Scheme Name",
                    "Closing Date",
                    "Extended Date",
                    "Max Budget INR",
                    "Min Qualification",
                    "Max Age",
                    "Target Beneficiary",
                    "Source URL",
                ])
                for foa in opportunities:
                    ben = foa.eligibility.target_beneficiaries[0].value if foa.eligibility.target_beneficiaries else ""
                    writer.writerow([
                        foa.foa_id,
                        foa.title,
                        foa.agency.value,
                        foa.issuing_authority or foa.agency.value,
                        foa.scheme_name or "",
                        foa.deadlines.closing_date.isoformat() if foa.deadlines.closing_date else "",
                        foa.deadlines.extended_closing_date.isoformat() if foa.deadlines.extended_closing_date else "",
                        foa.financials.max_amount_inr or "",
                        foa.eligibility.min_qualification or "",
                        foa.eligibility.max_age_limit or "",
                        ben,
                        foa.source_url,
                    ])

            logger.info(f"Exported {len(opportunities)} FOAs to {target_json} and {target_csv}")
        except Exception as e:
            logger.error(f"Failed to export opportunities to JSON/CSV: {e}")

        return {"json": str(target_json), "csv": str(target_csv)}
