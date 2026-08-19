"""Anusandhan National Research Foundation (ANRF / SERB) Crawler."""
import asyncio
import logging
from typing import List
import aiohttp
from bs4 import BeautifulSoup

from src.config import PORTAL_URLS
from src.crawlers.base import BasePortalCrawler, CrawledNotice
from src.schemas.foa import AgencyType

logger = logging.getLogger("MadadgaarAI.Crawlers.ANRF")


class ANRFCrawler(BasePortalCrawler):
    def __init__(self):
        super().__init__(
            agency=AgencyType.ANRF,
            portal_url=PORTAL_URLS["ANRF"]
        )

    async def crawl(self) -> List[CrawledNotice]:
        notices: List[CrawledNotice] = []
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_with_retry(self.portal_url, session)
            if not html:
                logger.info("ANRF live portal unreachable; continuing.")
                return notices

            soup = BeautifulSoup(html, "html.parser")
            scheme_cards = soup.find_all(["div", "article", "a"], class_=lambda c: c and any(k in str(c).lower() for k in ["scheme", "grant", "card", "news"]))

            for idx, card in enumerate(scheme_cards[:10], start=1):
                link = card if card.name == "a" else card.find("a")
                title = card.get_text(strip=True)[:120]
                href = link.get("href") if link else self.portal_url
                if href and not href.startswith("http"):
                    href = f"https://anrfonline.in/{href.lstrip('/')}"

                notice_id = f"ANRF-SCHEME-2026-{idx:02d}"
                raw_text = card.get_text(separator="\n", strip=True)
                notice = CrawledNotice(
                    notice_id=notice_id,
                    agency=self.agency,
                    title=title or f"ANRF Funding Scheme #{idx}",
                    source_url=href,
                    raw_content=raw_text,
                    metadata={"source": "ANRF Online"},
                )
                if not self.is_duplicate(notice.sha256_hash):
                    self.save_raw_notice(notice)
                    self.record_seen(notice.sha256_hash)
                    notices.append(notice)

        return notices
