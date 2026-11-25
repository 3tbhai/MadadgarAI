#!/usr/bin/env python3
"""Dataset Statistics & Summary Reporter for MadadgaarAI."""
import json
import sqlite3
import sys
from pathlib import Path
from collections import Counter

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "processed" / "madadgaar.db"
JSON_PATH = PROJECT_ROOT / "data" / "processed" / "funding_opportunities.json"

def generate_stats():
    if not DB_PATH.exists():
        print(f"[ERROR] Database {DB_PATH} not found.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT foa_id, title, agency, eligibility_json, financials_json FROM funding_opportunities")
    rows = cursor.fetchall()
    conn.close()

    total = len(rows)
    agencies = Counter()
    social_categories = Counter()
    degrees = Counter()
    scholarship_count = 0
    grant_count = 0

    for foa_id, title, agency, elig_str, fin_str in rows:
        agencies[agency] += 1
        if "SCHOLARSHIP" in foa_id.upper() or "SCHOLARSHIP" in title.upper():
            scholarship_count += 1
        else:
            grant_count += 1

        if elig_str:
            try:
                elig = json.loads(elig_str)
                for cat in elig.get("target_social_categories", []):
                    social_categories[cat] += 1
                for deg in elig.get("required_degree_levels", []):
                    degrees[deg] += 1
            except Exception:
                pass

    print("=" * 60)
    print("           MadadgaarAI Repository Analytics            ")
    print("=" * 60)
    print(f"Total Active Opportunities : {total}")
    print(f"  • Student Scholarships   : {scholarship_count}")
    print(f"  • Faculty/Research Grants: {grant_count}")
    print("-" * 60)
    print("Distribution by Statutory Agency:")
    for ag, count in agencies.most_common():
        pct = (count / total) * 100
        print(f"  • {ag.ljust(22)}: {str(count).rjust(4)} ({pct:5.1f}%)")
    print("-" * 60)
    if social_categories:
        print("Target Social Categories Coverage:")
        for cat, count in social_categories.most_common(6):
            print(f"  • {cat.ljust(22)}: {count} schemes")
    print("=" * 60)

if __name__ == "__main__":
    generate_stats()

