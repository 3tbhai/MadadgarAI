"""Department of Science & Technology (DST) Portal Crawler."""
import asyncio
import logging
from typing import List
import aiohttp
from bs4 import BeautifulSoup

from src.config import PORTAL_URLS
from src.crawlers.base import BasePortalCrawler, CrawledNotice
from src.schemas.foa import AgencyType

logger = logging.getLogger("MadadgaarAI.Crawlers.DST")


class DSTCrawler(BasePortalCrawler):
    def __init__(self):
        super().__init__(
            agency=AgencyType.DST,
            portal_url=PORTAL_URLS["DST"]
        )

    async def crawl(self) -> List[CrawledNotice]:
        notices: List[CrawledNotice] = []
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_with_retry(self.portal_url, session)
            if not html:
                logger.info(f"Live HTML not reachable for DST; utilizing fallback seed parsing.")
                return notices

            soup = BeautifulSoup(html, "html.parser")
            rows = soup.find_all(["tr", "div", "li"], class_=lambda c: c and any(k in str(c).lower() for k in ["view-row", "call", "announcement", "item"]))
            
            for idx, item in enumerate(rows[:10], start=1):
                link = item.find("a")
                title = link.get_text(strip=True) if link else item.get_text(strip=True)[:100]
                href = link.get("href") if link else self.portal_url
                if href and not href.startswith("http"):
                    href = f"https://dst.gov.in{href}"

                notice_id = f"DST-CALL-2026-{idx:02d}"
                raw_text = item.get_text(separator="\n", strip=True)
                notice = CrawledNotice(
                    notice_id=notice_id,
                    agency=self.agency,
                    title=title or f"DST Call for Proposals #{idx}",
                    source_url=href,
                    raw_content=raw_text,
                    metadata={"scraped_from": self.portal_url},
                )
                if not self.is_duplicate(notice.sha256_hash):
                    self.save_raw_notice(notice)
                    self.record_seen(notice.sha256_hash)
                    notices.append(notice)

        return notices
