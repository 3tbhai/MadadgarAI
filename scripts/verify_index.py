#!/usr/bin/env python3
"""Vector Index Inspector & Semantic Consistency Probe for MadadgaarAI."""
import json
import sys
from pathlib import Path
import numpy as np

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = PROJECT_ROOT / "data" / "processed" / "vector_index.json"

def verify_index():
    print("=" * 60)
    print("        MadadgaarAI Vector Index Diagnostics & Probe      ")
    print("=" * 60)

    if not INDEX_PATH.exists():
        print(f"[ERROR] Index file not found at {INDEX_PATH}")
        sys.exit(1)

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc_ids = data.get("doc_ids", [])
    embeddings = np.array(data.get("embeddings", []), dtype=np.float32)
    metadata_map = data.get("metadata_map", {})

    print(f"Total Indexed Documents : {len(doc_ids)}")
    print(f"Embedding Matrix Shape  : {embeddings.shape}")

    if len(doc_ids) == 0:
        print("[WARNING] Vector index contains no documents.")
        sys.exit(0)

    dim = embeddings.shape[1] if embeddings.ndim == 2 else 0
    print(f"Embedding Vector Dimension: {dim} (Expected: 384)")

    # Vector norms check (should be normalized ~ 1.0)
    norms = np.linalg.norm(embeddings, axis=1)
    min_norm = float(np.min(norms)) if len(norms) > 0 else 0.0
    max_norm = float(np.max(norms)) if len(norms) > 0 else 0.0
    avg_norm = float(np.mean(norms)) if len(norms) > 0 else 0.0
    print(f"L2 Norm Statistics      : min={min_norm:.4f}, max={max_norm:.4f}, avg={avg_norm:.4f}")

    if abs(avg_norm - 1.0) < 0.05:
        print("[OK] Vectors are properly unit-normalized for cosine similarity.")
    else:
        print("[NOTE] Vectors may be unnormalized or require cosine normalization on query.")

    print("-" * 60)
    print("Sample Indexed Scheme Identifiers:")
    for doc_id in doc_ids[:8]:
        meta = metadata_map.get(doc_id, {})
        title = meta.get("title", "No Title")
        agency = meta.get("agency", "Unknown")
        print(f"  • [{agency}] {doc_id} - {title[:45]}...")

    print("=" * 60)
    print("[SUCCESS] Vector index verification completed.")

if __name__ == "__main__":
    verify_index()
