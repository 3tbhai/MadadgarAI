"""AICTE and NSP Portal Crawlers."""
import asyncio
import logging
from typing import List
import aiohttp
from bs4 import BeautifulSoup

from src.config import PORTAL_URLS
from src.crawlers.base import BasePortalCrawler, CrawledNotice
from src.schemas.foa import AgencyType

logger = logging.getLogger("MadadgaarAI.Crawlers.AICTE_NSP")


class AICTECrawler(BasePortalCrawler):
    def __init__(self):
        super().__init__(
            agency=AgencyType.AICTE,
            portal_url=PORTAL_URLS["AICTE"]
        )

    async def crawl(self) -> List[CrawledNotice]:
        notices: List[CrawledNotice] = []
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_with_retry(self.portal_url, session)
            if not html:
                return notices

            soup = BeautifulSoup(html, "html.parser")
            rows = soup.find_all(["tr", "div"], class_=lambda c: c and any(k in str(c).lower() for k in ["scheme", "item", "row"]))
            for idx, r in enumerate(rows[:10], start=1):
                link = r.find("a")
                title = link.get_text(strip=True) if link else r.get_text(strip=True)[:100]
                href = link.get("href") if link else self.portal_url
                if href and not href.startswith("http"):
                    href = f"https://www.aicte-india.org{href}"

                notice = CrawledNotice(
                    notice_id=f"AICTE-SCHEME-2026-{idx:02d}",
                    agency=self.agency,
                    title=title or f"AICTE Scheme #{idx}",
                    source_url=href,
                    raw_content=r.get_text(separator="\n", strip=True),
                )
                if not self.is_duplicate(notice.sha256_hash):
                    self.save_raw_notice(notice)
                    self.record_seen(notice.sha256_hash)
                    notices.append(notice)
        return notices


class NSPCrawler(BasePortalCrawler):
    def __init__(self):
        super().__init__(
            agency=AgencyType.NSP,
            portal_url=PORTAL_URLS["NSP"]
        )

    async def crawl(self) -> List[CrawledNotice]:
        notices: List[CrawledNotice] = []
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_with_retry(self.portal_url, session)
            if not html:
                return notices

            soup = BeautifulSoup(html, "html.parser")
            cards = soup.find_all(["div", "li"], class_=lambda c: c and any(k in str(c).lower() for k in ["scheme", "scholarship", "card"]))
            for idx, c in enumerate(cards[:10], start=1):
                link = c.find("a")
                title = link.get_text(strip=True) if link else c.get_text(strip=True)[:100]
                href = link.get("href") if link else self.portal_url

                notice = CrawledNotice(
                    notice_id=f"NSP-SCHOLARSHIP-2026-{idx:02d}",
                    agency=self.agency,
                    title=title or f"NSP Scheme #{idx}",
                    source_url=href,
                    raw_content=c.get_text(separator="\n", strip=True),
                )
                if not self.is_duplicate(notice.sha256_hash):
                    self.save_raw_notice(notice)
                    self.record_seen(notice.sha256_hash)
                    notices.append(notice)
        return notices
