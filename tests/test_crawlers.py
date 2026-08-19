"""Tests for Crawler Deduplication and Ingestion."""
import pytest
from src.crawlers.base import CrawledNotice
from src.crawlers.seed_data import get_seed_foa_dataset
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


def test_seed_dataset_generation():
    seeds = get_seed_foa_dataset()
    assert len(seeds) >= 6
    agencies = {s.agency for s in seeds}
    assert AgencyType.DST in agencies
    assert AgencyType.ANRF in agencies
    assert AgencyType.CSIR in agencies
    assert AgencyType.AICTE in agencies
