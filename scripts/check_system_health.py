#!/usr/bin/env python3
"""Pre-flight System Diagnostics and Health Check Utility for MadadgaarAI."""
import os
import sys
import sqlite3
import json
import importlib.util
from pathlib import Path

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "processed" / "madadgaar.db"
INDEX_PATH = PROJECT_ROOT / "data" / "processed" / "vector_index.json"

REQUIRED_PACKAGES = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "numpy",
    "rank_bm25",
    "httpx",
    "bs4",
    "pytest",
]

OPTIONAL_PACKAGES = [
    "sentence_transformers",
    "torch",
]

def check_python_version() -> bool:
    print(f"[*] Python Version: {sys.version.split()[0]}", end=" ", flush=True)
    if sys.version_info >= (3, 10):
        print("[OK]", flush=True)
        return True
    print("[FAIL] (Requires Python 3.10+)", flush=True)
    return False

def check_dependencies() -> bool:
    print("[*] Checking Core Dependencies:", flush=True)
    all_ok = True
    for pkg in REQUIRED_PACKAGES:
        spec = importlib.util.find_spec(pkg)
        if spec is not None:
            print(f"    • {pkg.ljust(25)}: [OK]", flush=True)
        else:
            print(f"    • {pkg.ljust(25)}: [MISSING]", flush=True)
            all_ok = False
    for pkg in OPTIONAL_PACKAGES:
        spec = importlib.util.find_spec(pkg)
        status = "[OK]" if spec is not None else "[OPTIONAL - deterministic 384d fallback active]"
        print(f"    • {pkg.ljust(25)}: {status}", flush=True)
    return all_ok

def check_database() -> bool:
    print(f"[*] SQLite Database ({DB_PATH.name}):", end=" ", flush=True)
    if not DB_PATH.exists():
        print("[NOT FOUND - will bootstrap on first run]", flush=True)
        return True
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM funding_opportunities")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"[OK] ({count} opportunities present)", flush=True)
        return True
    except Exception as e:
        print(f"[FAIL] ({e})", flush=True)
        return False

def check_vector_index() -> bool:
    print(f"[*] Dense Vector Index ({INDEX_PATH.name}):", end=" ", flush=True)
    if not INDEX_PATH.exists():
        print("[NOT FOUND - will generate on first run]", flush=True)
        return True
    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        doc_count = len(data.get("doc_ids", []))
        print(f"[OK] ({doc_count} embeddings indexed)", flush=True)
        return True
    except Exception as e:
        print(f"[FAIL] ({e})", flush=True)
        return False

def main():
    print("=" * 60, flush=True)
    print("      MadadgaarAI Pre-flight Diagnostics System        ", flush=True)
    print("=" * 60, flush=True)
    py_ok = check_python_version()
    dep_ok = check_dependencies()
    db_ok = check_database()
    vec_ok = check_vector_index()
    print("=" * 60, flush=True)
    if py_ok and dep_ok and db_ok and vec_ok:
        print("[SUCCESS] All pre-flight system checks PASSED! System is ready.", flush=True)
        sys.exit(0)
    else:
        print("[WARNING] One or more diagnostic checks encountered issues.", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
