"""
VidyaVaani SQLite Data Layer
Provides zero-setup local persistence for student interactions, quiz results, and analytics metrics.
"""

import sqlite3
import pandas as pd
from datetime import datetime

DEFAULT_DB_PATH = "vidyavaani.db"


def get_connection(db_path=DEFAULT_DB_PATH):
    """Establishes a connection to the SQLite database with thread safety."""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=DEFAULT_DB_PATH):
    """Initializes tables automatically on app startup if they do not exist."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Student questions & tutor interactions
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                language TEXT NOT NULL,
                query TEXT NOT NULL,
                timestamp DATETIME NOT NULL
            )
            """
        )
        
        # Student practice quiz results
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                timestamp DATETIME NOT NULL
            )
            """
        )
        conn.commit()

        # Seed initial demo data if tables are brand new
        cursor.execute("SELECT COUNT(*) FROM interactions")
        count = cursor.fetchone()[0]
        if count == 0:
            demo_interactions = [
                ("Aarav Sharma", "Hindi", "प्रकाश संश्लेषण क्या है और इसके मुख्य चरण क्या हैं?", "2026-10-16 10:15:22"),
                ("Ananya Gowda", "Kannada", "ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆಯ ಸಮೀಕರಣ ಮತ್ತು ಹಂತಗಳನ್ನು ವಿವರಿಸಿ.", "2026-10-16 11:20:45"),
                ("Rohan Verma", "English", "What is the role of hydrochloric acid in the stomach?", "2026-10-16 12:05:10"),
                ("Meera Patel", "Hindi", "अवायवीय श्वसन और वायवीय श्वसन में क्या अंतर है?", "2026-10-16 13:42:33"),
                ("Kiran Kumar", "Kannada", "ಜಠರದಲ್ಲಿ ಪೆಪ್ಸಿನ್ ಕಿಣ್ವ ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ?", "2026-10-16 14:10:04"),
                ("Sneha Reddy", "Telugu", "కిరణజన్య సంయోగక్రియ (Photosynthesis) లో గ్లూకోజ్ ఎలా ఉత్పత్తి అవుతుంది?", "2026-10-16 14:45:10"),
                ("Rohan Verma", "English", "Why do human muscle cells produce lactic acid during exercise?", "2026-10-16 15:30:19")
            ]
            cursor.executemany(
                "INSERT INTO interactions (student_name, language, query, timestamp) VALUES (?, ?, ?, ?)",
                demo_interactions
            )

            demo_quizzes = [
                ("Aarav Sharma", 5, 5, "2026-10-16 10:30:00"),
                ("Ananya Gowda", 4, 5, "2026-10-16 11:35:12"),
                ("Rohan Verma", 4, 5, "2026-10-16 12:18:40"),
                ("Meera Patel", 3, 5, "2026-10-16 13:55:00"),
                ("Kiran Kumar", 5, 5, "2026-10-16 14:25:20"),
                ("Sneha Reddy", 4, 5, "2026-10-16 15:45:10")
            ]
            cursor.executemany(
                "INSERT INTO quiz_results (student_name, score, total, timestamp) VALUES (?, ?, ?, ?)",
                demo_quizzes
            )
            conn.commit()


def log_interaction(student_name: str, language: str, query: str, db_path=DEFAULT_DB_PATH):
    """Logs a student question and interaction into the database."""
    name = student_name.strip() if student_name and student_name.strip() else "Anonymous Learner"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO interactions (student_name, language, query, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (name, language, query.strip(), now),
        )
        conn.commit()


def log_quiz(student_name: str, score: int, total: int, db_path=DEFAULT_DB_PATH):
    """Logs a completed quiz result into the database."""
    name = student_name.strip() if student_name and student_name.strip() else "Anonymous Learner"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO quiz_results (student_name, score, total, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (name, int(score), int(total), now),
        )
        conn.commit()


def fetch_dashboard_metrics(db_path=DEFAULT_DB_PATH):
    """Fetches high-level metrics for the Teacher / Analytics Dashboard."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Total Questions Asked
        cursor.execute("SELECT COUNT(*) FROM interactions")
        total_questions = cursor.fetchone()[0] or 0
        
        # Active Students Count (union of names in interactions & quizzes)
        cursor.execute(
            """
            SELECT COUNT(DISTINCT name) FROM (
                SELECT student_name AS name FROM interactions
                UNION
                SELECT student_name AS name FROM quiz_results
            )
            """
        )
        active_students = cursor.fetchone()[0] or 0
        
        # Average Quiz Score (%)
        cursor.execute(
            """
            SELECT AVG(CAST(score AS FLOAT) / CASE WHEN total > 0 THEN total ELSE 1 END * 100)
            FROM quiz_results
            """
        )
        avg_score_row = cursor.fetchone()[0]
        avg_score_pct = round(avg_score_row, 1) if avg_score_row is not None else 0.0
        
        # Top Language Used
        cursor.execute(
            """
            SELECT language, COUNT(*) as cnt
            FROM interactions
            GROUP BY language
            ORDER BY cnt DESC
            LIMIT 1
            """
        )
        top_lang_row = cursor.fetchone()
        top_language = top_lang_row[0] if top_lang_row else "English"
        
        return {
            "total_questions": total_questions,
            "active_students": active_students,
            "avg_quiz_score_pct": avg_score_pct,
            "top_language": top_language,
        }


def fetch_recent_interactions(limit: int = 50, db_path=DEFAULT_DB_PATH) -> pd.DataFrame:
    """Returns a pandas DataFrame of recent student questions."""
    with get_connection(db_path) as conn:
        query = f"""
            SELECT id, student_name, language, query, timestamp
            FROM interactions
            ORDER BY id DESC
            LIMIT {int(limit)}
        """
        df = pd.read_sql_query(query, conn)
        return df


def fetch_language_breakdown(db_path=DEFAULT_DB_PATH) -> pd.DataFrame:
    """Returns language usage counts for charts."""
    with get_connection(db_path) as conn:
        query = """
            SELECT language, COUNT(*) as count
            FROM interactions
            GROUP BY language
            ORDER BY count DESC
        """
        df = pd.read_sql_query(query, conn)
        return df


def fetch_quiz_score_distribution(db_path=DEFAULT_DB_PATH) -> pd.DataFrame:
    """Returns quiz performance data."""
    with get_connection(db_path) as conn:
        query = """
            SELECT student_name, score, total,
                   ROUND((CAST(score AS FLOAT) / total) * 100, 1) as percentage,
                   timestamp
            FROM quiz_results
            ORDER BY id DESC
        """
        df = pd.read_sql_query(query, conn)
        return df


def export_student_logs_csv(db_path=DEFAULT_DB_PATH) -> str:
    """Exports all student interactions and quiz results merged into a CSV string."""
    with get_connection(db_path) as conn:
        interactions_df = pd.read_sql_query("SELECT * FROM interactions ORDER BY id DESC", conn)
        return interactions_df.to_csv(index=False)
