"""Real-Time Opportunity Pipeline Orchestrator, Deduplicator, TTL Cache & Filter-Accurate Store."""
import asyncio
from datetime import date, datetime, timedelta, timezone
import json
import logging
from pathlib import Path
import re
import sqlite3
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse
import httpx
from rank_bm25 import BM25Okapi

from src.config import DATABASE_PATH, PROCESSED_DATA_DIR
from src.crawlers.link_verifier import AsyncLinkVerifier, DEFAULT_HEADERS, canonicalize_url, is_specific_listing_url
from src.crawlers.live_scrapers import BaseLiveScraper, build_live_scrapers, make_opportunity_id
from src.embeddings.embedder import TextEmbedder
from src.embeddings.hybrid_search import tokenize_text
from src.extractor.normalizer import DatasetNormalizer
from src.schemas.foa import (
    AgencyType,
    BeneficiaryType,
    Deadlines,
    EligibilityCriteria,
    FinancialCeiling,
    FundingOpportunity,
)
from src.schemas.opportunity import (
    LiveOpportunity,
    LiveRefreshReport,
    OpportunityCategory,
    OpportunityListResponse,
    ScrapeSourceTelemetry,
)

logger = logging.getLogger("MadadgaarAI.Crawlers.Pipeline")

DEFAULT_CACHE_TTL_HOURS = 6


def _title_tokens(title: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]{3,}", title.lower())}


