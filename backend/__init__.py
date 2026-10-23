"""
VidyaVaani Backend Package
Contains server-side logic:
- LLM reasoning & API keys (Gemini, Groq)
- RAG retrieval & embeddings (multilingual-e5-small, FAISS)
- Document ingestion & PDF parsing (PyMuPDF)
- Speech synthesis & TTS (Azure Edge-TTS, gTTS)
- Database persistence & analytics (SQLite)
- Subject management & library registry
"""

import sys
from pathlib import Path

# Ensure backend directory is in python search path
_BACKEND_DIR = Path(__file__).resolve().parent
_ROOT_DIR = _BACKEND_DIR.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))
