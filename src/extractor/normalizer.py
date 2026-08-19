"""Database Persistence, Schema Normalizer, and JSON/CSV Exporter."""
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
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS funding_opportunities (
                    foa_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    agency TEXT NOT NULL,
                    scheme_name TEXT,
                    source_url TEXT,
                    pdf_download_url TEXT,
                    raw_document_hash TEXT UNIQUE,
                    brief_summary TEXT,
                    thematic_areas_json TEXT,
                    ontology_tags_json TEXT,
                    eligibility_json TEXT,
                    deadlines_json TEXT,
                    financials_json TEXT,
                    full_text_content TEXT,
                    is_ocr_extracted INTEGER,
                    ingested_at TEXT
                )
                """
            )
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
                        foa_id, title, agency, scheme_name, source_url, pdf_download_url,
                        raw_document_hash, brief_summary, thematic_areas_json, ontology_tags_json,
                        eligibility_json, deadlines_json, financials_json, full_text_content,
                        is_ocr_extracted, ingested_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(foa_id) DO UPDATE SET
                        title = excluded.title,
                        brief_summary = excluded.brief_summary,
                        deadlines_json = excluded.deadlines_json,
                        financials_json = excluded.financials_json,
                        eligibility_json = excluded.eligibility_json,
                        full_text_content = excluded.full_text_content
                    """,
                    (
                        foa.foa_id,
                        foa.title,
                        foa.agency.value,
                        foa.scheme_name,
                        foa.source_url,
                        foa.pdf_download_url,
                        foa.raw_document_hash,
                        foa.brief_summary,
                        json.dumps(foa.thematic_areas),
                        json.dumps([t.model_dump() for t in foa.ontology_tags]),
                        json.dumps(foa.eligibility.model_dump()),
                        json.dumps(foa.deadlines.model_dump(), default=str),
                        json.dumps(foa.financials.model_dump()),
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
                    foa_dict = {
                        "foa_id": r["foa_id"],
                        "title": r["title"],
                        "agency": r["agency"],
                        "scheme_name": r["scheme_name"],
                        "source_url": r["source_url"],
                        "pdf_download_url": r["pdf_download_url"],
                        "raw_document_hash": r["raw_document_hash"],
                        "brief_summary": r["brief_summary"],
                        "thematic_areas": json.loads(r["thematic_areas_json"] or "[]"),
                        "ontology_tags": json.loads(r["ontology_tags_json"] or "[]"),
                        "eligibility": json.loads(r["eligibility_json"] or "{}"),
                        "deadlines": json.loads(r["deadlines_json"] or "{}"),
                        "financials": json.loads(r["financials_json"] or "{}"),
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

        # Export JSON
        json_data = [foa.model_dump(mode="json") for foa in opportunities]
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(json_data, jf, indent=2, default=str)

        # Export CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as cf:
            writer = csv.writer(cf)
            writer.writerow([
                "FOA ID",
                "Title",
                "Agency",
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
                    foa.scheme_name or "",
                    foa.deadlines.closing_date.isoformat() if foa.deadlines.closing_date else "",
                    foa.deadlines.extended_closing_date.isoformat() if foa.deadlines.extended_closing_date else "",
                    foa.financials.max_amount_inr or "",
                    foa.eligibility.min_qualification or "",
                    foa.eligibility.max_age_limit or "",
                    ben,
                    foa.source_url,
                ])

        logger.info(f"Exported {len(opportunities)} FOAs to {json_path} and {csv_path}")
        return {"json": str(json_path), "csv": str(csv_path)}