def _jaccard_similarity(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / float(len(a | b))


class LiveOpportunityStore:
    """SQLite-backed store with TTL caching, live filtering, and hybrid search over verified opportunities."""

    def __init__(self, db_path: Path = DATABASE_PATH, cache_ttl_hours: int = DEFAULT_CACHE_TTL_HOURS):
        self.db_path = Path(db_path)
        self.cache_ttl_hours = cache_ttl_hours
        self.embedder = TextEmbedder()
        self._init_db()

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA journal_mode=WAL;")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS live_opportunities (
                    id TEXT PRIMARY KEY,
                    canonical_url TEXT UNIQUE,
                    title TEXT NOT NULL,
                    organization TEXT NOT NULL,
                    category TEXT NOT NULL,
                    source_type TEXT DEFAULT 'Government',
                    domain TEXT NOT NULL,
                    eligibility TEXT NOT NULL,
                    degree_level TEXT NOT NULL,
                    deadline TEXT,
                    is_rolling INTEGER DEFAULT 0,
                    stipend_or_amount TEXT,
                    funding_type TEXT,
                    source_url TEXT NOT NULL,
                    source_domain TEXT NOT NULL,
                    scraped_at TEXT NOT NULL,
                    last_verified_at TEXT NOT NULL,
                    http_status INTEGER NOT NULL,
                    summary TEXT NOT NULL,
                    tags_json TEXT DEFAULT '[]',
                    location TEXT
                )
                """
            )
            try:
                cur.execute("ALTER TABLE live_opportunities ADD COLUMN source_type TEXT DEFAULT 'Government'")
            except Exception:
                pass
            cur.execute("CREATE INDEX IF NOT EXISTS idx_live_cat ON live_opportunities(category);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_live_stype ON live_opportunities(source_type);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_live_dom ON live_opportunities(domain);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_live_deadline ON live_opportunities(deadline);")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS scrape_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def get_last_refreshed_at(self) -> Optional[datetime]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT value FROM scrape_meta WHERE key = 'last_refreshed_at'")
            row = cur.fetchone()
            if row and row[0]:
                try:
                    return datetime.fromisoformat(row[0])
                except ValueError:
                    return None
        return None

    def get_last_source_errors(self) -> List[str]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT value FROM scrape_meta WHERE key = 'last_source_errors'")
            row = cur.fetchone()
            if row and row[0]:
                try:
                    return json.loads(row[0])
                except Exception:
                    return []
        return []

    def is_cache_fresh(self) -> bool:
        last_ts = self.get_last_refreshed_at()
        if not last_ts:
            return False
        age = datetime.now(timezone.utc) - last_ts
        return age < timedelta(hours=self.cache_ttl_hours) and self.count() > 0

    def count(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM live_opportunities")
            return int(cur.fetchone()[0])

    def replace_all(self, opportunities: List[LiveOpportunity], source_errors: List[str]):
        """Replaces stored opportunities with the latest verified live set and updates TTL metadata."""
        now_iso = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM live_opportunities")
            for opp in opportunities:
                canon = canonicalize_url(str(opp.source_url))
                cur.execute(
                    """
                    INSERT OR REPLACE INTO live_opportunities (
                        id, canonical_url, title, organization, category, source_type, domain,
                        eligibility, degree_level, deadline, is_rolling, stipend_or_amount,
                        funding_type, source_url, source_domain, scraped_at, last_verified_at,
                        http_status, summary, tags_json, location
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        opp.id,
                        canon,
                        opp.title,
                        opp.organization,
                        opp.category.value,
                        opp.source_type,
                        opp.domain,
                        opp.eligibility,
                        opp.degree_level,
                        opp.deadline.isoformat() if opp.deadline else None,
                        1 if opp.is_rolling else 0,
                        opp.stipend_or_amount,
                        opp.funding_type,
                        str(opp.source_url),
                        opp.source_domain,
                        opp.scraped_at.isoformat(),
                        opp.last_verified_at.isoformat(),
                        opp.http_status,
                        opp.summary,
                        json.dumps(opp.tags),
                        opp.location,
                    ),
                )
            cur.execute(
                "INSERT OR REPLACE INTO scrape_meta (key, value) VALUES ('last_refreshed_at', ?)",
                (now_iso,),
            )
            cur.execute(
                "INSERT OR REPLACE INTO scrape_meta (key, value) VALUES ('last_source_errors', ?)",
                (json.dumps(source_errors),),
            )
            conn.commit()

        try:
            export_path = PROCESSED_DATA_DIR / "live_opportunities.json"
            export_path.parent.mkdir(parents=True, exist_ok=True)
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump([o.model_dump(mode="json") for o in opportunities], f, indent=2, default=str)
        except Exception as exc:
            logger.warning(f"Failed writing live JSON export: {exc}")

    def load_all(self, exclude_expired: bool = True) -> List[LiveOpportunity]:
        items: List[LiveOpportunity] = []
        today = date.today()
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM live_opportunities ORDER BY scraped_at DESC")
            for r in cur.fetchall():
                try:
                    keys = r.keys()
                    stype = r["source_type"] if "source_type" in keys and r["source_type"] else "Government"
                    opp = LiveOpportunity(
                        id=r["id"],
                        title=r["title"],
                        organization=r["organization"],
                        category=OpportunityCategory(r["category"]),
                        source_type=stype,
                        domain=r["domain"],
                        eligibility=r["eligibility"],
                        degree_level=r["degree_level"],
                        deadline=date.fromisoformat(r["deadline"]) if r["deadline"] else None,
                        is_rolling=bool(r["is_rolling"]),
                        stipend_or_amount=r["stipend_or_amount"] or "See Official Listing",
                        funding_type=r["funding_type"] or "Merit / Competitive",
                        source_url=r["source_url"],
                        source_domain=r["source_domain"],
                        scraped_at=datetime.fromisoformat(r["scraped_at"]),
                        last_verified_at=datetime.fromisoformat(r["last_verified_at"]),
                        http_status=int(r["http_status"]),
                        summary=r["summary"],
                        tags=json.loads(r["tags_json"] or "[]"),
                        location=r["location"],
                    )
                    if exclude_expired and opp.deadline and opp.deadline < today:
                        continue
                    items.append(opp)
                except Exception as exc:
                    logger.debug(f"Skipping malformed row {r['id']}: {exc}")
        return items

    def query(
        self,
        category: Optional[str] = None,
        source_type: Optional[str] = None,
        domain: Optional[str] = None,
        degree_level: Optional[str] = None,
        funding_type: Optional[str] = None,
        deadline_window: Optional[str] = None,
        q: Optional[str] = None,
        sort: str = "deadline_asc",
        limit: int = 120,
    ) -> OpportunityListResponse:
        """Dynamically filters and ranks the live dataset based on all user-selected filters."""
        all_items = self.load_all(exclude_expired=True)
        total_in_store = len(all_items)
        today = date.today()

        facets = {
            "categories": sorted({o.category.value for o in all_items}),
            "source_types": sorted({o.source_type for o in all_items}),
            "domains": sorted({o.domain for o in all_items}),
            "degree_levels": sorted({o.degree_level for o in all_items}),
            "funding_types": sorted({o.funding_type for o in all_items}),
            "source_domains": sorted({o.source_domain for o in all_items}),
        }

        filtered: List[LiveOpportunity] = []
        for opp in all_items:
            if category and category.lower() != "all" and opp.category.value.lower() != category.lower():
                continue
            if source_type and source_type.lower() != "all" and opp.source_type.lower() != source_type.lower():
                continue
            if domain and domain.lower() != "all" and opp.domain.lower() != domain.lower():
                continue
            if degree_level and degree_level.lower() != "all":
                if opp.degree_level.lower() != degree_level.lower() and opp.degree_level != "All Levels":
                    continue
            if funding_type and funding_type.lower() != "all" and opp.funding_type.lower() != funding_type.lower():
                continue
            if deadline_window and deadline_window.lower() != "all":
                dw = deadline_window.lower()
                days = (opp.deadline - today).days if opp.deadline else None
                if dw == "rolling":
                    if not opp.is_rolling and opp.deadline is not None:
                        continue
                elif dw == "urgent_14d":
                    if days is None or days > 14:
                        continue
                elif dw == "30d":
                    if days is None or days > 30:
                        continue
                elif dw == "90d":
                    if days is None or days > 90:
                        continue
            filtered.append(opp)

        if q and q.strip() and filtered:
            q_clean = q.strip()
            q_low = q_clean.lower()
            q_tokens = tokenize_text(q_clean)

            corpus_texts = [
                f"{o.title} {o.organization} {o.category.value} {o.source_type} {o.domain} {o.eligibility} {o.stipend_or_amount} {o.summary} {' '.join(o.tags)} {o.location or ''}"
                for o in filtered
            ]
            corpus_toks = [tokenize_text(t) for t in corpus_texts]
            bm25 = BM25Okapi(corpus_toks) if any(corpus_toks) else None
            bm25_scores = bm25.get_scores(q_tokens) if (bm25 and q_tokens) else [0.0] * len(filtered)

            q_vec = self.embedder.embed_text(q_clean)
            doc_vecs = self.embedder.embed_batch(corpus_texts)
            dense_scores = [TextEmbedder.cosine_similarity(q_vec, dv) for dv in doc_vecs]

            scored: List[Tuple[LiveOpportunity, float]] = []
            for idx, opp in enumerate(filtered):
                text_low = corpus_texts[idx].lower()
                exact_hit = q_low in text_low
                token_hits = sum(1 for tok in q_tokens if tok in text_low)
                if exact_hit or token_hits > 0 or bm25_scores[idx] > 0.2 or dense_scores[idx] > 0.28:
                    combined = (2.0 if exact_hit else 0.0) + float(bm25_scores[idx]) + (dense_scores[idx] * 3.0) + (token_hits * 0.5)
                    scored.append((opp, combined))

            scored.sort(key=lambda x: x[1], reverse=True)
            filtered = [o for o, _ in scored]
        else:
            if sort == "deadline_asc":
                filtered.sort(
                    key=lambda o: (
                        0 if o.deadline is not None else 1,
                        o.deadline if o.deadline is not None else date(2099, 12, 31),
                        o.title.lower(),
                    )
                )
            elif sort == "recent_desc":
                filtered.sort(key=lambda o: o.scraped_at, reverse=True)
            elif sort == "title_asc":
                filtered.sort(key=lambda o: o.title.lower())

        last_ts = self.get_last_refreshed_at()
        age_mins = int((datetime.now(timezone.utc) - last_ts).total_seconds() // 60) if last_ts else None

        return OpportunityListResponse(
            items=filtered[:limit],
            total_matching=len(filtered),
            total_in_store=total_in_store,
            last_refreshed_at=last_ts,
            cache_age_minutes=age_mins,
            cache_ttl_hours=self.cache_ttl_hours,
            source_errors=self.get_last_source_errors(),
            facets=facets,
        )


def live_opportunity_to_foa(opp: LiveOpportunity) -> FundingOpportunity:
    """Projects a verified LiveOpportunity into FundingOpportunity for RAG / calendar / search compatibility."""
    cat_agency = AgencyType.OTHER
    org_low = opp.organization.lower()
    if "birac" in org_low or "dbt" in org_low:
        cat_agency = AgencyType.DBT
    elif "dst" in org_low:
        cat_agency = AgencyType.DST
    elif "anrf" in org_low or "serb" in org_low:
        cat_agency = AgencyType.ANRF
    elif "csir" in org_low:
        cat_agency = AgencyType.CSIR
    elif "aicte" in org_low:
        cat_agency = AgencyType.AICTE
    elif "nsp" in org_low:
        cat_agency = AgencyType.NSP
    elif "ugc" in org_low:
        cat_agency = AgencyType.UGC

    ben = (
        BeneficiaryType.FACULTY
        if opp.category == OpportunityCategory.FUNDING
        else BeneficiaryType.UG_PG_STUDENT
    )

    return FundingOpportunity(
        foa_id=opp.id,
        title=opp.title,
        agency=cat_agency,
        issuing_authority=opp.organization,
        scheme_name=opp.category.value,
        source_url=str(opp.source_url),
        direct_apply_url=str(opp.source_url),
        portal_navigation_steps=[
            f"1. Open the verified official listing at {opp.source_url}.",
            f"2. Review eligibility requirements: {opp.eligibility}.",
            "3. Prepare required documents and submit directly before the deadline.",
        ],
        raw_document_hash=opp.id,
        brief_summary=opp.summary,
        thematic_areas=[opp.category.value, opp.source_type, opp.domain] + opp.tags[:3],
        field_of_study=[opp.domain],
        eligibility=EligibilityCriteria(
            target_beneficiaries=[ben],
            min_qualification=opp.degree_level,
            raw_eligibility_text=opp.eligibility,
        ),
        deadlines=Deadlines(
            closing_date=opp.deadline,
            is_rolling=opp.is_rolling,
            raw_deadline_text=opp.deadline.isoformat() if opp.deadline else "Rolling / Ongoing",
        ),
        financials=FinancialCeiling(
            raw_budget_text=opp.stipend_or_amount,
        ),
        last_verified_date=opp.last_verified_at.date(),
        full_text_content=f"{opp.title}\nOrganization: {opp.organization}\nSource Type: {opp.source_type}\nEligibility: {opp.eligibility}\n{opp.summary}",
        ingested_at=opp.scraped_at,
    )


class LivePipelineOrchestrator:
    """Coordinates live scraping, expiration filtering, deduplication, Anti-404 link checking, and persistence."""

    def __init__(
        self,
        store: Optional[LiveOpportunityStore] = None,
        normalizer: Optional[DatasetNormalizer] = None,
        scrapers: Optional[List[BaseLiveScraper]] = None,
        link_verifier: Optional[AsyncLinkVerifier] = None,
    ):
        self.store = store or LiveOpportunityStore()
        self.normalizer = normalizer or DatasetNormalizer()
        self.scrapers = scrapers or build_live_scrapers()
        self.link_verifier = link_verifier or AsyncLinkVerifier(concurrency=16, timeout_seconds=7.0)
        self._refresh_lock = asyncio.Lock()

    async def refresh_live_data(self, force: bool = False) -> LiveRefreshReport:
        if not force and self.store.is_cache_fresh():
            existing = self.store.load_all(exclude_expired=True)
            cat_counts: Dict[str, int] = {}
            for o in existing:
                cat_counts[o.category.value] = cat_counts.get(o.category.value, 0) + 1
            return LiveRefreshReport(
                refreshed_at=self.store.get_last_refreshed_at() or datetime.now(timezone.utc),
                total_live_opportunities=len(existing),
                cache_ttl_hours=self.store.cache_ttl_hours,
                from_cache=True,
                source_errors=self.store.get_last_source_errors(),
                category_counts=cat_counts,
            )

        async with self._refresh_lock:
            return await self._run_pipeline()

    async def _run_pipeline(self) -> LiveRefreshReport:
        today = date.today()
        all_candidates: List[Tuple[str, Dict[str, Any]]] = []
        telemetry_map: Dict[str, ScrapeSourceTelemetry] = {}
        source_errors: List[str] = []

        async with httpx.AsyncClient(verify=False, headers=DEFAULT_HEADERS) as client:
            async def _run_one(scraper: BaseLiveScraper):
                t0 = time.perf_counter()
                tel = ScrapeSourceTelemetry(
                    source_name=scraper.source_name,
                    category=scraper.default_category.value,
                )
                try:
                    raw_items = await scraper.fetch_raw(client)
                    tel.fetched_raw = len(raw_items)
                    for item in raw_items:
                        all_candidates.append((scraper.source_name, item))
                except Exception as exc:
                    err_msg = f"{scraper.source_name}: {type(exc).__name__} — {str(exc)[:120]}"
                    tel.error = err_msg
                    source_errors.append(err_msg)
                    logger.warning(f"Live scrape failed for {err_msg}")
                finally:
                    tel.duration_ms = int((time.perf_counter() - t0) * 1000)
                    telemetry_map[scraper.source_name] = tel

            await asyncio.gather(*(_run_one(s) for s in self.scrapers))

        deduped: List[Tuple[str, Dict[str, Any], str]] = []
        seen_urls = set()
        seen_title_sets: List[set] = []
        total_expired = 0
        total_dups = 0
        total_broken = 0

        for src_name, item in all_candidates:
            tel = telemetry_map[src_name]
            dl: Optional[date] = item.get("deadline")
            if dl and dl < today:
                tel.expired_filtered += 1
                total_expired += 1
                continue

            raw_url = str(item.get("source_url") or "").strip()
            if not is_specific_listing_url(raw_url):
                tel.broken_links_discarded += 1
                total_broken += 1
                continue

            canon = canonicalize_url(raw_url)
            if canon in seen_urls:
                tel.duplicates_removed += 1
                total_dups += 1
                continue

            t_set = _title_tokens(item.get("title", ""))
            if any(_jaccard_similarity(t_set, existing_set) >= 0.85 for existing_set in seen_title_sets):
                tel.duplicates_removed += 1
                total_dups += 1
                continue

            seen_urls.add(canon)
            seen_title_sets.append(t_set)
            deduped.append((src_name, item, canon))

        urls_to_verify = [item["source_url"] for _, item, _ in deduped]
        link_results = await self.link_verifier.verify_batch(urls_to_verify)

        verified_opportunities: List[LiveOpportunity] = []
        now_utc = datetime.now(timezone.utc)

        for src_name, item, canon in deduped:
            tel = telemetry_map[src_name]
            raw_url = item["source_url"]
            is_ok, status_code, final_url, verified_ts = link_results.get(
                raw_url, (False, 0, raw_url, now_utc)
            )
            if not is_ok:
                tel.broken_links_discarded += 1
                total_broken += 1
                continue

            final_canon = canonicalize_url(final_url) or canon
            src_domain = urlparse(final_canon).netloc.lower().replace("www.", "")
            opp_id = make_opportunity_id(final_canon, item["title"])

            try:
                opp = LiveOpportunity(
                    id=opp_id,
                    title=item["title"],
                    organization=item["organization"],
                    category=item["category"],
                    source_type=item.get("source_type") or "Government",
                    domain=item.get("domain") or "General",
                    eligibility=item.get("eligibility") or "See Official Listing",
                    degree_level=item.get("degree_level") or "All Levels",
                    deadline=item.get("deadline"),
                    is_rolling=bool(item.get("is_rolling", item.get("deadline") is None)),
                    stipend_or_amount=item.get("stipend_or_amount") or "See Official Listing",
                    funding_type=item.get("funding_type") or "Merit / Competitive",
                    source_url=final_url if is_specific_listing_url(final_url) else raw_url,
                    source_domain=src_domain,
                    scraped_at=now_utc,
                    last_verified_at=verified_ts,
                    http_status=status_code,
                    summary=item["summary"],
                    tags=list(dict.fromkeys([t for t in item.get("tags", []) if t]))[:6],
                    location=item.get("location"),
                )
                verified_opportunities.append(opp)
                tel.verified_saved += 1
            except Exception as exc:
                logger.debug(f"Schema validation rejected item from {src_name}: {exc}")

        self.store.replace_all(verified_opportunities, source_errors)

        try:
            with sqlite3.connect(self.normalizer.db_path) as conn:
                conn.execute("DELETE FROM funding_opportunities")
                conn.commit()
            for opp in verified_opportunities:
                self.normalizer.save_opportunity(live_opportunity_to_foa(opp))
            self.normalizer.export_to_json_and_csv()
        except Exception as exc:
            logger.warning(f"Normalizer sync warning: {exc}")

        cat_counts: Dict[str, int] = {}
        for o in verified_opportunities:
            cat_counts[o.category.value] = cat_counts.get(o.category.value, 0) + 1

        logger.info(
            f"Live pipeline completed: {len(verified_opportunities)} verified | "
            f"{total_expired} expired | {total_broken} broken links | {total_dups} duplicates"
        )

        return LiveRefreshReport(
            refreshed_at=now_utc,
            total_live_opportunities=len(verified_opportunities),
            newly_verified=len(verified_opportunities),
            expired_filtered=total_expired,
            broken_links_discarded=total_broken,
            duplicates_removed=total_dups,
            cache_ttl_hours=self.store.cache_ttl_hours,
            from_cache=False,
            sources=list(telemetry_map.values()),
            source_errors=source_errors,
            category_counts=cat_counts,
        )
