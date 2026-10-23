"""
VidyaVaani (ವಿಧ್ಯಾವಾಣಿ / विद्यावाणी): Voice-First Multilingual AI Tutor
Frontend UI (Streamlit Application)
- Clean student-first interface with NO exposed API keys or backend credentials
- 9 Regional Languages (English, Hindi, Kannada, Telugu, Tamil, Malayalam, Marathi, Bengali, Gujarati)
- My Subjects Library with SQLite persistence, auto-save, SHA-256 deduplication, re-indexing, and deletion
- Word-window chunking RAG with sentence-transformers multilingual-e5-small and FAISS cosine search
- Google-GenAI primary + Groq fallback LLM with strict grounding and NOT_FOUND refusal handling
- Edge-TTS neural speech with gTTS fallback
- 5-question dynamic practice quiz with defensive parsing and grading
- Teacher / Admin learning analytics dashboard
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
    page_title="VidyaVaani | Voice-First AI Tutor",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Impact CSS Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Kannada:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&family=Noto+Sans+Telugu:wght@400;600;700&family=Noto+Sans+Tamil:wght@400;600;700&family=Noto+Sans+Malayalam:wght@400;600;700&family=Noto+Sans+Bengali:wght@400;600;700&family=Noto+Sans+Gujarati:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', 'Noto Sans Kannada', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Bengali', 'Noto Sans Gujarati', sans-serif;
    }
    
    /* Hero Title Card */
    .hero-card {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        padding: 24px 32px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(67, 56, 202, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-card h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 2.1rem;
        margin-bottom: 6px;
        letter-spacing: -0.02em;
    }
    .hero-card p {
        color: #E0E7FF;
        font-size: 1.02rem;
        margin-bottom: 0;
        opacity: 0.95;
    }
    .hero-badges {
        display: flex;
        gap: 10px;
        margin-top: 14px;
        flex-wrap: wrap;
    }
    .badge-pill {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #F8FAFC;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Response Bubble */
    .tutor-bubble {
        background: #F8FAFC;
        border-left: 5px solid #4F46E5;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
    }
    
    /* Passage Card */
    .passage-card {
        background: #F1F5F9;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 10px;
        border: 1px solid #CBD5E1;
        font-size: 0.92rem;
    }
    .passage-page {
        font-weight: 700;
        color: #4338CA;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize database schema
library.init_library_db()

# ==========================================
# RESOURCE CACHE: EMBEDDING MODEL
# ==========================================
@st.cache_resource(show_spinner="Loading multilingual-e5-small model...")
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
    st.session_state.active_subject = None  # Dict of subject metadata
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


# Helper to activate a subject from the library
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
    """Preloads 5 high-yield sample presentation questions for the current subject."""
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
        # Dynamic fallback questions derived from chunk text
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
# SIDEBAR CONTROLS (Zero exposed API keys)
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ VidyaVaani Setup")
    
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
    
    st.markdown("---")

    # Demo Mode Checkbox
    demo_mode = st.checkbox(
        "🎯 Demo mode",
        value=st.session_state.get("demo_mode", False),
        help="Preloads 5 sample questions for the current subject as one-click buttons for smooth presentation without typing."
    )
    st.session_state.demo_mode = demo_mode

    if demo_mode:
        st.markdown("##### ⚡ One-Click Demo Questions:")
        curr_subj_name = st.session_state.active_subject['name'] if st.session_state.active_subject else "General"
        demo_qs_sb = get_demo_questions(curr_subj_name, st.session_state.indexed_chunks, language_choice)
        for d_i, d_q in enumerate(demo_qs_sb):
            if st.button(f"👉 {d_q}", key=f"sb_demo_btn_{d_i}", use_container_width=True):
                st.session_state.demo_query_triggered = d_q
                st.rerun()

    st.markdown("---")

    # 3. Textbook Upload & Indexing
    st.markdown("### 📖 Upload Textbook Chapter")
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

    st.markdown("---")
    # System Status Indicator
    st.markdown("#### 📡 Active Textbook")
    if st.session_state.active_subject:
        subj = st.session_state.active_subject
        st.success(f"✅ **{subj['name']}**\n- Pages: {subj['num_pages']} | Chunks: {subj['num_chunks']}")
    else:
        st.warning("⚠️ No subject selected. Upload a PDF or load the NCERT Demo.")

# ==========================================
# MAIN HEADER
# ==========================================
active_subj_name = st.session_state.active_subject['name'] if st.session_state.active_subject else "No Subject Loaded"

st.markdown(
    f"""
    <div class="hero-card">
        <h1>🎙️ VidyaVaani ({current_lang['native_name']})</h1>
        <p>Voice-First Multilingual AI Tutor for School Learners • Grounded in Textbooks</p>
        <div class="hero-badges">
            <span class="badge-pill">👤 Learner: {st.session_state.student_name}</span>
            <span class="badge-pill">🌐 Language: {current_lang['label']}</span>
            <span class="badge-pill">📚 Subject: {active_subj_name}</span>
            <span class="badge-pill">⚡ Multilingual-E5 RAG</span>
            <span class="badge-pill">🗣️ Neural Edge-TTS</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Translated Tab Headers
