"""Base Crawler module for MadadgaarAI."""
import asyncio
import hashlib
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import aiohttp
import requests
from bs4 import BeautifulSoup

from src.config import RAW_DATA_DIR
from src.schemas.foa import AgencyType

logger = logging.getLogger("MadadgaarAI.Crawlers")
logging.basicConfig(level=logging.INFO)


@dataclass
class CrawledNotice:
    notice_id: str
    agency: AgencyType
    title: str
    source_url: str
    raw_content: str
    pdf_url: Optional[str] = None
    pdf_bytes: Optional[bytes] = None
    sha256_hash: str = ""
    is_scanned_pdf: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    crawled_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.sha256_hash:
            payload = f"{self.title}|{self.raw_content}".encode("utf-8")
            if self.pdf_bytes:
                payload += self.pdf_bytes
            self.sha256_hash = hashlib.sha256(payload).hexdigest()


class BasePortalCrawler(ABC):
    def __init__(self, agency: AgencyType, portal_url: str, request_timeout: int = 15):
        self.agency = agency
        self.portal_url = portal_url
        self.timeout = request_timeout
        self.seen_hashes: Set[str] = self._load_seen_hashes()
        self.headers = {
            "User-Agent": "MadadgaarAI-Academic-Crawler/1.0 (+https://github.com/3tbhai/MadadgarAI; anjisht@jklu.edu.in)"
        }

    def _get_hash_checkpoint_path(self) -> Path:
        return RAW_DATA_DIR / f"{self.agency.value.lower().replace('/', '_')}_hashes.json"

    def _load_seen_hashes(self) -> Set[str]:
        path = self._get_hash_checkpoint_path()
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return set(json.load(f))
            except Exception as e:
                logger.warning(f"Failed to load hash checkpoint: {e}")
        return set()

    def _save_seen_hashes(self):
        path = self._get_hash_checkpoint_path()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(list(self.seen_hashes), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save hash checkpoint: {e}")

    def is_duplicate(self, doc_hash: str) -> bool:
        return doc_hash in self.seen_hashes

    def record_seen(self, doc_hash: str):
        self.seen_hashes.add(doc_hash)
        self._save_seen_hashes()

    async def fetch_with_retry(
        self,
        url: str,
        session: aiohttp.ClientSession,
        max_retries: int = 3,
        backoff_factor: float = 1.5,
    ) -> Optional[str]:
        for attempt in range(1, max_retries + 1):
            try:
                async with session.get(
                    url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        return await response.text()
                    logger.warning(
                        f"Attempt {attempt}: Received status {response.status} from {url}"
                    )
            except Exception as exc:
                logger.warning(f"Attempt {attempt} failed for {url}: {exc}")
                if attempt == max_retries:
                    logger.error(f"All {max_retries} retries exhausted for {url}")
                    return None
                await asyncio.sleep(backoff_factor**attempt)
        return None

    def save_raw_notice(self, notice: CrawledNotice) -> Path:
        agency_dir = RAW_DATA_DIR / self.agency.value.lower().replace("/", "_")
        agency_dir.mkdir(parents=True, exist_ok=True)
        safe_id = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in notice.notice_id)
        filepath = agency_dir / f"{safe_id}_{notice.sha256_hash[:8]}.json"
        
        notice_data = asdict(notice)
        # Avoid storing raw binary bytes in json
        if "pdf_bytes" in notice_data:
            del notice_data["pdf_bytes"]
            
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(notice_data, f, indent=2, ensure_ascii=False)
            
        if notice.pdf_bytes:
            pdf_path = agency_dir / f"{safe_id}_{notice.sha256_hash[:8]}.pdf"
            with open(pdf_path, "wb") as pf:
                pf.write(notice.pdf_bytes)

        return filepath

    @abstractmethod
    async def crawl(self) -> List[CrawledNotice]:
        """Crawl target portal and return a list of extracted notices."""
        pass
