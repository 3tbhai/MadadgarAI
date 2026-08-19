"""Vector Database & Semantic Index Store."""
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from src.config import VECTOR_INDEX_PATH
from src.embeddings.embedder import TextEmbedder

logger = logging.getLogger("MadadgaarAI.Embeddings.VectorStore")


class VectorStore:
    def __init__(self, index_path: Path = VECTOR_INDEX_PATH):
        self.index_path = index_path
        self.embedder = TextEmbedder()
        self.doc_ids: List[str] = []
        self.embeddings: np.ndarray = np.empty((0, self.embedder.dimension), dtype=np.float32)
        self.metadata_map: Dict[str, Dict[str, Any]] = {}
        self.load_index()

    def add_document(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        """Indexes a document text with its metadata."""
        emb = self.embedder.embed_text(text)
        emb_arr = np.array(emb, dtype=np.float32).reshape(1, -1)

        if doc_id in self.doc_ids:
            idx = self.doc_ids.index(doc_id)
            self.embeddings[idx] = emb_arr
            self.metadata_map[doc_id] = metadata or {}
        else:
            self.doc_ids.append(doc_id)
            if self.embeddings.shape[0] == 0:
                self.embeddings = emb_arr
            else:
                self.embeddings = np.vstack([self.embeddings, emb_arr])
            self.metadata_map[doc_id] = metadata or {}

    def search_dense(self, query_text: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Returns top_k (doc_id, cosine_similarity) matches."""
        if len(self.doc_ids) == 0:
            return []

        query_emb = np.array(self.embedder.embed_text(query_text), dtype=np.float32)
        query_norm = np.linalg.norm(query_emb)
        if query_norm > 0:
            query_emb = query_emb / query_norm

        # Vectorized cosine similarities
        scores = np.dot(self.embeddings, query_emb)
        ranked_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in ranked_indices:
            doc_id = self.doc_ids[idx]
            sim = float(scores[idx])
            results.append((doc_id, round(sim, 4)))

        return results

    def save_index(self):
        """Persists the vector index and metadata to disk."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "doc_ids": self.doc_ids,
            "embeddings": self.embeddings.tolist(),
            "metadata_map": self.metadata_map,
        }
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)
        logger.info(f"Saved {len(self.doc_ids)} vector embeddings to {self.index_path}")

    def load_index(self):
        """Loads index from disk if present."""
        if self.index_path.exists():
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                self.doc_ids = payload.get("doc_ids", [])
                embs = payload.get("embeddings", [])
                if embs:
                    self.embeddings = np.array(embs, dtype=np.float32)
                else:
                    self.embeddings = np.empty((0, self.embedder.dimension), dtype=np.float32)
                self.metadata_map = payload.get("metadata_map", {})
            except Exception as e:
                logger.error(f"Failed to load vector index: {e}")
