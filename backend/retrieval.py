"""
VidyaVaani Semantic Retrieval Module
Implements sentence-transformers multilingual-e5-small with mandatory
'query: ' and 'passage: ' prefixes, normalized embeddings, and FAISS cosine search.
"""

from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

try:
    from backend.config import EMBEDDING_MODEL_NAME, TOP_K, SIM_THRESHOLD
except (ImportError, ValueError):
    from config import EMBEDDING_MODEL_NAME, TOP_K, SIM_THRESHOLD

_MODEL_INSTANCE: Optional[SentenceTransformer] = None


def get_retrieval_model(model_name: str = EMBEDDING_MODEL_NAME) -> SentenceTransformer:
    """Loads and caches the multilingual embedding model instance."""
    global _MODEL_INSTANCE
    if _MODEL_INSTANCE is None:
        _MODEL_INSTANCE = SentenceTransformer(model_name)
    return _MODEL_INSTANCE


def encode_passages(texts: List[str], model: Optional[SentenceTransformer] = None) -> np.ndarray:
    """
    Encodes textbook chunks using the mandatory 'passage: ' prefix required by multilingual-e5.
    Returns normalized L2 float32 embeddings.
    """
    if model is None:
        model = get_retrieval_model()

    prefixed_texts = [f"passage: {t.strip()}" for t in texts]
    embeddings = model.encode(
        prefixed_texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return embeddings.astype(np.float32)


def encode_query(query: str, model: Optional[SentenceTransformer] = None) -> np.ndarray:
    """
    Encodes user query using the mandatory 'query: ' prefix required by multilingual-e5.
    Returns normalized L2 float32 embedding vector of shape (1, dimension).
    """
    if model is None:
        model = get_retrieval_model()

    prefixed_query = f"query: {query.strip()}"
    embedding = model.encode(
        [prefixed_query],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return embedding.astype(np.float32)


def search_similar_chunks(
    query: str,
    chunks: List[Dict[str, Any]],
    index: faiss.Index,
    model: Optional[SentenceTransformer] = None,
    k: int = TOP_K,
    sim_threshold: Optional[float] = None
) -> Tuple[List[Dict[str, Any]], float]:
    """
    Performs cosine similarity search against the FAISS index.
    
    Returns:
        tuple of (matching_chunks_list, top_similarity_score)
    """
    if not chunks or index is None or index.ntotal == 0:
        return [], 0.0

    if model is None:
        model = get_retrieval_model()

    query_vec = encode_query(query, model)
    actual_k = min(k, len(chunks), index.ntotal)
    
    scores, indices = index.search(query_vec, actual_k)
    
    results = []
    top_score = 0.0
    
    if len(scores) > 0 and len(scores[0]) > 0:
        top_score = float(scores[0][0])

    for score, idx in zip(scores[0], indices[0]):
        if 0 <= idx < len(chunks):
            chunk_copy = dict(chunks[idx])
            chunk_copy["score"] = float(score)
            results.append(chunk_copy)

    return results, top_score
