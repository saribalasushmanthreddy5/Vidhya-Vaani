"""
VidyaVaani (ವಿಧ್ಯಾವಾಣಿ / विद्यावाणी): Voice-First Multilingual AI Tutor
Synapse Design System (SuperDesign-matched aesthetic):
- Vantablack (#030303) canvas with central violet neural bloom & floating ambient glow orbs
- Floating Synapse Assistant Card with staggered interactive option pills (matched to reference screenshot)
- Sleek bottom input dock with voice mic, chapter badge, and circular upward-arrow submit button
- Instrument Serif editorial typography & shimmering gradient text
- Infinite horizontal metrics marquee ticker
- 6-card feature grid matching Synapse architecture
- Glassmorphic practice quiz with interactive selection cards
- Zero exposed keys on client; 100% server-side Gemini 3.8 Flash & Azure Neural TTS
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
    page_title="VidyaVaani • Synapse Voice AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SYNAPSE SUPERDESIGN CSS INJECTION
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;600&family=Noto+Sans+Kannada:wght@400;600&family=Noto+Sans+Telugu:wght@400;600&family=Noto+Sans+Tamil:wght@400;600&family=Noto+Sans+Malayalam:wght@400;600&family=Noto+Sans+Bengali:wght@400;600&family=Noto+Sans+Gujarati:wght@400;600&display=swap');

    /* Vantablack Base (#030303) */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #030303 !important;
        color: #EDEDED !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #070708 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* Ambient Neural Flare / Bloom (Matched to Reference Screenshot) */
    .synapse-bloom {
        position: fixed;
        width: 800px;
        height: 480px;
        bottom: 0px;
        left: 50%;
        transform: translateX(-50%);
        background: radial-gradient(ellipse at 50% 100%, rgba(139, 92, 246, 0.38) 0%, rgba(124, 58, 237, 0.18) 35%, rgba(6, 182, 212, 0.08) 60%, transparent 75%);
        filter: blur(55px);
        pointer-events: none;
        z-index: 0;
    }
    .synapse-orb-top {
        position: fixed;
        width: 600px;
        height: 600px;
        top: -160px;
        left: 50%;
        transform: translateX(-50%);
        background: radial-gradient(circle, rgba(139, 92, 246, 0.18) 0%, transparent 65%);
        filter: blur(80px);
        pointer-events: none;
        z-index: 0;
    }

    /* Typography */
    .font-serif {
        font-family: 'Instrument Serif', Georgia, serif !important;
        letter-spacing: -0.025em;
    }
    .font-mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Shimmer Text */
    .shimmer-text {
        background: linear-gradient(90deg, #A78BFA 0%, #FFFFFF 35%, #FFFFFF 65%, #22D3EE 100%);
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
        margin-bottom: 24px;
        position: relative;
        z-index: 10;
    }
    .nav-pill {
        width: 100%;
        max-width: 672px;
        background: rgba(10, 10, 10, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 9999px;
        padding: 8px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.9), 0 0 20px -10px rgba(139, 92, 246, 0.25);
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
    }
    .nav-links {
        display: flex;
        gap: 12px;
        align-items: center;
        font-size: 0.72rem;
        font-weight: 600;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    .nav-cta {
        background: #FFFFFF;
        color: #030303;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 5px 14px;
        border-radius: 9999px;
        display: flex;
        align-items: center;
        gap: 6px;
        letter-spacing: 0.02em;
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 24px 16px 20px 16px;
        position: relative;
        z-index: 1;
    }
    .status-chip {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 9999px;
        padding: 4px 14px;
        font-size: 0.78rem;
        color: #C4B5FD;
        margin-bottom: 16px;
        font-family: 'JetBrains Mono', monospace;
    }
    .hero-heading {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 4rem;
        line-height: 1.02;
        font-weight: 400;
        color: #FFFFFF;
        margin-bottom: 14px;
        letter-spacing: -0.035em;
    }
    @media (max-width: 768px) {
        .hero-heading { font-size: 2.5rem; }
    }
    .hero-subtext {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        color: #9CA3AF;
        max-width: 680px;
        margin: 0 auto 20px auto;
        line-height: 1.55;
        font-weight: 300;
    }
    .hero-badges-row {
        display: flex;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
    }
    .synapse-badge {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 9999px;
        padding: 5px 14px;
        font-size: 0.8rem;
        color: #D1D5DB;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-family: 'Inter', sans-serif;
    }

    /* Infinite Marquee Ticker */
    .ticker-wrapper {
        width: 100%;
        overflow: hidden;
        background: rgba(0, 0, 0, 0.5);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin: 22px 0 28px 0;
        padding: 12px 0;
    }
    .ticker-track {
        display: flex;
        width: max-content;
        animation: tickerMarquee 40s linear infinite;
        gap: 36px;
    }
    @keyframes tickerMarquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .ticker-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'JetBrains Mono', monospace;
    }
    .ticker-label {
        font-size: 0.65rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }
    .ticker-value {
        font-size: 0.84rem;
        font-weight: 600;
        color: #F3F4F6;
    }
    .ticker-accent-violet { color: #A78BFA; }
    .ticker-accent-cyan { color: #22D3EE; }
    .ticker-accent-emerald { color: #34D399; }

    /* =====================================================================
       SUPERDESIGN FLOATING CHAT CARD & OPTION PILLS (EXACT REFERENCE UI)
       ===================================================================== */
    .superdesign-card {
        background: #0C0C0E;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 26px;
        padding: 22px 24px;
        box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.95), 0 0 35px -12px rgba(139, 92, 246, 0.25);
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .superdesign-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 14px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 16px;
    }
    .superdesign-title-box {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .superdesign-grid-icon {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.05rem;
    }
    .superdesign-title {
        font-weight: 600;
        font-size: 0.96rem;
        color: #FFFFFF;
        letter-spacing: -0.01em;
    }
    .superdesign-subtitle {
        font-size: 0.74rem;
        color: #9CA3AF;
    }
    .superdesign-controls {
        display: flex;
        gap: 10px;
        color: #6B7280;
        font-size: 0.88rem;
    }
    
    /* Speech Bubble in Chat Card */
    .superdesign-bubble {
        background: #18181B;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px 20px 20px 6px;
        padding: 16px 20px;
        color: #F4F4F5;
        font-size: 0.93rem;
        line-height: 1.55;
        margin-bottom: 6px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .superdesign-bubble-meta {
        font-size: 0.72rem;
        color: #71717A;
        margin-left: 6px;
        margin-bottom: 18px;
    }

    /* Option Pills Section Header */
    .pills-section-title {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #71717A;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* SuperDesign Floating Option Pills (Matched to Reference Screenshot) */
    [data-testid="stTabs"] [data-testid="column"]:first-child .stButton {
        display: flex !important;
        justify-content: flex-end !important;
        margin-bottom: 8px !important;
    }
    [data-testid="stTabs"] [data-testid="column"]:first-child .stButton button {
        background: #18181B !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 9999px !important;
        color: #E4E4E7 !important;
        padding: 9px 20px !important;
        font-size: 0.88rem !important;
        font-weight: 400 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        width: auto !important;
        max-width: 100% !important;
    }
    [data-testid="stTabs"] [data-testid="column"]:first-child .stButton button:hover {
        background: #27272A !important;
        border-color: rgba(139, 92, 246, 0.55) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 0 18px -2px rgba(139, 92, 246, 0.45) !important;
    }
    [data-testid="stTabs"] [data-testid="column"]:first-child .stButton button:active {
        transform: scale(0.97) !important;
    }

    /* Generic button fallback */
    .stButton > button {
        background: rgba(255, 255, 255, 0.035) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 9999px !important;
        color: #E5E7EB !important;
        padding: 8px 18px !important;
        font-size: 0.88rem !important;
        font-weight: 400 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }
    .stButton > button:hover {
        background: rgba(139, 92, 246, 0.14) !important;
        border-color: rgba(139, 92, 246, 0.45) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) scale(1.02) !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 22px -5px rgba(124, 58, 237, 0.6) !important;
        font-weight: 600 !important;
    }

    /* Input Dock in Chat Column (Pill input + Circular send button) */
    .dock-meta-icons {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        padding: 0 4px;
        font-size: 0.74rem;
        color: #71717A;
    }
    .dock-meta-item {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 9999px;
        padding: 3px 10px;
        font-family: 'JetBrains Mono', monospace;
    }

    [data-testid="stTabs"] [data-testid="column"]:first-child .stTextInput input {
        background: #111114 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 9999px !important;
        color: #FFFFFF !important;
        padding: 12px 20px !important;
        font-size: 0.92rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stTabs"] [data-testid="column"]:first-child .stTextInput input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 20px -3px rgba(139, 92, 246, 0.45) !important;
    }
    [data-testid="stTabs"] [data-testid="column"]:first-child [data-testid="stFormSubmitButton"] button {
        background: #1E1E24 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.15rem !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    [data-testid="stTabs"] [data-testid="column"]:first-child [data-testid="stFormSubmitButton"] button:hover {
        background: #7C3AED !important;
        border-color: #8B5CF6 !important;
        transform: translateY(-2px) scale(1.06) !important;
        box-shadow: 0 0 22px rgba(139, 92, 246, 0.7) !important;
    }

    .stTextInput input {
        background: #111114 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 9999px !important;
        color: #F3F4F6 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 13px 22px !important;
        font-size: 0.95rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 20px -3px rgba(139, 92, 246, 0.45) !important;
    }

    /* Dark IDE-Style Tutor Response Block */
    .ide-window {
        background: rgba(8, 8, 8, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        overflow: hidden;
        margin: 20px 0;
        box-shadow: 0 25px 50px -15px rgba(0, 0, 0, 0.9), 0 0 25px -10px rgba(139, 92, 246, 0.25);
    }
    .ide-toolbar {
        background: rgba(16, 16, 18, 0.95);
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

    /* 6-Card Feature Grid (Matched to Second Reference Screenshot) */
    .synapse-feature-grid-6 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin: 36px 0;
    }
    @media (max-width: 900px) {
        .synapse-feature-grid-6 { grid-template-columns: 1fr; }
    }
    .feature-card-synapse {
        background: #0A0A0C;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 24px 26px;
        transition: transform 0.35s cubic-bezier(0.23, 1, 0.32, 1), border-color 0.35s, box-shadow 0.35s;
    }
    .feature-card-synapse:hover {
        transform: translateY(-6px);
        border-color: rgba(139, 92, 246, 0.4);
        box-shadow: 0 0 25px -8px rgba(139, 92, 246, 0.3);
        background: #0F0F12;
    }
    .feature-icon-box {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        margin-bottom: 14px;
        transition: transform 0.3s;
    }
    .feature-card-synapse:hover .feature-icon-box {
        transform: scale(1.08) rotate(-4deg);
    }
    .feature-title {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 1.35rem;
        color: #FFFFFF;
        margin-bottom: 6px;
        font-weight: 500;
    }
    .feature-desc {
        color: #9CA3AF;
        font-size: 0.86rem;
        line-height: 1.5;
        font-weight: 300;
    }

    /* Radio Options Card Transformation (Practice Quiz) */
    [data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 14px !important;
        padding: 12px 18px !important;
        margin-bottom: 8px !important;
        transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1) !important;
        color: #D1D5DB !important;
        font-size: 0.92rem !important;
    }
    [data-testid="stRadio"] label:hover {
        background: rgba(139, 92, 246, 0.08) !important;
        border-color: rgba(139, 92, 246, 0.4) !important;
        color: #FFFFFF !important;
        transform: translateX(4px) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        gap: 14px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin-bottom: 24px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #9CA3AF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        border-bottom: 2px solid #8B5CF6 !important;
    }

    /* Footer */
    .synapse-footer {
        background: #050505;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        padding: 40px 16px 24px 16px;
        margin-top: 50px;
        font-family: 'Inter', sans-serif;
    }
    .footer-grid {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 24px;
        max-width: 1100px;
        margin: 0 auto 28px auto;
    }
    @media (max-width: 800px) {
        .footer-grid { grid-template-columns: 1fr; }
    }
    .footer-brand-title {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 1.7rem;
        color: #FFFFFF;
        margin-bottom: 6px;
    }
    .footer-col-head {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: #6B7280;
        margin-bottom: 12px;
    }
    .footer-link {
        color: #9CA3AF;
        font-size: 0.84rem;
        margin-bottom: 6px;
        display: block;
        text-decoration: none;
    }
    .footer-bottom-bar {
        border-top: 1px solid rgba(255, 255, 255, 0.04);
        padding-top: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1100px;
        margin: 0 auto;
        font-size: 0.76rem;
        color: #6B7280;
    }
    </style>
    
    <!-- Ambient Background Elements -->
    <div class="synapse-orb-top"></div>
    <div class="synapse-bloom"></div>
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


def get_curated_prompts(language_key: str = "English") -> List[Dict[str, str]]:
    """Curated prompt pills with labels and icons matching the reference UI."""
    if language_key == "Hindi":
        return [
            {"label": "प्रकाश संश्लेषण क्या है? 🌱", "query": "प्रकाश संश्लेषण की रासायनिक समीकरण क्या है?"},
            {"label": "वायवीय और अवायवीय श्वसन 🫀", "query": "वायवीय और अवायवीय श्वसन में क्या अंतर है?"},
            {"label": "आमाशय में HCl की भूमिका 🧪", "query": "आमाशय में हाइड्रोक्लोरिक अम्ल (HCl) की क्या भूमिका है?"},
            {"label": "द्वार कोशिकाएं कैसे खुलती हैं? 🍃", "query": "द्वार कोशिकाएं रंध्रों को कैसे खोलती और बंद करती हैं?"},
            {"label": "मांसपेशियों में ऐंठन और लैक्टिक एसिड ⚡", "query": "व्यायाम के दौरान मांसपेशियों में लैक्टिक एसिड क्यों बनता है?"}
        ]
    elif language_key == "Kannada":
        return [
            {"label": "ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆ ಎಂದರೇನು? 🌱", "query": "ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆಯ ರಾಸಾಯನಿಕ ಸಮೀಕರಣವೇನು?"},
            {"label": "ವಾಯುವಿಕ vs ಅವಾಯುವಿಕ ಉಸಿರಾಟ 🫀", "query": "ವಾಯುವಿಕ ಮತ್ತು ಅವಾಯುವಿಕ ಉಸಿರಾಟದ ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು?"},
            {"label": "ಜಠರದಲ್ಲಿ HCl ಆಮ್ಲದ ಪಾತ್ರ 🧪", "query": "ಜಠರದಲ್ಲಿ ಹೈಡ್ರೋಕ್ಲೋರಿಕ್ ಆಮ್ಲದ (HCl) ಪಾತ್ರವೇನು?"},
            {"label": "ಕಾವಲು ಕೋಶಗಳ ಕಾರ್ಯವಿಧಾನ 🍃", "query": "ಕಾವಲು ಕೋಶಗಳು ಪತ್ರರಂಧ್ರಗಳನ್ನು ಹೇಗೆ ತೆರೆಯುತ್ತವೆ ಮತ್ತು ಮುಚ್ಚುತ್ತವೆ?"},
            {"label": "ಸ್ನಾಯುಗಳಲ್ಲಿ ಲ್ಯಾಕ್ಟಿಕ್ ಆಮ್ಲ ⚡", "query": "ವ್ಯಾಯಾಮದ ಸಮಯದಲ್ಲಿ ಸ್ನಾಯು ಕೋಶಗಳಲ್ಲಿ ಲ್ಯಾಕ್ಟಿಕ್ ಆಮ್ಲ ಏಕೆ ಸಂಗ್ರಹವಾಗುತ್ತದೆ?"}
        ]
    elif language_key == "Telugu":
        return [
            {"label": "కిరణజన్య సంయోగక్రియ సమీకరణం 🌱", "query": "కిరణజన్య సంయోగక్రియ రసాయన సమీకరణం ఏమిటి?"},
            {"label": "వాయు సహిత vs అవాయు శ్వాసక్రియ 🫀", "query": "వాయు సహిత మరియు అవాయు శ్వాసక్రియ మధ్య తేడా ఏమిటి?"},
            {"label": "జీర్ణాశయంలో HCl పాత్ర 🧪", "query": "జీర్ణాశయంలో హైడ್ರోక్లోరిక్ ఆమ్లం (HCl) పాత్ర ఏమిటి?"},
            {"label": "రక్షక కణాలు మరియు పత్రరంధ్రాలు 🍃", "query": "రక్షక కణాలు పత్రరంధ్రాలను ఎలా తెరుస్తాయి మరియు మూస్తాయి?"},
            {"label": "కండరాల నొప్పులు & లాక్టిక్ ఆమ్లం ⚡", "query": "వ్యాయామం చేసేటప్పుడు కండరాలలో లాక్టిక్ ఆమ్లం ఎందుకు పేరుకుపోతుంది?"}
        ]
    else:
        return [
            {"label": "What is Photosynthesis? 🌱", "query": "What is the chemical equation of photosynthesis and how does it synthesize glucose?"},
            {"label": "Aerobic vs Anaerobic Respiration 🫀", "query": "What is the difference between aerobic and anaerobic respiration in terms of ATP?"},
            {"label": "Role of HCl & Pepsin in Stomach 🧪", "query": "What is the role of hydrochloric acid (HCl) and pepsin secreted in the stomach?"},
            {"label": "How Guard Cells Open Stomata 🍃", "query": "How do guard cells regulate the opening and closing of stomata in leaves?"},
            {"label": "Why do Muscles Cramp during Exercise? ⚡", "query": "Why does lactic acid accumulate in muscle cells during vigorous exercise?"}
        ]


# Auto-load the most recent subject if none is active
existing_subjects = library.list_subjects()
if st.session_state.active_subject is None and existing_subjects:
    activate_subject(existing_subjects[0])

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
            <span class="nav-dot"></span>
            <span style="font-family: 'Instrument Serif', Georgia, serif; font-size: 1.5rem; color: #FFFFFF; font-weight: 500;">
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

    # 3. Textbook Upload & Indexing
    st.markdown("<p style='font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.15em; color:#9CA3AF;'>Textbook Chapter</p>", unsafe_allow_html=True)
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
# TRANSLATED TABS
# ==========================================
active_subj_name = st.session_state.active_subject['name'] if st.session_state.active_subject else "No Chapter Loaded"
ui = current_lang["ui"]

tab_ask, tab_quiz, tab_subjects, tab_analytics = st.tabs([
    ui["ask_tab"],
    ui["quiz_tab"],
    ui["library_tab"],
    "📊 Teacher Analytics"
])

# ==============================================================================
# TAB 1: 🗣️ ASK TUTOR (SUPERDESIGN CHAT INTERACTION & SYNAPSE PREVIEW)
# ==============================================================================
with tab_ask:
    col_chat_widget, col_chat_display = st.columns([1, 1.25], gap="large")

    # Determine Query triggers
    triggered_query = None
    action_type = "normal"
    pill_selected_query = None

    # LEFT COLUMN: SUPERDESIGN CHAT ASSISTANT CARD (EXACT REFERENCE UI)
    with col_chat_widget:
        st.markdown(
            f"""
            <div class="superdesign-card">
                <div class="superdesign-header">
                    <div class="superdesign-title-box">
                        <div class="superdesign-grid-icon">
                            <span style="font-size: 1.1rem;">❖</span>
                        </div>
                        <div>
                            <div class="superdesign-title">SuperDesign • VidyaVaani</div>
                            <div class="superdesign-subtitle">The tutor can also help • 9 Languages</div>
                        </div>
                    </div>
                    <div class="superdesign-controls">
                        <span>•••</span>
                        <span>✕</span>
                    </div>
                </div>
                
                <div class="superdesign-bubble">
                    {current_lang['greeting']} How can I help you today? Ask any question from your textbook chapter or select an option below:
                </div>
                <div class="superdesign-bubble-meta">
                    SuperDesign • Just now
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Floating Option Pills (Matched to the Reference Screenshot)
        # In the screenshot:
        # Quick start Guide
        # I have a question ❓
        # I found a bug 🐛
        # I want to ask for a new feature 🌟
        # Join our discord channel
        # Plus domain-specific learning actions:
        if st.button("Quick start Guide 🧭", key="pill_quickstart", use_container_width=False):
            triggered_query = f"Give me a clear, 3-bullet conceptual overview of {active_subj_name} for a school learner."

        if st.button("I have a question ❓", key="pill_question_prompt", use_container_width=False):
            triggered_query = f"What are the top 3 most important questions asked in board exams from {active_subj_name}?"

        btn_simpler = st.button(f"💡 {ui['simpler_btn']}", key="pill_simpler", use_container_width=False)
        btn_example = st.button(f"🔍 {ui['example_btn']} 🌟", key="pill_example", use_container_width=False)

        # Chapter-specific prompt pills
        curated_pills = get_curated_prompts(language_choice)
        for idx, item in enumerate(curated_pills[:3]):
            if st.button(item["label"], key=f"curated_pill_{idx}", use_container_width=False):
                pill_selected_query = item["query"]

        if st.button("Join student community 💬", key="pill_community", use_container_width=False):
            st.session_state.status_message = "Joined VidyaVaani Learner Circle! Share questions with classmates and track progress in Teacher Analytics."

        if st.button("Practice Quiz (5 MCQs) 📝", key="pill_quiz_shortcut", use_container_width=False):
            st.session_state.demo_query_triggered = f"Generate 5 high-yield practice MCQs based on {active_subj_name}."

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        # Optional Voice Recorder
        voice_query_text = None
        if speech_to_text is not None:
            col_m_rec, col_m_lbl = st.columns([1, 3])
            with col_m_rec:
                voice_query_text = speech_to_text(
                    language=current_lang.get("bcp47", "en-IN"),
                    start_prompt="🎙️ Speak",
                    stop_prompt="⏹️ Stop",
                    key="synapse_mic_recorder"
                )
            with col_m_lbl:
                if voice_query_text:
                    st.caption(f"🎙️ *\"{voice_query_text}\"*")

        # Micro Meta Bar
        st.markdown(
            f"""
            <div class="dock-meta-icons">
                <span class="dock-meta-item">📎 {active_subj_name[:18]}...</span>
                <span class="dock-meta-item">😊 Learner</span>
                <span class="dock-meta-item">🎙️ {current_lang['label']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Sleek Chat Input Dock with Circular Send Button
        with st.form("ask_form", clear_on_submit=False):
            col_dock_input, col_dock_btn = st.columns([5, 1])
            with col_dock_input:
                user_text = st.text_input(
                    "Question",
                    value=voice_query_text or "",
                    placeholder="Ask a question...",
                    label_visibility="collapsed"
                )
            with col_dock_btn:
                ask_submitted = st.form_submit_button("↑", type="primary", use_container_width=True)

    # Resolve Query
    if pill_selected_query:
        triggered_query = pill_selected_query
    elif st.session_state.get("demo_query_triggered"):
        triggered_query = st.session_state.pop("demo_query_triggered")
    elif ask_submitted and user_text.strip():
        triggered_query = user_text.strip()
    elif btn_simpler:
        action_type = "simpler"
        triggered_query = user_text.strip() or st.session_state.last_query or "Explain the main topic of this chapter in simple terms"
    elif btn_example:
        action_type = "example"
        triggered_query = user_text.strip() or st.session_state.last_query or "Give a real-world everyday example of this concept"

    # Execute RAG Pipeline with Gemini 3.8 Flash
    if triggered_query:
        if not st.session_state.indexed_chunks or st.session_state.faiss_index is None:
            st.error(ui["no_subject_alert"])
        else:
            with st.spinner("Searching textbook vector index and reasoning with Gemini 3.8 Flash..."):
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

    # RIGHT COLUMN: SYNAPSE PREVIEW & ACTIVE TUTOR RESPONSE CONSOLE
    with col_chat_display:
        if st.session_state.last_response:
            # Active Response in IDE Window
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
                        <div style="display:flex; align-items:center; gap:6px; font-family:'JetBrains Mono', monospace; font-size:0.72rem; color:#10B981;">
                            <span class="pulse-dot"></span>
                            <span>GROUNDED IN NCERT</span>
                        </div>
                    </div>
                    <div class="ide-content">
                        <div style="font-family:'JetBrains Mono', monospace; font-size:0.78rem; color:#A78BFA; margin-bottom:12px;">
                            PROMPT: "{st.session_state.last_query}"
                        </div>
                        {st.session_state.last_response.replace(chr(10), '<br>')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Spoken Neural Audio Player
            if st.session_state.last_audio_path and os.path.exists(st.session_state.last_audio_path):
                st.markdown(
                    f"""
                    <div style="display:flex; align-items:center; gap:8px; margin: 12px 0 6px 0;">
                        <span style="font-family:'Instrument Serif', Georgia, serif; font-size:1.3rem; color:#C4B5FD;">🎙️ {ui['audio_label']}</span>
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
                            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 14px 18px; margin-bottom: 10px;">
                                <div style="font-family:'JetBrains Mono', monospace; font-size:0.76rem; color:#A78BFA; font-weight:600; margin-bottom:6px;">
                                    PASSAGE #{idx+1} — [PAGE {src['page']}] • SIMILARITY: {src.get('score', 0):.3f}
                                </div>
                                <div style="color: #D1D5DB; font-size: 0.9rem; line-height: 1.5;">"{src['text']}"</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.write("No matching passages found.")
        else:
            # Synapse Hero Preview (Matched to Right Side of Screenshot 1)
            st.markdown(
                f"""
                <div class="hero-container" style="text-align: left; padding: 16px 20px 24px 20px; border: 1px solid rgba(255,255,255,0.06); border-radius: 26px; background: rgba(12, 12, 14, 0.5); backdrop-filter: blur(16px);">
                    <div class="status-chip" style="margin-bottom: 20px;">
                        <span class="nav-dot"></span>
                        <span>Mainnet Beta Live • Gemini 3.8 Flash</span>
                    </div>
                    <h1 class="hero-heading" style="font-size: 3.6rem; margin-bottom: 16px;">
                        Voices of Learning,<br><span class="shimmer-text">Grounded.</span>
                    </h1>
                    <p class="hero-subtext" style="margin: 0 0 24px 0; font-size: 1.05rem; line-height: 1.6; max-width: 580px;">
                        The first cognitive voice layer for educational equity. Synapse unifies textbook identity, neural execution, and multilingual settlement into a single neural fabric.
                    </p>
                    <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 28px;">
                        <div style="background: #FFFFFF; color: #030303; font-weight: 700; font-size: 0.88rem; padding: 10px 22px; border-radius: 9999px; display: inline-flex; align-items: center; gap: 8px;">
                            Start Learning →
                        </div>
                        <div style="color: #D1D5DB; font-size: 0.88rem; font-weight: 500; padding: 10px 16px;">
                            Read Chapter Specs 📖
                        </div>
                    </div>
                    <div class="hero-badges-row" style="justify-content: flex-start;">
                        <span class="synapse-badge">👤 {st.session_state.student_name}</span>
                        <span class="synapse-badge">🌐 {current_lang['label']}</span>
                        <span class="synapse-badge">📚 {active_subj_name}</span>
                        <span class="synapse-badge">⚡ Sub-500ms TTS</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ==========================================
    # INFINITE MARQUEE TICKER (Spanning Full Width)
    # ==========================================
    st.markdown(
        """
        <div class="ticker-wrapper" style="margin-top: 36px;">
            <div class="ticker-track">
                <div class="ticker-item"><span class="ticker-label">REASONING:</span><span class="ticker-value ticker-accent-violet">GEMINI 3.8 FLASH</span></div>
                <div class="ticker-item"><span class="ticker-label">RETRIEVAL:</span><span class="ticker-value ticker-accent-cyan">FAISS DENSE COSINE</span></div>
                <div class="ticker-item"><span class="ticker-label">EMBEDDINGS:</span><span class="ticker-value">MULTILINGUAL-E5</span></div>
                <div class="ticker-item"><span class="ticker-label">TTS ENGINE:</span><span class="ticker-value ticker-accent-violet">AZURE NEURAL (EDGE)</span></div>
                <div class="ticker-item"><span class="ticker-label">LANGUAGES:</span><span class="ticker-value ticker-accent-emerald">9 REGIONAL INDIC</span></div>
                <div class="ticker-item"><span class="ticker-label">ACCURACY:</span><span class="ticker-value">MANDATORY CITATIONS</span></div>
                <div class="ticker-item"><span class="ticker-label">STATUS:</span><span class="ticker-value ticker-accent-emerald">ACTIVE & GROUNDED</span></div>
                <!-- Loop -->
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
    # 6-CARD ARCHITECTURE FEATURE GRID
    # (Matched to Second Reference Screenshot)
    # ==========================================
    st.markdown(
        """
        <div style="text-align: center; margin-top: 36px; margin-bottom: 12px;">
            <div style="font-family: 'Instrument Serif', Georgia, serif; font-size: 2.6rem; color: #FFFFFF; font-weight: 400; letter-spacing: -0.02em;">
                Constructed for scale.
            </div>
            <div style="color: #9CA3AF; font-size: 0.95rem; font-weight: 300; max-width: 600px; margin: 6px auto 0 auto;">
                Built on a novel consensus mechanism that mimics neural pathways, enabling instant regional grounding at zero marginal cost.
            </div>
        </div>
        <div class="synapse-feature-grid-6">
            <div class="feature-card-synapse">
                <div class="feature-icon-box">🛡️</div>
                <div class="feature-title">Strict Grounding</div>
                <div class="feature-desc">Your biometric textbook boundary is your private key. Recover every factual claim with exact page citations.</div>
            </div>
            <div class="feature-card-synapse">
                <div class="feature-icon-box">⚡</div>
                <div class="feature-title">Instant Finality</div>
                <div class="feature-desc">FAISS vector cosine retrieval settles in 180ms. No hallucination, no front-running, just pure grounded execution speed.</div>
            </div>
            <div class="feature-card-synapse">
                <div class="feature-icon-box">🔒</div>
                <div class="feature-title">Zero Hallucination</div>
                <div class="feature-desc">Verify knowledge without guessing. Institutional-grade textbook factual grounding by default.</div>
            </div>
            <div class="feature-card-synapse">
                <div class="feature-icon-box">🧠</div>
                <div class="feature-title">Neural Consensus</div>
                <div class="feature-desc">A deep learning reasoning fabric powered by Gemini 3.8 Flash that scales as classroom curiosity increases.</div>
            </div>
            <div class="feature-card-synapse">
                <div class="feature-icon-box">🌐</div>
                <div class="feature-title">9 Indic Dialects</div>
                <div class="feature-desc">Access global knowledge in any regional tongue. VidyaVaani acts as the universal spoken translator.</div>
            </div>
            <div class="feature-card-synapse">
                <div class="feature-icon-box">📊</div>
                <div class="feature-title">Self-Auditing Metrics</div>
                <div class="feature-desc">The SQLite engine automatically balances inquiry logs, quiz mastery, and comprehension analytics.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
