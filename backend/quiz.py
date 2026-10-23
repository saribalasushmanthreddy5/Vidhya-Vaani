"""
VidyaVaani Practice Quiz Generator
Generates a 5-question multiple choice assessment grounded in the textbook chapter.
Implements defensive JSON parsing and one retry upon failure, with robust fallback.
"""

import os
import re
import json
from typing import List, Dict, Any, Optional

try:
    from backend.config import LANGUAGES, GEMINI_MODEL, GROQ_MODEL
except (ImportError, ValueError):
    from config import LANGUAGES, GEMINI_MODEL, GROQ_MODEL

# google-genai
try:
    from google import genai
except ImportError:
    genai = None

# groq
try:
    from groq import Groq
except ImportError:
    Groq = None


def _clean_and_parse_json(raw_text: str) -> Optional[List[Dict[str, Any]]]:
    """Defensively extracts and parses a JSON list of quiz question objects."""
    if not raw_text:
        return None
    
    # Strip markdown fences
    cleaned = re.sub(r'```(?:json)?\s*', '', raw_text, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s*```', '', cleaned).strip()

    # Find array brackets
    match = re.search(r'\[\s*\{.*\}\s*\]', cleaned, re.DOTALL)
    candidate_str = match.group(0) if match else cleaned

    try:
        data = json.loads(candidate_str)
        if isinstance(data, list) and len(data) > 0:
            valid_questions = []
            for item in data:
                if (
                    isinstance(item, dict)
                    and "question" in item
                    and "options" in item
                    and isinstance(item["options"], list)
                    and len(item["options"]) == 4
                    and "answer" in item
                ):
                    valid_questions.append({
                        "id": len(valid_questions) + 1,
                        "question": str(item["question"]),
                        "options": [str(opt) for opt in item["options"]],
                        "answer": str(item["answer"]).strip().upper()[:1],
                        "explanation": str(item.get("explanation", "Grounded in textbook.")),
                        "page": int(item.get("page", 1))
                    })
            if len(valid_questions) >= 3:
                return valid_questions[:5]
    except Exception:
        pass

    return None


def _build_quiz_prompt(context_text: str, language_key: str, is_retry: bool = False) -> str:
    lang_info = LANGUAGES.get(language_key, LANGUAGES["English"])
    target_lang = lang_info["prompt_lang"]

    retry_warning = (
        "CRITICAL ERROR IN PREVIOUS ATTEMPT: Your output was not valid JSON! "
        "DO NOT write any explanation, intro, or markdown. Output RAW JSON ONLY.\n"
        if is_retry else ""
    )

    return f"""{retry_warning}Based SOLELY on the textbook excerpts below, generate EXACTLY 5 multiple-choice questions for school students in {target_lang}.

EXCERPTS:
{context_text}

OUTPUT INSTRUCTIONS:
Return strictly a valid JSON array of 5 objects. Do NOT use markdown fences or additional text.
Example JSON Structure:
[
  {{
    "id": 1,
    "question": "What is the primary product of photosynthesis?",
    "options": ["A) Carbon dioxide", "B) Glucose", "C) Hydrochloric acid", "D) Lactic acid"],
    "answer": "B",
    "explanation": "Plants synthesize glucose from CO2 and water [Page 1].",
    "page": 1
  }}
]
"""


def _invoke_llm_for_quiz(prompt: str, gemini_api_key: Optional[str] = None, groq_api_key: Optional[str] = None) -> Optional[str]:
    """Helper to query Gemini or Groq for raw quiz text."""
    g_key = (gemini_api_key or os.getenv("GEMINI_API_KEY") or "").strip()
    gr_key = (groq_api_key or os.getenv("GROQ_API_KEY") or "").strip()

    # Try Gemini
    if g_key and genai is not None:
        try:
            client = genai.Client(api_key=g_key)
            models = [GEMINI_MODEL, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
            for m in dict.fromkeys(models):
                try:
                    res = client.models.generate_content(model=m, contents=prompt)
                    if res and res.text:
                        return res.text.strip()
                except Exception:
                    continue
        except Exception:
            pass

    # Try Groq
    if gr_key and Groq is not None:
        try:
            client = Groq(api_key=gr_key)
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=GROQ_MODEL,
                temperature=0.2
            )
            return chat.choices[0].message.content.strip()
        except Exception:
            pass

    return None


def get_default_chapter_quiz() -> List[Dict[str, Any]]:
    """Curated deterministic fallback quiz based on the NCERT sample chapter."""
    return [
        {
            "id": 1,
            "question": "What is the primary chemical carbohydrate synthesized by plants during photosynthesis?",
            "options": ["A) Carbon dioxide", "B) Glucose (C6H12O6)", "C) Hydrochloric acid", "D) Lactic acid"],
            "answer": "B",
            "explanation": "Photosynthesis synthesizes glucose and releases oxygen [Page 1].",
            "page": 1
        },
        {
            "id": 2,
            "question": "Which specialized cells regulate the opening and closing of stomata in plant leaves?",
            "options": ["A) Guard cells", "B) Alveoli", "C) Intestinal villi", "D) Gastric cells"],
            "answer": "A",
            "explanation": "The swelling and shrinking of guard cells control the stomatal pore [Page 2].",
            "page": 2
        },
        {
            "id": 3,
            "question": "What is the primary function of hydrochloric acid (HCl) secreted by gastric glands in the stomach?",
            "options": ["A) Emulsifies fats", "B) Creates an acidic medium for pepsin and kills bacteria", "C) Absorbs water", "D) Breaks starch into maltose"],
            "answer": "B",
            "explanation": "HCl creates an acidic medium necessary for pepsin action and kills pathogens [Page 3].",
            "page": 3
        },
        {
            "id": 4,
            "question": "In which cellular organelle does aerobic respiration take place to generate ~38 ATP molecules?",
            "options": ["A) Ribosome", "B) Mitochondria", "C) Chloroplast", "D) Endoplasmic reticulum"],
            "answer": "B",
            "explanation": "Aerobic breakdown of pyruvate occurs in the mitochondria [Page 4].",
            "page": 4
        },
        {
            "id": 5,
            "question": "What substance accumulates in human muscle cells during vigorous exercise, causing sudden cramps?",
            "options": ["A) Ethanol", "B) Lactic acid", "C) Salivary amylase", "D) Bile salts"],
            "answer": "B",
            "explanation": "Anaerobic breakdown of pyruvate in human muscle cells under oxygen lack produces lactic acid [Page 4].",
            "page": 4
        }
    ]


def generate_chapter_quiz(
    chunks: List[Dict[str, Any]],
    language_key: str = "English",
    gemini_api_key: Optional[str] = None,
    groq_api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Generates 5 multiple choice questions grounded strictly in the chapter text.
    Implements defensive parsing and one retry if the initial parse fails.
    """
    if not chunks:
        return get_default_chapter_quiz()

    # Sample representative excerpts from chunks (up to 8 passages across pages)
    sample_text = "\n\n".join([f"[Page {c['page']}]: {c['text'][:350]}" for c in chunks[:8]])

    # Attempt 1
    prompt_1 = _build_quiz_prompt(sample_text, language_key, is_retry=False)
    raw_response_1 = _invoke_llm_for_quiz(prompt_1, gemini_api_key, groq_api_key)
    parsed_1 = _clean_and_parse_json(raw_response_1)
    if parsed_1 and len(parsed_1) == 5:
        return parsed_1

    # Attempt 2 (One Retry with strict formatting reinforcement)
    prompt_2 = _build_quiz_prompt(sample_text, language_key, is_retry=True)
    raw_response_2 = _invoke_llm_for_quiz(prompt_2, gemini_api_key, groq_api_key)
    parsed_2 = _clean_and_parse_json(raw_response_2)
    if parsed_2 and len(parsed_2) >= 3:
        return parsed_2

    # Deterministic fallback
    return get_default_chapter_quiz()
