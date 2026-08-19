"""Crawlers package initialization."""
from .base import BasePortalCrawler, CrawledNotice
from .dst_crawler import DSTCrawler
from .anrf_crawler import ANRFCrawler
from .csir_crawler import CSIRCrawler
from .aicte_crawler import AICTECrawler
from .nsp_crawler import NSPCrawler
from .seed_data import get_seed_foa_dataset

__all__ = [
    "BasePortalCrawler",
    "CrawledNotice",
    "DSTCrawler",
    "ANRFCrawler",
    "CSIRCrawler",
    "AICTECrawler",
    "NSPCrawler",
    "get_seed_foa_dataset",
]
