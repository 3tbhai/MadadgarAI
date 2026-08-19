"""Dense Semantic Text Embedder with Resilient Fallback."""
import logging
from typing import List, Optional
import numpy as np

from src.config import EMBEDDING_DIMENSION, EMBEDDING_MODEL_NAME

logger = logging.getLogger("MadadgaarAI.Embeddings.Embedder")


class TextEmbedder:
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        self.dimension = EMBEDDING_DIMENSION
        self.st_model = None
        self._init_model()

    def _init_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.st_model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded SentenceTransformer: {self.model_name}")
        except Exception as e:
            logger.warning(
                f"SentenceTransformer not initialized directly ({e}). Utilizing deterministic semantic vectorizer."
            )
            self.st_model = None

    def embed_text(self, text: str) -> List[float]:
        """Encodes single text string into a normalized 384-dimensional dense vector."""
        if not text or not text.strip():
            return [0.0] * self.dimension

        if self.st_model is not None:
            try:
                emb = self.st_model.encode(text, normalize_embeddings=True)
                return emb.tolist()
            except Exception as e:
                logger.error(f"SentenceTransformer encoding error: {e}")

        # Resilient deterministic semantic embedding
        return self._deterministic_semantic_vector(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Batch encodes list of text strings."""
        if not texts:
            return []
        if self.st_model is not None:
            try:
                embs = self.st_model.encode(texts, normalize_embeddings=True)
                return [e.tolist() for e in embs]
            except Exception as e:
                logger.error(f"SentenceTransformer batch encoding error: {e}")

        return [self._deterministic_semantic_vector(t) for t in texts]

    def _deterministic_semantic_vector(self, text: str) -> List[float]:
        """Generates a dense vector with hash-based word n-gram features."""
        vector = np.zeros(self.dimension, dtype=np.float32)
        words = text.lower().replace(",", " ").replace(".", " ").split()
        if not words:
            return vector.tolist()

        for idx, word in enumerate(words):
            if len(word) < 2:
                continue
            # Use deterministic hash projections
            h1 = hash(word) % self.dimension
            h2 = hash(word + "_term") % self.dimension
            weight = 1.0 / (1.0 + (idx * 0.01))
            vector[h1] += weight
            vector[h2] += weight * 0.5

        # Also add bigrams for local context
        for idx in range(len(words) - 1):
            bigram = f"{words[idx]}_{words[idx+1]}"
            bh = hash(bigram) % self.dimension
            vector[bh] += 1.5

        # L2 Normalization
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm

        return vector.tolist()

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Calculates cosine similarity between two unit vectors."""
        a = np.array(vec_a, dtype=np.float32)
        b = np.array(vec_b, dtype=np.float32)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
