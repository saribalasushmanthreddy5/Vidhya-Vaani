"""
VidyaVaani Document Ingestion Module
Handles PyMuPDF extraction, word-window chunking with page tracking,
and persistent FAISS indexing under data/indexes/<id>/.
"""

import os
import re
import json
import uuid
from pathlib import Path
from typing import List, Dict, Any, Tuple, Union, BinaryIO, Optional

import pymupdf as fitz
import faiss
import numpy as np

try:
    from backend.config import INDEX_DIR, CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS
except (ImportError, ValueError):
    from config import INDEX_DIR, CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS


def extract_chunks_from_pdf(
    pdf_source: Union[str, Path, bytes, BinaryIO],
    chunk_size_words: int = CHUNK_SIZE_WORDS,
    overlap_words: int = CHUNK_OVERLAP_WORDS
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Extracts text per page using PyMuPDF and slices text into word-window chunks
    while strictly recording page citations.
    
    Raises:
        ValueError: If PDF is corrupt or completely devoid of selectable text (scanned PDF).
    """
    try:
        if isinstance(pdf_source, (str, Path)):
            doc = fitz.open(str(pdf_source))
        elif isinstance(pdf_source, bytes):
            doc = fitz.open(stream=pdf_source, filetype="pdf")
        elif hasattr(pdf_source, "read"):
            doc = fitz.open(stream=pdf_source.read(), filetype="pdf")
        else:
            raise ValueError("Unsupported PDF input type.")
    except Exception as e:
        raise ValueError(f"Could not read PDF file. It might be corrupt or an invalid format: {str(e)}")

    total_pages = len(doc)
    if total_pages == 0:
        doc.close()
        raise ValueError("The provided PDF has 0 pages.")

    all_chunks: List[Dict[str, Any]] = []
    total_text_length = 0

    for page_idx in range(total_pages):
        page = doc[page_idx]
        page_num = page_idx + 1
        raw_text = page.get_text("text") or ""
        # Clean extra whitespaces
        cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()
        total_text_length += len(cleaned_text)

        if not cleaned_text:
            continue

        words = cleaned_text.split()
        if not words:
            continue

        start = 0
        step = max(1, chunk_size_words - overlap_words)
        while start < len(words):
            chunk_slice = words[start : start + chunk_size_words]
            chunk_str = " ".join(chunk_slice).strip()
            if len(chunk_str) > 15:  # Skip negligible fragments
                all_chunks.append({
                    "page": page_num,
                    "text": chunk_str
                })
            start += step

    doc.close()

    if total_text_length == 0 or not all_chunks:
        raise ValueError(
            "This PDF contains no readable text. It appears to be a scanned image or empty document. "
            "Please provide a text-selectable PDF."
        )

    return all_chunks, total_pages


def build_and_save_index(
    subject_id: str,
    chunks: List[Dict[str, Any]],
    embeddings: np.ndarray
) -> Path:
    """
    Builds a FAISS IndexFlatIP (cosine similarity on normalized vectors)
    and persists index.faiss and chunks.json in data/indexes/<subject_id>/.
    """
    if len(chunks) == 0:
        raise ValueError("Cannot index empty chunks.")

    target_dir = INDEX_DIR / subject_id
    target_dir.mkdir(parents=True, exist_ok=True)

    embeddings = np.ascontiguousarray(embeddings.astype(np.float32))
    dimension = embeddings.shape[1]

    # IndexFlatIP calculates inner product, which equals cosine similarity for normalized vectors
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    index_file = target_dir / "index.faiss"
    faiss.write_index(index, str(index_file))

    chunks_file = target_dir / "chunks.json"
    with open(chunks_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    return target_dir


def load_saved_index(subject_id: str) -> Tuple[Optional[faiss.Index], List[Dict[str, Any]]]:
    """
    Loads persisted FAISS index and chunk metadata from data/indexes/<subject_id>/.
    """
    target_dir = INDEX_DIR / subject_id
    index_file = target_dir / "index.faiss"
    chunks_file = target_dir / "chunks.json"

    if not index_file.exists() or not chunks_file.exists():
        return None, []

    index = faiss.read_index(str(index_file))
    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    return index, chunks
