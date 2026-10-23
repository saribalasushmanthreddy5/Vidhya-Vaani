"""
Test audio synthesis across all 9 supported languages.
Verifies edge-tts and gTTS fallback for each language.
"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.config import LANGUAGES
import backend.speech as speech

sample_phrases = {
    "English": "Welcome to VidyaVaani. Photosynthesis creates glucose and oxygen in plant leaves.",
    "Hindi": "विद्यावाणी में आपका स्वागत है। प्रकाश संश्लेषण से पौधों में भोजन बनता है।",
    "Kannada": "ವಿದ್ಯಾವಾಣಿಗೆ ಸುಸ್ವಾಗತ. ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆಯಿಂದ ಸಸ್ಯಗಳಲ್ಲಿ ಗ್ಲೂಕೋಸ್ ಉತ್ಪತ್ತಿಯಾಗುತ್ತದೆ.",
    "Telugu": "విద్యావాణికి స్వాగతం. కిరణజన్య సంయోగక్రియ ద్వారా మొక్కలు గ్లూకోజ్ తయారు చేస్తాయి.",
    "Tamil": "வித்யாவாணிக்கு நல்வரவு. ஒளிச்சேர்க்கை மூலம் தாவரங்கள் உணவைத் தயாரிக்கின்றன.",
    "Malayalam": "വിദ്യാവാണിയിലേക്ക് സ്വാഗതം. പ്രകാശസംശ്ലേഷണം വഴി സസ്യങ്ങൾ ആഹാരം നിർമ്മിക്കുന്നു.",
    "Marathi": "विद्यावाणीमध्ये आपले स्वागत आहे. प्रकाशसंश्लेषण प्रक्रियेने वनस्पती अन्न तयार करतात.",
    "Bengali": "বিদ্যাবাণীতে স্বাগতম। সালোকসংশ্লেষ প্রক্রিয়ায় উদ্ভিদ গ্লুকোজ তৈরি করে।",
    "Gujarati": "વિદ્યાવાણીમાં તમારું સ્વાગત છે. પ્રકાશસંશ્લેષણ દ્વારા વનસ્પતિ ખોરાક બનાવે છે."
}

results = {}
for lang in LANGUAGES:
    text = sample_phrases.get(lang, "Test phrase.")
    voice = LANGUAGES[lang]["voice"]
    try:
        audio_path = speech.synthesize_speech(text, lang)
        if audio_path and os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            size_kb = os.path.getsize(audio_path) / 1024
            results[lang] = f"PASS ({size_kb:.1f} KB, voice: {voice})"
        else:
            results[lang] = "FAIL (Empty audio)"
    except Exception as e:
        results[lang] = f"FAIL (Error: {e})"

print("\n=== AUDIO SYNTHESIS PER-LANGUAGE RESULTS ===")
for lang, res in results.items():
    print(f"{lang:<12}: {res}")
