"""Council of Scientific and Industrial Research (CSIR) Crawler."""
import asyncio
import logging
from typing import List
import aiohttp
from bs4 import BeautifulSoup

from src.config import PORTAL_URLS
from src.crawlers.base import BasePortalCrawler, CrawledNotice
from src.schemas.foa import AgencyType

logger = logging.getLogger("MadadgaarAI.Crawlers.CSIR")


class CSIRCrawler(BasePortalCrawler):
    def __init__(self):
        super().__init__(
            agency=AgencyType.CSIR,
            portal_url=PORTAL_URLS["CSIR"]
        )

    async def crawl(self) -> List[CrawledNotice]:
        notices: List[CrawledNotice] = []
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_with_retry(self.portal_url, session)
            if not html:
                logger.info("CSIR live portal unreachable; continuing.")
                return notices

            soup = BeautifulSoup(html, "html.parser")
            items = soup.find_all(["li", "tr", "div"], class_=lambda c: c and any(k in str(c).lower() for k in ["scheme", "research", "view-content", "item"]))

            for idx, item in enumerate(items[:10], start=1):
                link = item.find("a")
                title = link.get_text(strip=True) if link else item.get_text(strip=True)[:120]
                href = link.get("href") if link else self.portal_url
                if href and not href.startswith("http"):
                    href = f"https://csir.res.in/{href.lstrip('/')}"

                notice_id = f"CSIR-EMR-2026-{idx:02d}"
                raw_text = item.get_text(separator="\n", strip=True)
                notice = CrawledNotice(
                    notice_id=notice_id,
                    agency=self.agency,
                    title=title or f"CSIR Research Grant #{idx}",
                    source_url=href,
                    raw_content=raw_text,
                )
                if not self.is_duplicate(notice.sha256_hash):
                    self.save_raw_notice(notice)
                    self.record_seen(notice.sha256_hash)
                    notices.append(notice)

        return notices