ui = current_lang["ui"]
tab_ask, tab_quiz, tab_subjects, tab_analytics = st.tabs([
    ui["ask_tab"],
    ui["quiz_tab"],
    ui["library_tab"],
    "📊 Teacher Analytics"
])

# ==============================================================================
# TAB 1: 🗣️ ASK TUTOR (STUDENT EXPERIENCE)
# ==============================================================================
with tab_ask:
    st.subheader(f"Ask your question in {current_lang['label']}")
    st.caption("Ask questions by voice or typing. VidyaVaani answers with spoken audio and textbook citations.")
    st.info(current_lang["greeting"])

    # 1. Voice Input Option (if mic recorder installed)
    voice_query_text = None
    if speech_to_text is not None:
        col_mic, col_mic_info = st.columns([1, 4])
        with col_mic:
            voice_query_text = speech_to_text(
                language=current_lang.get("bcp47", "en-IN"),
                start_prompt="🎙️ Speak Question",
                stop_prompt="⏹️ Stop Recording",
                key="mic_recorder"
            )
        with col_mic_info:
            if voice_query_text:
                st.success(f"Recognized Voice: *\"{voice_query_text}\"*")

    # 2. Text Query Form
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

    # 3. Demo Mode One-Click Presentation Questions
    tab_demo_selected = None
    if st.session_state.get("demo_mode", False):
        curr_subj_name = st.session_state.active_subject['name'] if st.session_state.active_subject else "General"
        demo_qs_tab = get_demo_questions(curr_subj_name, st.session_state.indexed_chunks, language_choice)
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); padding: 12px 18px; border-radius: 12px; border: 1px solid #C7D2FE; margin-top: 10px; margin-bottom: 12px;">
                <b style="color: #3730A3; font-size: 0.95rem;">🎯 Demo Mode Active:</b>
                <span style="color: #4338CA; font-size: 0.88rem;"> Click any preloaded sample question below to present instantly:</span>
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

    # 4. Learner Scaffolding Quick Actions
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        btn_simpler = st.button(ui["simpler_btn"], use_container_width=True)
    with col_s2:
        btn_example = st.button(ui["example_btn"], use_container_width=True)
    with col_s3:
        btn_sample_1 = st.button("🌱 What is Photosynthesis?", use_container_width=True)
    with col_s4:
        btn_sample_2 = st.button("🫀 How does Respiration work?", use_container_width=True)

    # Determine Active Query and Action Modifier
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

    # Execute RAG Pipeline (Clean server-side LLM call)
    if triggered_query:
        if not st.session_state.indexed_chunks or st.session_state.faiss_index is None:
            st.error(ui["no_subject_alert"])
        else:
            with st.spinner("Searching textbook chapter and synthesizing voice answer..."):
                emb_model = load_embedding_model()
                top_chunks, top_score = retrieval.search_similar_chunks(
                    query=triggered_query,
                    chunks=st.session_state.indexed_chunks,
                    index=st.session_state.faiss_index,
                    model=emb_model,
                    k=TOP_K
                )

                # Server-side LLM call without frontend API key handling
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

                # Persist interaction to database
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

    # Render Answer & Audio
    if st.session_state.last_response:
        st.markdown(f"### {ui['tutor_response']}")
        
        # Audio Player
        if st.session_state.last_audio_path and os.path.exists(st.session_state.last_audio_path):
            st.markdown(f"**{ui['audio_label']}**")
            with open(st.session_state.last_audio_path, "rb") as af:
                st.audio(af.read(), format="audio/mp3")

        # Answer Bubble
        formatted_resp = st.session_state.last_response.replace("\n", "<br>")
        st.markdown(
            f"""
            <div class="tutor-bubble">
                <div style="font-weight: 700; color: #4338CA; margin-bottom: 8px;">
                    🗣️ VidyaVaani ({current_lang['label']}):
                </div>
                <div>{formatted_resp}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Grounding Passages Expander
        with st.expander(ui["sources_title"], expanded=False):
            if st.session_state.last_sources:
                for idx, src in enumerate(st.session_state.last_sources):
                    st.markdown(
                        f"""
                        <div class="passage-card">
                            <span class="passage-page">Passage #{idx+1} — [Page {src['page']}] (Similarity Score: {src.get('score', 0):.3f})</span><br>
                            <em>"{src['text']}"</em>
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
    st.subheader(ui["quiz_title"])
    st.caption("5 multiple-choice questions grounded strictly in the active chapter.")

    col_qbtn, col_qinfo = st.columns([1, 2])
    with col_qbtn:
        if st.button(ui["quiz_gen_btn"], type="primary", use_container_width=True):
            if not st.session_state.indexed_chunks:
                st.warning(ui["no_subject_alert"])
            else:
                with st.spinner("Generating 5 chapter questions..."):
                    qdata = quiz.generate_chapter_quiz(
                        chunks=st.session_state.indexed_chunks,
                        language_key=language_choice
                    )
                    st.session_state.quiz_data = qdata
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = 0
                    st.rerun()

    if st.session_state.quiz_data:
        st.markdown("---")
        with st.form("quiz_form"):
            user_choices = {}
            for item in st.session_state.quiz_data:
                st.markdown(f"**Q{item['id']}: {item['question']}**")
                choice = st.radio(
                    f"Options for Q{item['id']}:",
                    options=item["options"],
                    key=f"quiz_opt_{item['id']}",
                    index=None
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
            st.markdown("---")
            if pct >= 80:
                st.balloons()
                st.success(f"🎉 Fantastic Job, {st.session_state.student_name}! Score: **{score}/{total} ({pct}%)**")
            elif pct >= 50:
                st.info(f"👍 Good effort, {st.session_state.student_name}! Score: **{score}/{total} ({pct}%)**. Review the chapter to improve!")
            else:
                st.warning(f"📚 Score: **{score}/{total} ({pct}%)**. Don't worry! Ask VidyaVaani about these topics and try again.")

            # Review Details
            st.markdown("#### Detailed Question Review:")
            for f in feedback_list:
                status_text = "✅ Correct" if f["is_correct"] else "❌ Incorrect"
                color = "#059669" if f["is_correct"] else "#DC2626"
                st.markdown(
                    f"""
                    <div style="background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                        <strong>Q{f['id']}: {f['question']}</strong><br>
                        <span style="color: {color}; font-weight: 700;">{status_text}</span> • Your Answer: <code>{f['chosen']}</code> • Correct: <code>Option {f['correct']}</code><br>
                        <span style="font-size: 0.9rem; color: #4B5563;">💡 <em>{f['explanation']} [Page {f['page']}]</em></span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("Click 'Generate / Refresh Quiz' above to create questions from your active textbook.")

# ==============================================================================
# TAB 3: 📚 MY SUBJECTS LIBRARY (REGISTRY & MANAGEMENT)
# ==============================================================================
with tab_subjects:
    st.subheader("📚 My Subjects Library")
    st.caption("Manage saved textbooks, re-index documents, or select an active subject.")

    all_subjects = library.list_subjects()
    if not all_subjects:
        st.info("No subjects saved yet. Upload a PDF or click 'Load NCERT Demo Chapter' in the sidebar.")
    else:
        for subj in all_subjects:
            is_active = (
                st.session_state.active_subject is not None
                and st.session_state.active_subject["id"] == subj["id"]
            )
            col_info, col_act1, col_act2, col_act3 = st.columns([4, 1.2, 1.2, 1.2])
            
            with col_info:
                active_badge = " 🟢 **(Active)**" if is_active else ""
                st.markdown(f"### {subj['name']}{active_badge}")
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

            st.markdown("---")

# ==============================================================================
# TAB 4: 📊 TEACHER / ADMIN LEARNING ANALYTICS
# ==============================================================================
with tab_analytics:
    st.subheader("📊 VidyaVaani Learning Analytics")
    st.caption("Student engagement, regional language distribution, quiz performance, and activity logs.")

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
    col_m1.metric("Total Questions Asked", q_count)
    col_m2.metric("Active Students", s_count)
    col_m3.metric("Average Quiz Score", f"{avg_score}%")
    col_m4.metric("Top Language", top_lang)

    st.markdown("---")
    
    # Language Breakdown Chart
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("#### 🌐 Regional Language Breakdown")
        with library.get_connection() as conn:
            lang_df = pd.read_sql_query("SELECT language, COUNT(*) as count FROM interactions GROUP BY language ORDER BY count DESC", conn)
        if not lang_df.empty:
            st.bar_chart(lang_df.set_index("language")["count"], color="#4F46E5")
        else:
            st.info("No questions asked yet.")

    with col_c2:
        st.markdown("#### 📈 Quiz Score Distribution")
        with library.get_connection() as conn:
            quiz_df = pd.read_sql_query("SELECT student_name, ROUND((CAST(score AS FLOAT)/total)*100, 1) as percentage FROM quiz_results ORDER BY id DESC LIMIT 20", conn)
        if not quiz_df.empty:
            st.bar_chart(quiz_df.set_index("student_name")["percentage"], color="#059669")
        else:
            st.info("No quiz results yet.")

    st.markdown("---")
    st.markdown("#### 🕒 Recent Activity Log")
    with library.get_connection() as conn:
        logs_df = pd.read_sql_query("SELECT id, student_name, language, query, response, timestamp FROM interactions ORDER BY id DESC LIMIT 50", conn)
    if not logs_df.empty:
        st.dataframe(logs_df, use_container_width=True, hide_index=True)
    else:
        st.info("No activity recorded.")
