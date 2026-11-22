"""Tests for Crawler Deduplication, Canonicalization, and Link Guard."""
from src.crawlers.base import CrawledNotice
from src.crawlers.link_verifier import canonicalize_url, is_specific_listing_url
from src.crawlers.live_scrapers import build_live_scrapers
from src.schemas.foa import AgencyType


def test_sha256_deduplication():
    notice1 = CrawledNotice(
        notice_id="N-01",
        agency=AgencyType.DST,
        title="Notice Alpha",
        source_url="https://dst.gov.in/a",
        raw_content="Call for proposals in AI systems.",
    )
    notice2 = CrawledNotice(
        notice_id="N-02",
        agency=AgencyType.DST,
        title="Notice Alpha",
        source_url="https://dst.gov.in/a",
        raw_content="Call for proposals in AI systems.",
    )
    assert notice1.sha256_hash == notice2.sha256_hash
    assert len(notice1.sha256_hash) == 64


def test_canonical_url_and_anti_homepage_guard():
    assert canonicalize_url("https://Example.com/grants/123/?utm_source=twitter&id=5") == "https://example.com/grants/123?id=5"
    assert is_specific_listing_url("https://grants.gov/search-results-detail/356893") is True
    assert is_specific_listing_url("https://grants.gov/") is False
    assert is_specific_listing_url("javascript:void(0)") is False


def test_live_scrapers_registered():
    scrapers = build_live_scrapers()
    assert len(scrapers) >= 6
