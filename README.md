# 🎙️ VidyaVaani (ವಿಧ್ಯಾವಾಣಿ / विद्यावाणी)
### A Voice-First AI Tutor for First-Generation Learners with Real-Time Spoken Regional Output & Teacher Analytics Dashboard

Built for hackathons, educational equity, and first-generation school students who learn best through spoken native languages.

---

## 🌟 Key Features

1. **Voice-First Regional Tutoring**:
   - Spoken answers powered by Microsoft Azure Neural voices via `edge-tts`:
     - **Kannada**: `kn-IN-GaganNeural` (or `kn-IN-SapnaNeural`)
     - **Hindi**: `hi-IN-MadhurNeural` (or `hi-IN-SwaraNeural`)
     - **English (Indian Accent)**: `en-IN-PrabhatNeural`
   - Spoken responses play automatically via inline audio players.

2. **Strict Grounded Retrieval-Augmented Generation (RAG)**:
   - Chunked PDF extraction with PyMuPDF (`fitz`).
   - Multilingual dense vector representations with `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`).
   - In-memory similarity retrieval using FAISS (`faiss-cpu`) with top-3 citations.
   - **Refusal Fallback**: Explicitly rejects off-topic queries with:  
     `"I cannot find this topic in your textbook chapter. Please ask a question related to this chapter."`
   - **Mandatory Page Citations**: Every factual claim cites its exact textbook page (e.g. `[Page 2]`).

3. **Tailored Scaffolding for First-Generation Learners**:
   - **💡 Explain Simpler**: Rewrites textbook concepts with gentle analogies and simple terms.
   - **🔍 Give an Example**: Generates relatable, real-world examples from Indian daily life.

4. **Dynamic Practice Quiz (Tab 2)**:
   - Generates 5 multiple choice questions grounded exclusively in the uploaded chapter.
   - Instant automated grading, answer keys, textbook explanations, and celebratory feedback.
   - Scores automatically logged to local SQLite database.

5. **Teacher / Admin Learning Analytics Dashboard (Tab 3)**:
   - Real-time KPI Metric cards: Total Questions Asked, Active Students Count, Average Quiz Score (%), Top Language Used.
   - Visual charts: Regional Language Breakdown and Student Score Distribution.
   - Live audit table of recent queries and student timestamps.
   - One-click CSV log export.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit |
| **PDF Extraction & Chunking** | PyMuPDF (`fitz`) |
| **Embeddings** | `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`) |
| **Vector Index** | FAISS (`faiss-cpu`) |
| **LLM Reasoning** | Google Gemini (`gemini-1.5-flash`) via `google-generativeai` |
| **Voice Synthesis** | `edge-tts` (Regional Indian Neural Voices) |
| **Database** | Built-in Python `sqlite3` |

---

## 🚀 Quickstart & Run Instructions

### 1. Prerequisites
Ensure Python 3.10 or 3.11 is installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Set your Gemini API Key
You can pass your API key via environment variable:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="AIzaSy..."

# Linux / macOS
export GEMINI_API_KEY="AIzaSy..."
```
*(Alternatively, enter it directly into the masked input field in the Streamlit sidebar).*

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 📂 Repository Structure

```
vidhyavaani/
├── app.py                # Main Streamlit web application & UI
├── database.py           # SQLite database layer & analytics helper functions
├── create_sample_pdf.py  # Utility script to generate the NCERT demo textbook chapter
├── sample_chapter.pdf    # Demo textbook chapter (Class 10 Science: Life Processes)
├── requirements.txt      # Production Python dependencies
├── vidyavaani.db         # SQLite database file (created automatically on startup)
└── README.md             # Documentation & setup guide
```

---

## 🎯 Architecture Diagram

```
+-----------------------------------------------------------+
|                   Student / Teacher UI                   |
|                        (Streamlit)                        |
+-----------------------------+-----------------------------+
                              |
       +----------------------+----------------------+
       |                                             |
[Tab 1: Ask Tutor]                         [Tab 2: Practice Quiz]
       |                                             |
  PDF Parser (PyMuPDF)                     Gemini 1.5 Flash MCQ Gen
       |                                             |
  FAISS Vector Index (k=3)                 Interactive Streamlit Form
       |                                             |
  Gemini 1.5 Flash Grounded RAG            Automated Grading & Feedback
       |                                             |
  Edge-TTS Regional Neural Audio                     |
  (Kannada / Hindi / English)                        |
       |                                             |
       +----------------------+----------------------+
                              |
                              v
                  [Tab 3: SQLite Analytics]
               - interactions table
               - quiz_results table
               - Metrics, Charts & CSV Export
```
