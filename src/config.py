"""MadadgaarAI Configuration Module."""
import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
BENCHMARK_DATA_DIR = DATA_DIR / "benchmark"
DATABASE_PATH = PROCESSED_DATA_DIR / "madadgaar.db"
JSON_EXPORT_PATH = PROCESSED_DATA_DIR / "funding_opportunities.json"
CSV_EXPORT_PATH = PROCESSED_DATA_DIR / "funding_opportunities.csv"
VECTOR_INDEX_PATH = PROCESSED_DATA_DIR / "vector_index.json"

# Ensure directories exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, BENCHMARK_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Agency Source Endpoints
PORTAL_URLS = {
    "DST": "https://dst.gov.in/call-for-proposals",
    "ANRF": "https://anrfonline.in",
    "CSIR": "https://csir.res.in/funding-schemes",
    "AICTE": "https://www.aicte-india.org/schemes/research-innovations-development-schemes",
    "NSP": "https://scholarships.gov.in",
    "DBT": "https://dbtindia.gov.in/latest-announcements",
}

# Parser & OCR Thresholds
MIN_TEXT_DENSITY_CHARS_PER_PAGE = 120  # Below this, route to OCR worker
MAX_OCR_PAGES = 15

# Embedding & Search
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
RRF_K_CONSTANT = 60  # Standard Reciprocal Rank Fusion constant
DEFAULT_TOP_K = 5

# Application Server
API_HOST = os.getenv("MADADGAAR_HOST", "0.0.0.0")
API_PORT = int(os.getenv("MADADGAAR_PORT", "8000"))
DEBUG = os.getenv("MADADGAAR_DEBUG", "True").lower() in ("true", "1")
