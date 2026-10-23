"""
VidyaVaani Subject Registry & SQLite Data Layer
Handles auto-saving, hash deduplication, indexing metadata, and deletion for subjects.
"""

import sqlite3
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

from config import DB_PATH, INDEX_DIR


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Returns a SQLite connection with Row factory."""
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_library_db(db_path: Path = DB_PATH) -> None:
    """Initializes tables for subjects, student queries, and quiz scores."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Subjects registry
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS subjects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                file_hash TEXT UNIQUE NOT NULL,
                filename TEXT NOT NULL,
                num_chunks INTEGER NOT NULL,
                num_pages INTEGER NOT NULL,
                index_path TEXT NOT NULL,
                created_at DATETIME NOT NULL
            )
            """
        )
        
        # Student questions & tutor interactions
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id TEXT,
                student_name TEXT NOT NULL,
                language TEXT NOT NULL,
                query TEXT NOT NULL,
                response TEXT,
                timestamp DATETIME NOT NULL
            )
            """
        )
        
        # Student quiz results
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id TEXT,
                student_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                timestamp DATETIME NOT NULL
            )
            """
        )
        conn.commit()


def compute_file_hash(content: bytes) -> str:
    """Computes SHA-256 hash for file content deduplication."""
    return hashlib.sha256(content).hexdigest()


def get_subject_by_hash(file_hash: str) -> Optional[Dict[str, Any]]:
    """Checks if a document with this hash already exists."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subjects WHERE file_hash = ?", (file_hash,))
        row = cursor.fetchone()
        if row:
            return dict(row)
    return None


def get_subject_by_id(subject_id: str) -> Optional[Dict[str, Any]]:
    """Fetches subject record by subject ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
    return None


def list_subjects() -> List[Dict[str, Any]]:
    """Returns all registered subjects ordered by creation time descending."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subjects ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]


def save_subject(
    subject_id: str,
    name: str,
    file_hash: str,
    filename: str,
    num_chunks: int,
    num_pages: int,
    index_path: str
) -> Dict[str, Any]:
    """Saves or updates a subject in the SQLite registry."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO subjects 
            (id, name, file_hash, filename, num_chunks, num_pages, index_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (subject_id, name.strip(), file_hash, filename, num_chunks, num_pages, str(index_path), now)
        )
        conn.commit()
    return get_subject_by_id(subject_id)


def delete_subject(subject_id: str) -> bool:
    """Deletes a subject from the registry and removes its persisted FAISS index files."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
        conn.commit()
    
    # Remove index directory safely on all OS including Windows OneDrive
    import gc
    import os
    import stat
    gc.collect()

    def _remove_readonly(func, path, _):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception:
            pass

    target_dir = INDEX_DIR / subject_id
    if target_dir.exists():
        try:
            os.chmod(str(target_dir), stat.S_IWRITE)
            shutil.rmtree(str(target_dir), onerror=_remove_readonly)
        except Exception:
            pass
    return True


def log_interaction(student_name: str, language: str, query: str, response: str = "", subject_id: Optional[str] = None):
    """Logs question and answer to interactions table."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO interactions (subject_id, student_name, language, query, response, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (subject_id, student_name.strip() or "Anonymous Learner", language, query.strip(), response.strip(), now)
        )
        conn.commit()


def log_quiz(student_name: str, score: int, total: int, subject_id: Optional[str] = None):
    """Logs quiz score."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO quiz_results (subject_id, student_name, score, total, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (subject_id, student_name.strip() or "Anonymous Learner", int(score), int(total), now)
        )
        conn.commit()
