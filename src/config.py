"""MadadgaarAI Configuration Module."""
import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv_file(env_path: Path) -> None:
    """Loads key=value pairs from .env into os.environ without overriding already-set variables."""
    if not env_path.exists():
        return
    try:
        for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val
    except Exception:
        pass


_load_dotenv_file(PROJECT_ROOT / ".env")
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
    "DST": "https://dst.gov.in",
    "ANRF": "https://anrf.gov.in",
    "CSIR": "https://www.csir.res.in",
    "AICTE": "https://www.aicte.gov.in/schemes",
    "NSP": "https://scholarships.gov.in",
    "DBT": "https://birac.nic.in",
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
DEFAULT_PAGE_SIZE = int(os.getenv("MADADGAAR_PAGE_SIZE", "12"))
API_REQUEST_TIMEOUT = float(os.getenv("MADADGAAR_TIMEOUT_SEC", "15.0"))
