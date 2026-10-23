"""
VidyaVaani (ವಿಧ್ಯಾವಾಣಿ / विद्यावाणी): Voice-First Multilingual AI Tutor
Synapse Design System Interface:
- Vantablack (#030303) foundation with ambient floating violet & cyan glowing orbs
- Instrument Serif typography for high-impact editorial headings
- Crisp Inter typography & JetBrains Mono for metrics and UI
- Floating Glass Navigation Pill, Infinite Marquee Metrics Ticker, and 3-Column Interactive Cards
- High-Tech Dark IDE-Style Tutor Response block with terminal window controls
- Zero API keys exposed on frontend; all backend logic and AI credentials safely server-side
"""

import os
import sys
import time
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any

# Ensure project root and backend are in path
_FRONTEND_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _FRONTEND_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "backend"))

import streamlit as st
import pandas as pd
import numpy as np

# Import VidyaVaani modular backend components
from backend.config import (
    LANGUAGES,
    DEFAULT_SAMPLE_PDF,
    SIM_THRESHOLD,
    TOP_K,
    INDEX_DIR,
    DB_PATH
)
import backend.library as library
import backend.ingest as ingest
import backend.retrieval as retrieval
import backend.llm as llm
import backend.speech as speech
import backend.quiz as quiz

# Optional voice recorder
try:
    from streamlit_mic_recorder import speech_to_text
