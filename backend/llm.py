"""
VidyaVaani LLM Orchestration Layer
Uses google-genai (Gemini) as primary engine with Groq as fallback.
Enforces grounded tutor prompting, mandatory [Page X] citations, Explain Simpler,
Give an Example, and strict 'NOT_FOUND' refusal handling.
"""

import os
from typing import List, Dict, Any, Optional

try:
    from backend.config import (
        LANGUAGES,
        GEMINI_MODEL,
        GROQ_MODEL,
        SIM_THRESHOLD
    )
except (ImportError, ValueError):
    from config import (
        LANGUAGES,
        GEMINI_MODEL,
        GROQ_MODEL,
        SIM_THRESHOLD
    )

# Flag to verify google-genai package availability
try:
    from google import genai
    from google.genai import errors as genai_errors
except ImportError:
    genai = None

# Flag for Groq fallback
try:
    from groq import Groq
except ImportError:
    Groq = None


def build_tutor_prompt(
    query: str,
    context_chunks: List[Dict[str, Any]],
    language_key: str,
    action_type: str = "normal"
) -> str:
    """Builds the strictly grounded prompt with clear behavioral constraints."""
    lang_info = LANGUAGES.get(language_key, LANGUAGES["English"])
    target_lang = lang_info["prompt_lang"]

    context_formatted = "\n\n".join([
        f"[Page {c['page']}]:\n{c['text']}"
        for c in context_chunks
    ])

    action_instructions = ""
    if action_type == "simpler":
        action_instructions = (
            "TASK: The learner pressed 'Explain Simpler'. Rewrite the answer using very gentle, "
            "clear analogies, short sentences, and everyday terms suitable for a young student."
        )
    elif action_type == "example":
        action_instructions = (
            "TASK: The learner pressed 'Give an Example'. Provide an intuitive real-world example "
            "from daily life in India or common surroundings to clearly illustrate the concept."
        )

    prompt = f"""You are 'VidyaVaani', a compassionate, encouraging, and clear voice-first AI tutor for school students.

CRITICAL RULES:
1. STRICT GROUNDING: Answer ONLY using information present in the Textbook Passages below. Do NOT assume, speculate, or bring in external knowledge.
2. REFUSAL PROTOCOL: If the provided Textbook Passages do NOT contain enough information to answer the question, or if the question is off-topic, you MUST reply with ONLY the exact keyword:
NOT_FOUND
Do not say anything else if the answer is not in the text.
3. CITATIONS: Every factual claim must include its exact source page in square brackets, such as [Page 1] or [Page 2]. Even when answering in regional languages, write the citation strictly as [Page X] (with the English word 'Page') so that digital page citations link properly.
4. LANGUAGE: Provide your complete explanation in {target_lang}.
5. FORMAT: Use warm, encouraging, conversational phrasing suitable for spoken audio.

{action_instructions}

TEXTBOOK PASSAGES:
{context_formatted}

STUDENT'S QUESTION:
{query}
"""
    return prompt


def generate_tutor_response(
    query: str,
    context_chunks: List[Dict[str, Any]],
    language_key: str,
    action_type: str = "normal",
    gemini_api_key: Optional[str] = None,
    groq_api_key: Optional[str] = None,
    top_score: float = 1.0
) -> str:
    """
    Coordinates primary (Gemini via google-genai) and fallback (Groq) reasoning.
    Handles 'NOT_FOUND' responses and returns translated refusal message.
    """
    lang_info = LANGUAGES.get(language_key, LANGUAGES["English"])
    refusal_msg = lang_info["refusal"]

    # 1. First-pass retrieval threshold check
    if not context_chunks or top_score < SIM_THRESHOLD:
        return refusal_msg

    prompt = build_tutor_prompt(query, context_chunks, language_key, action_type)

    # API keys loaded securely from backend environment / .env
    g_key = (gemini_api_key if gemini_api_key is not None else (os.getenv("GEMINI_API_KEY") or "")).strip()
    gr_key = (groq_api_key if groq_api_key is not None else (os.getenv("GROQ_API_KEY") or "")).strip()

    # Attempt 1: Google GenAI (Gemini) Primary
    if g_key and genai is not None:
        try:
            client = genai.Client(api_key=g_key)
            # Try specified model, with fallback candidate list (gemini-3.5-flash-lite has active free quota)
            models_to_try = [
                GEMINI_MODEL,
                "gemini-3.5-flash-lite",
                "gemini-3.5-flash",
                "gemini-flash-lite-latest",
                "gemini-3.8-flash",
                "gemini-3.1-flash-lite",
            ]
            for model_name in dict.fromkeys(models_to_try):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    text = (response.text or "").strip()
                    if "NOT_FOUND" in text:
                        return refusal_msg
                    if text:
                        return text
                except Exception:
                    continue
        except Exception:
            pass

    # Attempt 2: Groq Fallback
    if gr_key and Groq is not None:
        try:
            groq_client = Groq(api_key=gr_key)
            groq_models = [GROQ_MODEL, "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
            for gm in dict.fromkeys(groq_models):
                try:
                    chat_completion = groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=gm,
                        temperature=0.3
                    )
                    text = (chat_completion.choices[0].message.content or "").strip()
                    if "NOT_FOUND" in text:
                        return refusal_msg
                    if text:
                        return text
                except Exception:
                    continue
        except Exception:
            pass

    # Attempt 3: Friendly Grounded Fallback (Synthesize from top chunk)
    if context_chunks:
        best_chunk = context_chunks[0]
        page_ref = f"[Page {best_chunk['page']}]"
        sample_text = best_chunk['text']
        
        notice_msg = {
            "English": f"According to your textbook {page_ref}:\n\n{sample_text}\n\n*(VidyaVaani Textbook Grounded Explanation)*",
            "Hindi": f"आपकी पाठ्यपुस्तक के अनुसार {page_ref}:\n\n{sample_text}",
            "Kannada": f"ನಿಮ್ಮ ಪಠ್ಯಪುಸ್ತಕದ ಪ್ರಕಾರ {page_ref}:\n\n{sample_text}",
            "Telugu": f"మీ పాఠ్యపుస్తకం ప్రకారం {page_ref}:\n\n{sample_text}",
            "Tamil": f"உங்கள் பாடப்புத்தகத்தின்படி {page_ref}:\n\n{sample_text}",
            "Malayalam": f"നിങ്ങളുടെ പാഠപുസ്തകമനുസരിച്ച് {page_ref}:\n\n{sample_text}",
            "Marathi": f"तुमच्या पाठ्यपुस्तकानुसार {page_ref}:\n\n{sample_text}",
            "Bengali": f"আপনার পাঠ্যবই অনুসারে {page_ref}:\n\n{sample_text}",
            "Gujarati": f"તમારા પાઠ્યપુસ્તક મુજબ {page_ref}:\n\n{sample_text}"
        }
        return notice_msg.get(language_key, notice_msg["English"])

    return "⚠️ Could not connect to AI services. Please verify your internet connection and backend API configuration."