except ImportError:
    speech_to_text = None

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="VidyaVaani • Synapse Voice AI Tutor",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SYNAPSE DESIGN SYSTEM CSS INJECTION
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;600&family=Noto+Sans+Kannada:wght@400;600&family=Noto+Sans+Telugu:wght@400;600&family=Noto+Sans+Tamil:wght@400;600&family=Noto+Sans+Malayalam:wght@400;600&family=Noto+Sans+Bengali:wght@400;600&family=Noto+Sans+Gujarati:wght@400;600&display=swap');

    /* Global Reset & Vantablack Base */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #030303 !important;
        color: #EDEDED !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #060606 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* Ambient Floating Orbs */
    .synapse-orb-violet {
        position: fixed;
        width: 650px;
        height: 650px;
        top: -120px;
        left: 50%;
        transform: translateX(-50%);
        background: radial-gradient(circle, rgba(139, 92, 246, 0.22) 0%, rgba(139, 92, 246, 0) 70%);
        filter: blur(85px);
        pointer-events: none;
        z-index: 0;
        animation: floatOrb 12s ease-in-out infinite alternate;
    }
    .synapse-orb-cyan {
        position: fixed;
        width: 550px;
        height: 550px;
        top: 380px;
        left: -120px;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.14) 0%, rgba(6, 182, 212, 0) 70%);
        filter: blur(95px);
        pointer-events: none;
        z-index: 0;
        animation: floatOrb 15s ease-in-out infinite alternate-reverse;
    }
    @keyframes floatOrb {
        0% { transform: translateY(0px) scale(1); }
        100% { transform: translateY(-24px) scale(1.05); }
    }

    /* Typography Classes */
    .font-serif {
        font-family: 'Instrument Serif', Georgia, serif !important;
        letter-spacing: -0.025em;
    }
    .font-mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Text Shimmer Animation */
    .shimmer-text {
        background: linear-gradient(90deg, #A78BFA 0%, #FFFFFF 40%, #FFFFFF 60%, #22D3EE 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textShimmer 4s linear infinite;
        font-style: italic;
    }
    @keyframes textShimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    /* Fixed Navigation Pill */
    .nav-pill-container {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: 28px;
    }
    .nav-pill {
        width: 100%;
        max-width: 672px;
        background: rgba(10, 10, 10, 0.72);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 9999px;
        padding: 8px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.8), 0 0 20px -10px rgba(139, 92, 246, 0.3);
        z-index: 10;
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .nav-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: linear-gradient(135deg, #8B5CF6, #06B6D4);
        box-shadow: 0 0 8px #8B5CF6;
    }
    .nav-title {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 1.25rem;
        color: #FFFFFF;
        font-weight: 500;
        letter-spacing: -0.01em;
    }
    .nav-links {
        display: flex;
        gap: 12px;
        align-items: center;
        font-size: 0.75rem;
        font-weight: 600;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    .nav-cta {
        background: #FFFFFF;
        color: #030303;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 5px 14px;
        border-radius: 9999px;
        display: flex;
        align-items: center;
        gap: 6px;
        letter-spacing: 0.02em;
        transition: transform 0.2s cubic-bezier(0.23, 1, 0.32, 1);
    }
    .nav-cta:hover {
        transform: scale(1.04);
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 36px 16px 28px 16px;
        position: relative;
        z-index: 1;
    }
    .hero-heading {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 3.6rem;
        line-height: 1.04;
        font-weight: 400;
        color: #FFFFFF;
        margin-bottom: 14px;
        letter-spacing: -0.035em;
    }
    .hero-subtext {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        color: #9CA3AF;
        max-width: 680px;
        margin: 0 auto 24px auto;
        line-height: 1.55;
        font-weight: 300;
    }
    .hero-badges-row {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 10px;
    }
    .synapse-badge {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 9999px;
        padding: 6px 16px;
        font-size: 0.82rem;
        color: #D1D5DB;
        display: inline-flex;
        align-items: center;
        gap: 7px;
        font-family: 'Inter', sans-serif;
        transition: all 0.25s cubic-bezier(0.23, 1, 0.32, 1);
    }
    .synapse-badge:hover {
        border-color: rgba(139, 92, 246, 0.4);
        box-shadow: 0 0 15px -5px rgba(139, 92, 246, 0.4);
        color: #FFFFFF;
    }

    /* Infinite Metrics Marquee Ticker */
    .ticker-wrapper {
        width: 100%;
        overflow: hidden;
        background: rgba(0, 0, 0, 0.45);
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin: 24px 0 32px 0;
        padding: 14px 0;
        position: relative;
    }
    .ticker-track {
        display: flex;
        width: max-content;
        animation: tickerMarquee 38s linear infinite;
        gap: 36px;
    }
    @keyframes tickerMarquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .ticker-item {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'JetBrains Mono', monospace;
    }
    .ticker-label {
        font-size: 0.65rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }
    .ticker-value {
        font-size: 0.88rem;
        font-weight: 600;
        color: #F3F4F6;
    }
    .ticker-accent-violet { color: #A78BFA; }
    .ticker-accent-cyan { color: #22D3EE; }
    .ticker-accent-emerald { color: #34D399; }

    /* Interactive Feature Cards (3-column) */
    .synapse-feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-bottom: 32px;
    }
    @media (max-width: 900px) {
        .synapse-feature-grid { grid-template-columns: 1fr; }
    }
    .synapse-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 26px 28px;
        transition: transform 0.35s cubic-bezier(0.23, 1, 0.32, 1), border-color 0.35s, box-shadow 0.35s;
        position: relative;
        overflow: hidden;
    }
    .synapse-card:hover {
        transform: translateY(-8px);
        border-color: rgba(139, 92, 246, 0.4);
        box-shadow: 0 0 25px -8px rgba(139, 92, 246, 0.35);
        background: rgba(255, 255, 255, 0.035);
    }
    .card-icon-box {
        width: 46px;
        height: 46px;
        border-radius: 12px;
        background: rgba(139, 92, 246, 0.12);
        border: 1px solid rgba(139, 92, 246, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin-bottom: 16px;
        transition: transform 0.3s cubic-bezier(0.23, 1, 0.32, 1);
    }
    .synapse-card:hover .card-icon-box {
        transform: scale(1.1) rotate(-4deg);
    }
    .card-title {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 1.45rem;
        color: #FFFFFF;
        margin-bottom: 8px;
        font-weight: 500;
    }
    .card-body {
        color: #9CA3AF;
        font-size: 0.9rem;
        line-height: 1.5;
        font-weight: 300;
    }

    /* Dark IDE-Style Tutor Response Block */
    .ide-window {
        background: rgba(8, 8, 8, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        overflow: hidden;
        margin: 20px 0;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.9), 0 0 25px -10px rgba(139, 92, 246, 0.25);
    }
    .ide-toolbar {
        background: rgba(16, 16, 16, 0.95);
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        padding: 10px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .ide-controls {
        display: flex;
        gap: 7px;
        align-items: center;
    }
    .control-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        opacity: 0.75;
    }
    .dot-red { background: #EF4444; }
    .dot-yellow { background: #EAB308; }
    .dot-green { background: #10B981; }
    .ide-filename {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #9CA3AF;
        letter-spacing: 0.04em;
    }
    .ide-status {
        display: flex;
        align-items: center;
        gap: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #10B981;
    }
    .pulse-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 8px #10B981;
        animation: pulseAnimation 2s infinite;
    }
    @keyframes pulseAnimation {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }
    .ide-content {
        padding: 24px 28px;
        font-family: 'Inter', sans-serif;
        font-size: 1.02rem;
        line-height: 1.68;
        color: #F3F4F6;
    }
    .ide-citation {
        display: inline-block;
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: #C4B5FD;
        padding: 2px 8px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 0 2px;
    }

    /* Shiny Neon Buttons & Controls */
    .stButton > button {
        background: rgba(18, 18, 18, 0.8) !important;
        color: #F9FAFB !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 9999px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 8px 22px !important;
        transition: all 0.25s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }
    .stButton > button:hover {
        border-color: rgba(139, 92, 246, 0.6) !important;
        box-shadow: 0 0 20px -5px rgba(139, 92, 246, 0.45) !important;
        transform: translateY(-2px) !important;
        background: rgba(28, 28, 35, 0.9) !important;
        color: #FFFFFF !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 20px -5px rgba(124, 58, 237, 0.5) !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 28px -3px rgba(124, 58, 237, 0.75) !important;
        transform: translateY(-2px) scale(1.02) !important;
    }

    /* Input Fields */
    .stTextInput input {
        background: rgba(12, 12, 12, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        color: #F3F4F6 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 12px 18px !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 15px -3px rgba(139, 92, 246, 0.4) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        gap: 16px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin-bottom: 24px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #9CA3AF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        padding: 10px 18px !important;
        border: none !important;
        letter-spacing: 0.02em !important;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        border-bottom: 2px solid #8B5CF6 !important;
    }

    /* Passage Citation Cards */
    .synapse-passage {
        background: rgba(255, 255, 255, 0.018);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .synapse-passage-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #A78BFA;
        font-weight: 600;
        margin-bottom: 6px;
    }

    /* Metrics Cards */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: #F3F4F6 !important;
        font-size: 2rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        color: #6B7280 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.15em !important;
        font-size: 0.72rem !important;
    }

    /* Footer */
    .synapse-footer {
        background: #050505;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        padding: 40px 16px 24px 16px;
        margin-top: 60px;
        font-family: 'Inter', sans-serif;
    }
    .footer-grid {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 24px;
        max-width: 1100px;
        margin: 0 auto 32px auto;
    }
    @media (max-width: 800px) {
        .footer-grid { grid-template-columns: 1fr; }
    }
    .footer-brand-title {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 1.8rem;
        color: #FFFFFF;
        margin-bottom: 6px;
    }
    .footer-col-head {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: #6B7280;
        margin-bottom: 12px;
    }
    .footer-link {
        color: #9CA3AF;
        font-size: 0.85rem;
        margin-bottom: 6px;
        display: block;
        text-decoration: none;
    }
    .footer-bottom-bar {
        border-top: 1px solid rgba(255, 255, 255, 0.04);
        padding-top: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1100px;
        margin: 0 auto;
        font-size: 0.78rem;
        color: #6B7280;
    }
    </style>
    
    <!-- Ambient Floating Glow Orbs in DOM -->
    <div class="synapse-orb-violet"></div>
    <div class="synapse-orb-cyan"></div>
    """,
    unsafe_allow_html=True
)

# Initialize database schema
library.init_library_db()

# ==========================================
# RESOURCE CACHE: EMBEDDING MODEL
# ==========================================
@st.cache_resource(show_spinner=False)
def load_embedding_model():
    """Caches sentence-transformers multilingual-e5-small."""
    try:
        return retrieval.get_retrieval_model()
    except Exception as e:
        st.error(f"Failed to load embedding model: {e}")
        return None

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "active_subject" not in st.session_state:
    st.session_state.active_subject = None
if "indexed_chunks" not in st.session_state:
    st.session_state.indexed_chunks = []
if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "last_response" not in st.session_state:
    st.session_state.last_response = ""
if "last_sources" not in st.session_state:
    st.session_state.last_sources = []
if "last_audio_path" not in st.session_state:
    st.session_state.last_audio_path = None
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "student_name" not in st.session_state:
    st.session_state.student_name = "Aarav Sharma"
if "status_message" not in st.session_state:
    st.session_state.status_message = None


def activate_subject(subj: Dict[str, Any]):
    """Loads a subject's persisted FAISS index and chunks into session state."""
    idx, chunks = ingest.load_saved_index(subj["id"])
    if idx is not None and chunks:
        st.session_state.active_subject = subj
        st.session_state.faiss_index = idx
        st.session_state.indexed_chunks = chunks
        st.session_state.quiz_data = None
        st.session_state.last_response = ""
        st.session_state.last_audio_path = None
        return True
    return False


def get_demo_questions(subject_name: str, chunks: List[Dict[str, Any]], language_key: str = "English") -> List[str]:
    """Preloads sample presentation questions for the current subject."""
    all_text = " ".join([c.get("text", "") for c in (chunks or [])[:8]]).lower()
    is_life_processes = (
        "photosynthesis" in all_text or 
        "respiration" in all_text or 
        "science" in (subject_name or "").lower() or
        "life processes" in (subject_name or "").lower()
    )

    if is_life_processes:
        if language_key == "Hindi":
            return [
                "प्रकाश संश्लेषण की रासायनिक समीकरण क्या है?",
                "वायवीय और अवायवीय श्वसन में क्या अंतर है?",
                "आमाशय में हाइड्रोक्लोरिक अम्ल (HCl) की क्या भूमिका है?",
                "द्वार कोशिकाएं रंध्रों को कैसे खोलती और बंद करती हैं?",
                "व्यायाम के दौरान मांसपेशियों में लैक्टिक एसिड क्यों बनता है?"
            ]
        elif language_key == "Kannada":
            return [
                "ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆಯ ರಾಸಾಯನಿಕ ಸಮೀಕರಣವೇನು?",
                "ವಾಯುವಿಕ ಮತ್ತು ಅವಾಯುವಿಕ ಉಸಿರಾಟದ ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು?",
                "ಜಠರದಲ್ಲಿ ಹೈಡ್ರೋಕ್ಲೋರಿಕ್ ಆಮ್ಲದ (HCl) ಪಾತ್ರವೇನು?",
                "ಕಾವಲು ಕೋಶಗಳು ಪತ್ರರಂಧ್ರಗಳನ್ನು ಹೇಗೆ ತೆರೆಯುತ್ತವೆ ಮತ್ತು ಮುಚ್ಚುತ್ತವೆ?",
                "ವ್ಯಾಯಾಮದ ಸಮಯದಲ್ಲಿ ಸ್ನಾಯು ಕೋಶಗಳಲ್ಲಿ ಲ್ಯಾಕ್ಟಿಕ್ ಆಮ್ಲ ಏಕೆ ಸಂಗ್ರಹವಾಗುತ್ತದೆ?"
            ]
        elif language_key == "Telugu":
            return [
                "కిరణజన్య సంయోగక్రియ రసాయన సమీకరణం ఏమిటి?",
                "వాయు సహిత మరియు అవాయు శ్వాసక్రియ మధ్య తేడా ఏమిటి?",
                "జీర్ణాశయంలో హైడ్రోక్లోరిక్ ఆమ్లం (HCl) పాత్ర ఏమిటి?",
                "రక్షక కణాలు పత్రరంధ్రాలను ఎలా తెరుస్తాయి మరియు మూస్తాయి?",
                "వ్యాయామం చేసేటప్పుడు కండరాలలో లాక్టిక్ ఆమ్లం ఎందుకు పేరుకుపోతుంది?"
            ]
        elif language_key == "Tamil":
            return [
                "ஒளிச்சேர்க்கையின் வேதியியல் சமன்பாடு என்ன?",
                "காற்றுள்ள மற்றும் காற்றில்லா சுவாசத்திற்கு உள்ள வேறுபாடு என்ன?",
                "இரைப்பையில் ஹைட்ரோகுளோரிக் அமிலத்தின் (HCl) பங்கு என்ன?",
                "காப்பு செல்கள் இலைத்துளைகளை எவ்வாறு திறந்து மூடுகின்றன?",
                "உடற்பயிற்சியின் போது தசை செல்களில் லாக்டிக் அமிலம் ஏன் உருவாகிறது?"
            ]
        elif language_key == "Marathi":
            return [
                "प्रकाशसंश्लेषण रासायनिक समीकरण काय आहे?",
                "ऑक्सिश्वसन आणि विनाक्सिश्वसन यातील फरक काय आहे?",
                "जठरामध्ये हायड्रोक्लोरिक आम्लाची (HCl) भूमिका काय आहे?",
                "रक्षक पेशी पर्णरंध्रे कशी उघडतात आणि बंद करतात?",
                "व्यायामादरम्यान स्नायूंमध्ये लॅक्टिक ॲसिड का तयार होते?"
            ]
        elif language_key == "Bengali":
            return [
                "সালোকসংশ্লেষের রাসায়নিক সমীকরণটি কী?",
                "সবাত ও অবাত শ্বসনের মধ্যে পার্থক্য কী?",
                "পাকস্থলীতে হাইড্রোক্লোরিক অ্যাসিডের (HCl) ভূমিকা কী?",
                "রক্ষী কোষ কীভাবে পত্ররন্ধ্র খোলে ও বন্ধ করে?",
                "ব্যায়ামের সময় পেশীকোষে ল্যাকটিক অ্যাসিড কেন জমা হয়?"
            ]
        elif language_key == "Gujarati":
            return [
                "પ્રકાશસંશ્લેષણનું રાસાયણિક સમીકરણ શું છે?",
                "જારક અને અજારક શ્વસન વચ્ચે શું તફાવત છે?",
                "જઠરમાં હાઇડ્રોક્લોરિક એસિડ (HCl) નો શો ભાગ છે?",
                "રક્ષક કોષો વાયુરંધ્રોને કેવી રીતે ખોલે અને બંધ કરે છે?",
                "કસરત દરમિયાન સ્નાયુઓમાં લેક્ટિક એસિડ કેમ બને છે?"
            ]
        elif language_key == "Malayalam":
            return [
                "പ്രകാശസംശ്ലേഷണത്തിന്റെ രാസസമവാക്യം എന്താണ്?",
                "വായു ശ്വസനവും അവായു ശ്വസനവും തമ്മിലുള്ള വ്യത്യാസം എന്താണ്?",
                "ആമാശയത്തിൽ ഹൈഡ്രോക്ലോറിക് ആസിഡിന്റെ (HCl) പങ്ക് എന്താണ്?",
                "കാവൽ കോശങ്ങൾ ആസ്യരന്ധ്രങ്ങൾ എങ്ങനെ തുറക്കുകയും അടയ്ക്കുകയും ചെയ്യുന്നു?",
                "വ്യായാമ വേളയിൽ പേശി കോശങ്ങളിൽ ലാക്റ്റിക് ആസിഡ് അടിഞ്ഞുകൂടുന്നത് എന്തുകൊണ്ട്?"
            ]
        else:
            return [
                "What is the chemical equation of photosynthesis?",
                "What is the difference between aerobic and anaerobic respiration?",
                "What is the role of hydrochloric acid (HCl) in the stomach?",
                "How do guard cells open and close stomatal pores?",
                "Why does lactic acid accumulate in muscle cells during exercise?"
            ]
    else:
        extracted = []
        for c in (chunks or []):
            text = c.get("text", "").strip()
            sentences = [s.strip() for s in text.split(".") if len(s.strip().split()) >= 4]
            if sentences:
                candidate = sentences[0].replace("\n", " ").strip()
                if len(candidate) > 55:
                    candidate = candidate[:55] + "..."
                q_candidate = f"What does the textbook explain about: {candidate}?"
                if q_candidate not in extracted:
                    extracted.append(q_candidate)
            if len(extracted) == 5:
                break
        while len(extracted) < 5:
            extracted.append(f"Can you explain the main points on Page {len(extracted) + 1}?")
        return extracted[:5]


# Auto-load the most recent subject if none is active
existing_subjects = library.list_subjects()
if st.session_state.active_subject is None and existing_subjects:
    activate_subject(existing_subjects[0])

# ==========================================
# SIDEBAR: SETUP & TEXTBOOK MANAGEMENT
# ==========================================
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
            <span class="nav-dot"></span>
            <span style="font-family: 'Instrument Serif', Georgia, serif; font-size: 1.45rem; color: #FFFFFF; font-weight: 500;">
                VidyaVaani Setup
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 1. Student Name
    student_name_input = st.text_input("👤 Student Name / ID", value=st.session_state.student_name)
    st.session_state.student_name = student_name_input.strip() or "Anonymous Learner"

    # 2. Regional Spoken Language (All 9 languages from config)
    lang_keys = list(LANGUAGES.keys())
    language_choice = st.selectbox(
        "🌐 Regional Spoken Language",
        options=lang_keys,
        format_func=lambda x: f"{LANGUAGES[x]['native_name']} ({x})"
    )
    current_lang = LANGUAGES[language_choice]
    st.caption(f"🎙️ Neural Voice: `{current_lang['voice']}`")
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)

    # Demo Mode Checkbox
    demo_mode = st.checkbox(
        "🎯 Demo mode",
        value=st.session_state.get("demo_mode", False),
        help="Preloads sample questions for the current subject as one-click buttons."
    )
    st.session_state.demo_mode = demo_mode

    if demo_mode:
        st.markdown("<p style='font-size:0.75rem; letter-spacing:0.15em; text-transform:uppercase; color:#9CA3AF; margin-top:8px;'>Sample Prompts</p>", unsafe_allow_html=True)
        curr_subj_name = st.session_state.active_subject['name'] if st.session_state.active_subject else "General"
        demo_qs_sb = get_demo_questions(curr_subj_name, st.session_state.indexed_chunks, language_choice)
        for d_i, d_q in enumerate(demo_qs_sb):
            if st.button(f"👉 {d_q}", key=f"sb_demo_btn_{d_i}", use_container_width=True):
                st.session_state.demo_query_triggered = d_q
                st.rerun()

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)

    # 3. Textbook Upload & Indexing
    st.markdown(
        """
        <p style='font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.15em; color:#9CA3AF;'>
            Textbook Chapter
        </p>
        """,
        unsafe_allow_html=True
    )
    upload_subject_name = st.text_input("Subject / Chapter Name", placeholder="e.g. Science - Life Processes")
    uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"], help="Select a textbook chapter PDF")

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_hash = library.compute_file_hash(file_bytes)
        
        # Hash deduplication check
        existing_subject = library.get_subject_by_hash(file_hash)
        if existing_subject:
            st.info(f"ℹ️ **Already saved**: '{existing_subject['name']}' ({existing_subject['num_pages']} pages, {existing_subject['num_chunks']} passages).")
            if st.button("📂 Load This Saved Subject", use_container_width=True):
                activate_subject(existing_subject)
                st.rerun()
        else:
            if st.button("🚀 Index & Save to Library", use_container_width=True, type="primary"):
                subj_title = upload_subject_name.strip() or uploaded_file.name.replace(".pdf", "")
                with st.spinner("Extracting text and building multilingual FAISS index..."):
                    try:
                        chunks, num_pages = ingest.extract_chunks_from_pdf(file_bytes)
                        emb_model = load_embedding_model()
                        if emb_model is None:
                            st.error("Failed to load embedding model.")
                        else:
                            texts = [c["text"] for c in chunks]
                            embeddings = retrieval.encode_passages(texts, emb_model)
                            new_subj_id = str(uuid.uuid4())[:8]
                            index_dir_path = ingest.build_and_save_index(new_subj_id, chunks, embeddings)
                            saved_sub = library.save_subject(
                                subject_id=new_subj_id,
                                name=subj_title,
                                file_hash=file_hash,
                                filename=uploaded_file.name,
                                num_chunks=len(chunks),
                                num_pages=num_pages,
                                index_path=str(index_dir_path)
                            )
                            activate_subject(saved_sub)
                            st.success(f"Indexed {len(chunks)} passages from {num_pages} pages!")
                            st.rerun()
                    except ValueError as ve:
                        st.error(f"❌ Document Error: {str(ve)}")
                    except Exception as e:
                        st.error(f"❌ Indexing Failed: {str(e)}")

    # Quick Demo Chapter Loader
    if st.button("📚 Load NCERT Demo Chapter", use_container_width=True):
        if not DEFAULT_SAMPLE_PDF.exists():
            import create_sample_pdf
            create_sample_pdf.generate_sample_chapter_pdf(str(DEFAULT_SAMPLE_PDF))
        
        with open(DEFAULT_SAMPLE_PDF, "rb") as f:
            demo_bytes = f.read()
        demo_hash = library.compute_file_hash(demo_bytes)
        demo_sub = library.get_subject_by_hash(demo_hash)
        
        if demo_sub:
            activate_subject(demo_sub)
            st.success("Loaded demo subject from registry!")
            st.rerun()
        else:
            with st.spinner("Indexing NCERT Science demo chapter..."):
                try:
                    chunks, num_pages = ingest.extract_chunks_from_pdf(demo_bytes)
                    emb_model = load_embedding_model()
                    texts = [c["text"] for c in chunks]
                    embeddings = retrieval.encode_passages(texts, emb_model)
                    demo_id = "ncert_science_demo"
                    p = ingest.build_and_save_index(demo_id, chunks, embeddings)
                    saved = library.save_subject(
                        subject_id=demo_id,
                        name="NCERT Class 10 Science - Life Processes",
                        file_hash=demo_hash,
                        filename="sample_chapter.pdf",
                        num_chunks=len(chunks),
                        num_pages=num_pages,
                        index_path=str(p)
                    )
                    activate_subject(saved)
                    st.success("Demo chapter indexed and activated!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"Error loading demo: {ex}")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
    
    # Active Subject Indicator
    if st.session_state.active_subject:
        subj = st.session_state.active_subject
        st.markdown(
            f"""
            <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 12px 14px;">
                <div style="display:flex; align-items:center; gap:6px; color:#10B981; font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.1em;">
                    <span class="pulse-dot"></span> Active Chapter
                </div>
                <div style="font-weight:600; color:#F3F4F6; margin-top:4px; font-size:0.88rem;">{subj['name']}</div>
                <div style="color:#9CA3AF; font-size:0.76rem; font-family:'JetBrains Mono', monospace; margin-top:2px;">
                    {subj['num_pages']} Pages • {subj['num_chunks']} Chunks
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ No subject loaded. Upload a PDF or click 'Load NCERT Demo'.")

# ==========================================
# FIXED NAVIGATION PILL
# ==========================================
st.markdown(
    """
    <div class="nav-pill-container">
        <div class="nav-pill">
            <div class="nav-brand">
                <span class="nav-dot"></span>
                <span class="nav-title">VidyaVaani</span>
            </div>
            <div class="nav-links">
                <span>VOICE RAG</span>
                <span>•</span>
                <span>9 INDIC VOICES</span>
                <span>•</span>
                <span>GROUNDED</span>
            </div>
            <div class="nav-cta">
                <span class="pulse-dot"></span>
                <span>OPERATIONAL</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# HERO SECTION (Synapse Editorial)
# ==========================================
active_subj_name = st.session_state.active_subject['name'] if st.session_state.active_subject else "No Chapter Loaded"

st.markdown(
    f"""
    <div class="hero-container">
        <h1 class="hero-heading">
            Voices of Learning, <span class="shimmer-text">Grounded</span> in Knowledge
        </h1>
        <p class="hero-subtext">
            A high-fidelity multilingual voice tutor engineered for educational equity. Strict textbook RAG, real-time regional neural speech, and zero hallucinations.
        </p>
        <div class="hero-badges-row">
            <span class="synapse-badge">👤 {st.session_state.student_name}</span>
            <span class="synapse-badge">🌐 {current_lang['label']}</span>
            <span class="synapse-badge">📚 {active_subj_name}</span>
            <span class="synapse-badge">⚡ Gemini 3.8 Flash</span>
            <span class="synapse-badge">🗣️ Neural Edge-TTS</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# INFINITE METRICS TICKER
# ==========================================
st.markdown(
    """
    <div class="ticker-wrapper">
        <div class="ticker-track">
            <div class="ticker-item"><span class="ticker-label">REASONING:</span><span class="ticker-value ticker-accent-violet">GEMINI 3.8 FLASH</span></div>
            <div class="ticker-item"><span class="ticker-label">RETRIEVAL:</span><span class="ticker-value ticker-accent-cyan">FAISS DENSE COSINE</span></div>
            <div class="ticker-item"><span class="ticker-label">EMBEDDINGS:</span><span class="ticker-value">MULTILINGUAL-E5</span></div>
            <div class="ticker-item"><span class="ticker-label">TTS ENGINE:</span><span class="ticker-value ticker-accent-violet">AZURE NEURAL (EDGE)</span></div>
            <div class="ticker-item"><span class="ticker-label">LANGUAGES:</span><span class="ticker-value ticker-accent-emerald">9 REGIONAL INDIC</span></div>
            <div class="ticker-item"><span class="ticker-label">ACCURACY:</span><span class="ticker-value">MANDATORY CITATIONS</span></div>
            <div class="ticker-item"><span class="ticker-label">STATUS:</span><span class="ticker-value ticker-accent-emerald">ACTIVE & GROUNDED</span></div>
            <!-- Duplicate for seamless infinite loop -->
            <div class="ticker-item"><span class="ticker-label">REASONING:</span><span class="ticker-value ticker-accent-violet">GEMINI 3.8 FLASH</span></div>
            <div class="ticker-item"><span class="ticker-label">RETRIEVAL:</span><span class="ticker-value ticker-accent-cyan">FAISS DENSE COSINE</span></div>
            <div class="ticker-item"><span class="ticker-label">EMBEDDINGS:</span><span class="ticker-value">MULTILINGUAL-E5</span></div>
            <div class="ticker-item"><span class="ticker-label">TTS ENGINE:</span><span class="ticker-value ticker-accent-violet">AZURE NEURAL (EDGE)</span></div>
            <div class="ticker-item"><span class="ticker-label">LANGUAGES:</span><span class="ticker-value ticker-accent-emerald">9 REGIONAL INDIC</span></div>
            <div class="ticker-item"><span class="ticker-label">ACCURACY:</span><span class="ticker-value">MANDATORY CITATIONS</span></div>
            <div class="ticker-item"><span class="ticker-label">STATUS:</span><span class="ticker-value ticker-accent-emerald">ACTIVE & GROUNDED</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 3-COLUMN INTERACTIVE FEATURE CARDS
# ==========================================
st.markdown(
    """
    <div class="synapse-feature-grid">
        <div class="synapse-card">
            <div class="card-icon-box">🎙️</div>
            <div class="card-title">Regional Neural Voice</div>
            <div class="card-body">Natural speech synthesis across 9 Indian languages. Every concept is spoken aloud in warm, native dialect accents.</div>
        </div>
        <div class="synapse-card">
            <div class="card-icon-box">🛡️</div>
            <div class="card-title">Strict Grounding & Refusal</div>
            <div class="card-body">Zero external hallucination. All answers cite verified textbook pages, and off-topic questions trigger polite translated refusals.</div>
        </div>
        <div class="synapse-card">
            <div class="card-icon-box">💡</div>
            <div class="card-title">Scaffolding for Learners</div>
            <div class="card-body">One-click 'Explain Simpler' rewrites jargon into gentle analogies, while 'Give an Example' connects concepts to Indian daily life.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# TRANSLATED TABS
# ==========================================
ui = current_lang["ui"]
tab_ask, tab_quiz, tab_subjects, tab_analytics = st.tabs([
    ui["ask_tab"],
    ui["quiz_tab"],
    ui["library_tab"],
    "📊 Teacher Analytics"
])

# ==============================================================================
# TAB 1: 🗣️ ASK TUTOR
# ==============================================================================
with tab_ask:
    st.markdown(
        f"""
        <div style="margin-bottom: 16px;">
            <div style="font-family:'Instrument Serif', Georgia, serif; font-size: 1.8rem; color:#FFFFFF;">
                Ask your question in {current_lang['label']}
            </div>
            <div style="color:#9CA3AF; font-size:0.9rem;">
                Speak or type. VidyaVaani answers with spoken regional audio and textbook citations.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Greeting Banner
    st.markdown(
        f"""
        <div style="background: rgba(139, 92, 246, 0.08); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 14px; padding: 12px 18px; margin-bottom: 16px; color: #E9D5FF; font-size: 0.95rem;">
            💬 {current_lang['greeting']}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Voice Input (if mic recorder available)
    voice_query_text = None
    if speech_to_text is not None:
        col_mic, col_mic_info = st.columns([1, 4])
        with col_mic:
            voice_query_text = speech_to_text(
                language=current_lang.get("bcp47", "en-IN"),
                start_prompt="🎙️ Speak Question",
                stop_prompt="⏹️ Stop Recording",
                key="synapse_mic_recorder"
            )
        with col_mic_info:
            if voice_query_text:
                st.success(f"Recognized Voice: *\"{voice_query_text}\"*")

    # Text Query Form
    with st.form("ask_form", clear_on_submit=False):
        col_in, col_btn = st.columns([4, 1])
        with col_in:
            user_text = st.text_input(
                "Question",
                value=voice_query_text or "",
                placeholder=ui["ask_placeholder"],
                label_visibility="collapsed"
            )
        with col_btn:
            ask_submitted = st.form_submit_button(ui["ask_btn"], type="primary", use_container_width=True)

    # Demo Mode One-Click Questions
    tab_demo_selected = None
    if st.session_state.get("demo_mode", False):
        curr_subj_name = st.session_state.active_subject['name'] if st.session_state.active_subject else "General"
        demo_qs_tab = get_demo_questions(curr_subj_name, st.session_state.indexed_chunks, language_choice)
        st.markdown(
            """
            <div style="background: rgba(6, 182, 212, 0.08); border: 1px solid rgba(6, 182, 212, 0.2); padding: 10px 16px; border-radius: 12px; margin: 10px 0;">
                <span style="color: #22D3EE; font-weight: 600; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.1em;">
                    ⚡ One-Click Presentation Prompts
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        d_c1, d_c2 = st.columns(2)
        for d_i, d_q in enumerate(demo_qs_tab):
            t_col = d_c1 if d_i % 2 == 0 else d_c2
            with t_col:
                if st.button(f"✨ {d_q}", key=f"tab_demo_btn_{d_i}", use_container_width=True):
                    tab_demo_selected = d_q

    # Pedagogical Scaffolding Quick Action Buttons
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        btn_simpler = st.button(ui["simpler_btn"], use_container_width=True)
    with col_s2:
        btn_example = st.button(ui["example_btn"], use_container_width=True)
    with col_s3:
        btn_sample_1 = st.button("🌱 What is Photosynthesis?", use_container_width=True)
    with col_s4:
        btn_sample_2 = st.button("🫀 Respiration & Energy", use_container_width=True)

    # Determine Query
    triggered_query = None
    action_type = "normal"

    if tab_demo_selected:
        triggered_query = tab_demo_selected
    elif st.session_state.get("demo_query_triggered"):
        triggered_query = st.session_state.pop("demo_query_triggered")
    elif ask_submitted and user_text.strip():
        triggered_query = user_text.strip()
    elif btn_simpler:
        action_type = "simpler"
        triggered_query = user_text.strip() or st.session_state.last_query or "Explain the main topic of this chapter"
    elif btn_example:
        action_type = "example"
        triggered_query = user_text.strip() or st.session_state.last_query or "Give a real-world example of this concept"
    elif btn_sample_1:
        triggered_query = "What is photosynthesis and what are its steps?"
    elif btn_sample_2:
        triggered_query = "What is the difference between aerobic and anaerobic respiration?"

    # Execute RAG Pipeline
    if triggered_query:
        if not st.session_state.indexed_chunks or st.session_state.faiss_index is None:
            st.error(ui["no_subject_alert"])
        else:
            with st.spinner("Searching textbook vector index and reasoning with Gemini..."):
                emb_model = load_embedding_model()
                top_chunks, top_score = retrieval.search_similar_chunks(
                    query=triggered_query,
                    chunks=st.session_state.indexed_chunks,
                    index=st.session_state.faiss_index,
                    model=emb_model,
                    k=TOP_K
                )

                answer = llm.generate_tutor_response(
                    query=triggered_query,
                    context_chunks=top_chunks,
                    language_key=language_choice,
                    action_type=action_type,
                    top_score=top_score
                )

                audio_file = speech.synthesize_speech(
                    text=answer,
                    language_key=language_choice
                )

                # Persist to database
                subj_id = st.session_state.active_subject["id"] if st.session_state.active_subject else None
                library.log_interaction(
                    student_name=st.session_state.student_name,
                    language=language_choice,
                    query=triggered_query,
                    response=answer,
                    subject_id=subj_id
                )

                st.session_state.last_query = triggered_query
                st.session_state.last_response = answer
                st.session_state.last_sources = top_chunks
                st.session_state.last_audio_path = audio_file

    # Render High-Tech Dark IDE-Style Tutor Response
    if st.session_state.last_response:
        st.markdown(
            f"""
            <div class="ide-window">
                <div class="ide-toolbar">
                    <div class="ide-controls">
                        <span class="control-dot dot-red"></span>
                        <span class="control-dot dot-yellow"></span>
                        <span class="control-dot dot-green"></span>
                    </div>
                    <div class="ide-filename">vidyavaani.response • {current_lang['label']}</div>
                    <div class="ide-status">
                        <span class="pulse-dot"></span>
                        <span>GROUNDED</span>
                    </div>
                </div>
                <div class="ide-content">
                    {st.session_state.last_response.replace(chr(10), '<br>')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Audio Player with Ambient Frame
        if st.session_state.last_audio_path and os.path.exists(st.session_state.last_audio_path):
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:8px; margin: 8px 0;">
                    <span style="font-family:'Instrument Serif', Georgia, serif; font-size:1.25rem; color:#A78BFA;">🎙️ {ui['audio_label']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            with open(st.session_state.last_audio_path, "rb") as af:
                st.audio(af.read(), format="audio/mp3")

        # Grounding Passages Expander
        with st.expander(ui["sources_title"], expanded=False):
            if st.session_state.last_sources:
                for idx, src in enumerate(st.session_state.last_sources):
                    st.markdown(
                        f"""
                        <div class="synapse-passage">
                            <div class="synapse-passage-header">PASSAGE #{idx+1} — [PAGE {src['page']}] • SIMILARITY: {src.get('score', 0):.3f}</div>
                            <div style="color: #D1D5DB; font-size: 0.9rem; line-height: 1.5;">"{src['text']}"</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.write("No matching passages found.")

# ==============================================================================
# TAB 2: 📝 PRACTICE QUIZ
# ==============================================================================
with tab_quiz:
    st.markdown(
        f"""
        <div style="font-family:'Instrument Serif', Georgia, serif; font-size: 1.8rem; color:#FFFFFF; margin-bottom: 4px;">
            {ui['quiz_title']}
        </div>
        <div style="color:#9CA3AF; font-size:0.9rem; margin-bottom: 16px;">
            5 multiple-choice questions grounded strictly in the active textbook chapter.
        </div>
        """,
        unsafe_allow_html=True
    )

    col_qbtn, col_qinfo = st.columns([1, 2])
    with col_qbtn:
        if st.button(ui["quiz_gen_btn"], type="primary", use_container_width=True):
            if not st.session_state.indexed_chunks:
                st.warning(ui["no_subject_alert"])
            else:
                with st.spinner("Generating 5 chapter questions with Gemini 3.8 Flash..."):
                    qdata = quiz.generate_chapter_quiz(
                        chunks=st.session_state.indexed_chunks,
                        language_key=language_choice
                    )
                    st.session_state.quiz_data = qdata
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = 0
                    st.rerun()

    if st.session_state.quiz_data:
        st.markdown("<hr style='border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
        with st.form("quiz_form"):
            user_choices = {}
            for item in st.session_state.quiz_data:
                st.markdown(
                    f"""
                    <div style="font-family:'Instrument Serif', Georgia, serif; font-size: 1.25rem; color:#FFFFFF; margin-top: 14px;">
                        Q{item['id']}: {item['question']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                choice = st.radio(
                    f"Options for Q{item['id']}:",
                    options=item["options"],
                    key=f"quiz_opt_{item['id']}",
                    index=None,
                    label_visibility="collapsed"
                )
                user_choices[item["id"]] = choice
                st.write("")

            submit_quiz = st.form_submit_button(ui["quiz_submit_btn"], type="primary")

        if submit_quiz:
            score = 0
            total = len(st.session_state.quiz_data)
            feedback_list = []

            for item in st.session_state.quiz_data:
                chosen = user_choices.get(item["id"])
                chosen_letter = chosen[0].upper() if chosen else ""
                expected_letter = item["answer"].strip().upper()
                is_correct = (chosen_letter == expected_letter)

                if is_correct:
                    score += 1

                feedback_list.append({
                    "id": item["id"],
                    "question": item["question"],
                    "chosen": chosen or "Not Answered",
                    "correct": expected_letter,
                    "is_correct": is_correct,
                    "explanation": item.get("explanation", ""),
                    "page": item.get("page", 1)
                })

            st.session_state.quiz_submitted = True
            st.session_state.quiz_score = score
            pct = round((score / total) * 100, 1)

            # Log score to database
            subj_id = st.session_state.active_subject["id"] if st.session_state.active_subject else None
            library.log_quiz(
                student_name=st.session_state.student_name,
                score=score,
                total=total,
                subject_id=subj_id
            )

            # Score Banner
            st.markdown("<hr style='border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
            if pct >= 80:
                st.balloons()
                st.success(f"🎉 Outstanding, {st.session_state.student_name}! Score: **{score}/{total} ({pct}%)**")
            elif pct >= 50:
                st.info(f"👍 Good effort, {st.session_state.student_name}! Score: **{score}/{total} ({pct}%)**. Review your textbook to reach 100%!")
            else:
                st.warning(f"📚 Score: **{score}/{total} ({pct}%)**. Ask VidyaVaani to explain simpler and retry!")

            # Review Details
            st.markdown("#### Question-by-Question Review:")
            for f in feedback_list:
                status_text = "✅ Correct" if f["is_correct"] else "❌ Incorrect"
                color = "#10B981" if f["is_correct"] else "#EF4444"
                st.markdown(
                    f"""
                    <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 14px 18px; margin-bottom: 10px;">
                        <div style="font-weight: 600; color: #FFFFFF;">Q{f['id']}: {f['question']}</div>
                        <div style="margin-top: 4px;">
                            <span style="color: {color}; font-weight: 700;">{status_text}</span> • Your Answer: <code>{f['chosen']}</code> • Correct: <code>Option {f['correct']}</code>
                        </div>
                        <div style="font-size: 0.85rem; color: #9CA3AF; margin-top: 4px;">
                            💡 <em>{f['explanation']} [Page {f['page']}]</em>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("Click 'Generate / Refresh Quiz' above to create questions from your active textbook.")

# ==============================================================================
# TAB 3: 📚 MY SUBJECTS LIBRARY
# ==============================================================================
with tab_subjects:
    st.markdown(
        """
        <div style="font-family:'Instrument Serif', Georgia, serif; font-size: 1.8rem; color:#FFFFFF; margin-bottom: 4px;">
            My Subjects Library
        </div>
        <div style="color:#9CA3AF; font-size:0.9rem; margin-bottom: 20px;">
            Manage saved textbooks, re-index documents, or activate another subject.
        </div>
        """,
        unsafe_allow_html=True
    )

    all_subjects = library.list_subjects()
    if not all_subjects:
        st.info("No subjects registered yet. Upload a PDF or click 'Load NCERT Demo' in the sidebar.")
    else:
        for subj in all_subjects:
            is_active = (
                st.session_state.active_subject is not None
                and st.session_state.active_subject["id"] == subj["id"]
            )
            col_info, col_act1, col_act2, col_act3 = st.columns([4, 1.2, 1.2, 1.2])
            
            with col_info:
                active_badge = " 🟢 <span style='color:#10B981; font-size:0.85rem; font-family:sans-serif;'>(Active)</span>" if is_active else ""
                st.markdown(f"<h3 style='margin:0; font-family:\"Instrument Serif\", serif;'>{subj['name']}{active_badge}</h3>", unsafe_allow_html=True)
                st.caption(f"File: `{subj['filename']}` • Pages: {subj['num_pages']} • Chunks: {subj['num_chunks']} • Saved: {subj['created_at']}")
            
            with col_act1:
                if not is_active:
                    if st.button("📂 Load", key=f"load_{subj['id']}", use_container_width=True):
                        activate_subject(subj)
                        st.rerun()
                else:
                    st.button("✓ Loaded", key=f"active_{subj['id']}", disabled=True, use_container_width=True)

            with col_act2:
                if st.button("🔄 Re-index", key=f"reindex_{subj['id']}", use_container_width=True):
                    with st.spinner(f"Re-indexing '{subj['name']}'..."):
                        try:
                            _, current_chunks = ingest.load_saved_index(subj["id"])
                            if current_chunks:
                                emb_model = load_embedding_model()
                                texts = [c["text"] for c in current_chunks]
                                embeddings = retrieval.encode_passages(texts, emb_model)
                                ingest.build_and_save_index(subj["id"], current_chunks, embeddings)
                                if is_active:
                                    activate_subject(subj)
                                st.success("Re-indexed successfully!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Re-indexing failed: {e}")

            with col_act3:
                if st.button("🗑️ Delete", key=f"del_{subj['id']}", use_container_width=True):
                    library.delete_subject(subj["id"])
                    if is_active:
                        st.session_state.active_subject = None
                        st.session_state.faiss_index = None
                        st.session_state.indexed_chunks = []
                    st.success(f"Deleted '{subj['name']}'")
                    st.rerun()

            st.markdown("<hr style='border-color: rgba(255,255,255,0.04); margin: 12px 0;'>", unsafe_allow_html=True)

# ==============================================================================
# TAB 4: 📊 TEACHER ANALYTICS
# ==============================================================================
with tab_analytics:
    st.markdown(
        """
        <div style="font-family:'Instrument Serif', Georgia, serif; font-size: 1.8rem; color:#FFFFFF; margin-bottom: 4px;">
            VidyaVaani Learning Analytics
        </div>
        <div style="color:#9CA3AF; font-size:0.9rem; margin-bottom: 20px;">
            Teacher and administrative metrics: student query audit, regional language spread, and quiz mastery.
        </div>
        """,
        unsafe_allow_html=True
    )

    with library.get_connection() as conn:
        q_count = conn.execute("SELECT COUNT(*) FROM interactions").fetchone()[0] or 0
        s_count = conn.execute(
            """
            SELECT COUNT(DISTINCT name) FROM (
                SELECT student_name AS name FROM interactions
                UNION
                SELECT student_name AS name FROM quiz_results
            )
            """
        ).fetchone()[0] or 0
        avg_score_row = conn.execute(
            "SELECT AVG(CAST(score AS FLOAT) / CASE WHEN total > 0 THEN total ELSE 1 END * 100) FROM quiz_results"
        ).fetchone()[0]
        avg_score = round(avg_score_row, 1) if avg_score_row is not None else 0.0
        top_l_row = conn.execute("SELECT language, COUNT(*) as c FROM interactions GROUP BY language ORDER BY c DESC LIMIT 1").fetchone()
        top_lang = top_l_row[0] if top_l_row else "English"

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Total Inquiries", q_count)
    col_m2.metric("Active Learners", s_count)
    col_m3.metric("Average Score", f"{avg_score}%")
    col_m4.metric("Top Language", top_lang)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 24px 0;'>", unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("<div style='font-family:\"Instrument Serif\", serif; font-size: 1.3rem; margin-bottom: 8px;'>Regional Language Breakdown</div>", unsafe_allow_html=True)
        with library.get_connection() as conn:
            lang_df = pd.read_sql_query("SELECT language, COUNT(*) as count FROM interactions GROUP BY language ORDER BY count DESC", conn)
        if not lang_df.empty:
            st.bar_chart(lang_df.set_index("language")["count"], color="#8B5CF6")
        else:
            st.info("No questions logged yet.")

    with col_c2:
        st.markdown("<div style='font-family:\"Instrument Serif\", serif; font-size: 1.3rem; margin-bottom: 8px;'>Quiz Score Mastery Distribution</div>", unsafe_allow_html=True)
        with library.get_connection() as conn:
            quiz_df = pd.read_sql_query("SELECT student_name, ROUND((CAST(score AS FLOAT)/total)*100, 1) as percentage FROM quiz_results ORDER BY id DESC LIMIT 20", conn)
        if not quiz_df.empty:
            st.bar_chart(quiz_df.set_index("student_name")["percentage"], color="#10B981")
        else:
            st.info("No quiz scores logged yet.")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 24px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:\"Instrument Serif\", serif; font-size: 1.3rem; margin-bottom: 12px;'>Recent Inquiry Audit Log</div>", unsafe_allow_html=True)
    with library.get_connection() as conn:
        logs_df = pd.read_sql_query("SELECT id, student_name, language, query, response, timestamp FROM interactions ORDER BY id DESC LIMIT 50", conn)
    if not logs_df.empty:
        st.dataframe(logs_df, use_container_width=True, hide_index=True)
    else:
        st.info("No activity logged yet.")

# ==========================================
# SYNAPSE FOOTER
# ==========================================
st.markdown(
    """
    <footer class="synapse-footer">
        <div class="footer-grid">
            <div>
                <div class="footer-brand-title">VidyaVaani</div>
                <div style="color: #9CA3AF; font-size: 0.88rem; max-width: 320px; line-height: 1.5; font-weight: 300;">
                    Futuristic voice-first educational equity for school learners. Grounded in NCERT textbooks with Microsoft Azure neural Indian accents.
                </div>
            </div>
            <div>
                <div class="footer-col-head">Core Engine</div>
                <div class="footer-link">Gemini 3.8 Flash</div>
                <div class="footer-link">FAISS Vector Index</div>
                <div class="footer-link">Multilingual-E5</div>
            </div>
            <div>
                <div class="footer-col-head">Speech & TTS</div>
                <div class="footer-link">Microsoft Edge-TTS</div>
                <div class="footer-link">9 Regional Accents</div>
                <div class="footer-link">Low-Latency Audio</div>
            </div>
            <div>
                <div class="footer-col-head">Architecture</div>
                <div class="footer-link">Decoupled Backend</div>
                <div class="footer-link">SQLite Audit Layer</div>
                <div class="footer-link">Synapse Design System</div>
            </div>
        </div>
        <div class="footer-bottom-bar">
            <div>© 2026 VidyaVaani • Synapse System. Educational Equity for Every Learner.</div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="pulse-dot"></span>
                <span style="color: #10B981; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">ALL SYSTEMS OPERATIONAL</span>
            </div>
        </div>
    </footer>
    """,
    unsafe_allow_html=True
)
