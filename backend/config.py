"""
VidyaVaani Configuration Module
Contains all system settings, models, paths, and the single authoritative LANGUAGES registry.
All language-specific logic, translations, voices, and codes live exclusively in this file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ==========================================
# PATHS & PERSISTENCE
# ==========================================
# Root of the project workspace
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INDEX_DIR = DATA_DIR / "indexes"
DB_PATH = DATA_DIR / "vidyavaani.db"
DEFAULT_SAMPLE_PDF = BASE_DIR / "sample_chapter.pdf"

# Load environment variables strictly from root .env if present
load_dotenv(BASE_DIR / ".env")

DATA_DIR.mkdir(parents=True, exist_ok=True)
INDEX_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# MODELS & PARAMETERS (Server-Side Backend)
# ==========================================
# Primary LLM via google-genai
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
# Fallback LLM via groq
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Embedding model specified in architecture
EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-small"

# Retrieval tuning: calibrated using in-chapter regional & English (0.785-0.89) vs off-topic (0.72-0.78)
SIM_THRESHOLD = float(os.getenv("SIM_THRESHOLD", "0.782"))
TOP_K = 3
CHUNK_SIZE_WORDS = 150
CHUNK_OVERLAP_WORDS = 30

# ==========================================
# 9 SUPPORTED LANGUAGES REGISTRY
# ==========================================
LANGUAGES = {
    "English": {
        "name": "English",
        "native_name": "English",
        "label": "English (Indian Accent)",
        "voice": "en-IN-PrabhatNeural",
        "gtts_lang": "en",
        "bcp47": "en-IN",
        "prompt_lang": "clear, warm Indian English in standard English script",
        "greeting": "Hello! Ask any question from your textbook chapter.",
        "refusal": "I cannot find this topic in your textbook chapter. Please ask a question related to this chapter.",
        "ui": {
            "ask_tab": "🗣️ Ask Tutor",
            "quiz_tab": "📝 Practice Quiz",
            "library_tab": "📚 My Subjects",
            "ask_placeholder": "Ask a question from this chapter...",
            "ask_btn": "🚀 Ask Tutor",
            "simpler_btn": "💡 Explain Simpler",
            "example_btn": "🔍 Give an Example",
            "audio_label": "🎙️ Listen to Explanation:",
            "tutor_response": "🗣️ VidyaVaani Tutor Response",
            "sources_title": "📖 Textbook Grounding Passages (Citations)",
            "no_subject_alert": "Please select or upload a subject textbook in the sidebar first.",
            "quiz_title": "Chapter Practice Quiz (5 Questions)",
            "quiz_gen_btn": "🎯 Generate / Refresh Quiz",
            "quiz_submit_btn": "🏁 Submit Quiz for Grading"
        }
    },
    "Hindi": {
        "name": "Hindi",
        "native_name": "हिन्दी",
        "label": "हिन्दी (Hindi)",
        "voice": "hi-IN-MadhurNeural",
        "gtts_lang": "hi",
        "bcp47": "hi-IN",
        "prompt_lang": "Hindi language in Devanagari script (हिन्दी)",
        "greeting": "नमस्ते! अपने पाठ्यपुस्तक अध्याय से कोई भी प्रश्न पूछें।",
        "refusal": "मुझे आपकी पाठ्यपुस्तक के अध्याय में यह विषय नहीं मिला। कृपया इस अध्याय से संबंधित प्रश्न पूछें।",
        "ui": {
            "ask_tab": "🗣️ शिक्षक से पूछें",
            "quiz_tab": "📝 अभ्यास प्रश्नोत्तरी",
            "library_tab": "📚 मेरे विषय",
            "ask_placeholder": "इस अध्याय से कोई प्रश्न पूछें...",
            "ask_btn": "🚀 प्रश्न पूछें",
            "simpler_btn": "💡 सरल शब्दों में समझाएं",
            "example_btn": "🔍 एक उदाहरण दें",
            "audio_label": "🎙️ स्पष्टीकरण सुनें:",
            "tutor_response": "🗣️ विद्यावाणी उत्तर",
            "sources_title": "📖 पाठ्यपुस्तक संदर्भ (पृष्ठ उद्धरण)",
            "no_subject_alert": "कृपया पहले साइडबार से किसी विषय की पाठ्यपुस्तक चुनें या अपलोड करें।",
            "quiz_title": "अध्याय अभ्यास प्रश्नोत्तरी (5 प्रश्न)",
            "quiz_gen_btn": "🎯 प्रश्नोत्तरी बनाएं / रीफ्रेश करें",
            "quiz_submit_btn": "🏁 मूल्यांकन के लिए जमा करें"
        }
    },
    "Kannada": {
        "name": "Kannada",
        "native_name": "ಕನ್ನಡ",
        "label": "ಕನ್ನಡ (Kannada)",
        "voice": "kn-IN-GaganNeural",
        "gtts_lang": "kn",
        "bcp47": "kn-IN",
        "prompt_lang": "Kannada language in Kannada script (ಕನ್ನಡ)",
        "greeting": "ನಮಸ್ಕಾರ! ನಿಮ್ಮ ಪಠ್ಯಪುಸ್ತಕದ ಅಧ್ಯಾಯದಿಂದ ಯಾವುದೇ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ.",
        "refusal": "ನಿಮ್ಮ ಪಠ್ಯಪುಸ್ತಕದ ಅಧ್ಯಾಯದಲ್ಲಿ ಈ ವಿಷಯ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಈ ಅಧ್ಯಾಯಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ.",
        "ui": {
            "ask_tab": "🗣️ ಶಿಕ್ಷಕರನ್ನು ಕೇಳಿ",
            "quiz_tab": "📝 ರಸಪ್ರಶ್ನೆ ಅಭ್ಯಾಸ",
            "library_tab": "📚 ನನ್ನ ವಿಷಯಗಳು",
            "ask_placeholder": "ಈ ಅಧ್ಯಾಯದಿಂದ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ...",
            "ask_btn": "🚀 ಪ್ರಶ್ನೆ ಕೇಳಿ",
            "simpler_btn": "💡 ಸರಳವಾಗಿ ವಿವರಿಸಿ",
            "example_btn": "🔍 ಒಂದು ಉದಾಹರಣೆ ನೀಡಿ",
            "audio_label": "🎙️ ವಿವರಣೆಯನ್ನು ಆಲಿಸಿ:",
            "tutor_response": "🗣️ ವಿದ್ಯಾವಾಣಿ ಉತ್ತರ",
            "sources_title": "📖 ಪಠ್ಯಪುಸ್ತಕದ ಉಲ್ಲೇಖಗಳು (ಪುಟ ಸಂಖ್ಯೆ)",
            "no_subject_alert": "ದಯವಿಟ್ಟು ಮೊದಲು ಸೈಡ್‌ಬಾರ್‌ನಿಂದ ವಿಷಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ ಅಥವಾ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
            "quiz_title": "ಅಧ್ಯಾಯ ರಸಪ್ರಶ್ನೆ (5 ಪ್ರಶ್ನೆಗಳು)",
            "quiz_gen_btn": "🎯 ರಸಪ್ರಶ್ನೆ ರಚಿಸಿ / ರಿಫ್ರೆಶ್ ಮಾಡಿ",
            "quiz_submit_btn": "🏁 ಮೌಲ್ಯಮಾಪನಕ್ಕೆ ಸಲ್ಲಿಸಿ"
        }
    },
    "Telugu": {
        "name": "Telugu",
        "native_name": "తెలుగు",
        "label": "తెలుగు (Telugu)",
        "voice": "te-IN-MohanNeural",
        "gtts_lang": "te",
        "bcp47": "te-IN",
        "prompt_lang": "Telugu language in Telugu script (తెలుగు)",
        "greeting": "నమస్కారం! మీ పాఠ్యపుస్తకం అధ్యాయం నుండి ఏదైనా ప్రశ్న అడగండి.",
        "refusal": "మీ పాఠ్యపుస్తకం అధ్యాయంలో ఈ అంశం కనిపించలేదు. దయచేసి ఈ అధ్యాయానికి సంబంధించిన ప్రశ్నను అడగండి.",
        "ui": {
            "ask_tab": "🗣️ గురువును అడగండి",
            "quiz_tab": "📝 అభ్యాస క్విజ్",
            "library_tab": "📚 నా సబ్జెక్టులు",
            "ask_placeholder": "ఈ అధ్యాయం నుండి ప్రశ్న అడగండి...",
            "ask_btn": "🚀 ప్రశ్న అడగండి",
            "simpler_btn": "💡 సరళంగా వివరించండి",
            "example_btn": "🔍 ఒక ఉదాహరణ ఇవ్వండి",
            "audio_label": "🎙️ వివరణ వినండి:",
            "tutor_response": "🗣️ విద్యావాణి సమాధానం",
            "sources_title": "📖 పాఠ్యపుస్తక ఆధారాలు (పేజీ సంఖ్య)",
            "no_subject_alert": "దయచేసి మొదట సైడ్‌బార్‌లో ఒక పాఠ్యపుస్తకాన్ని ఎంచుకోండి లేదా అప్‌లోడ్ చేయండి.",
            "quiz_title": "అధ్యాయం క్విజ్ (5 ప్రశ్నలు)",
            "quiz_gen_btn": "🎯 క్విజ్ సృష్టించండి",
            "quiz_submit_btn": "🏁 క్విజ్ సమర్పించండి"
        }
    },
    "Tamil": {
        "name": "Tamil",
        "native_name": "தமிழ்",
        "label": "தமிழ் (Tamil)",
        "voice": "ta-IN-ValluvarNeural",
        "gtts_lang": "ta",
        "bcp47": "ta-IN",
        "prompt_lang": "Tamil language in Tamil script (தமிழ்)",
        "greeting": "வணக்கம்! உங்கள் பாடப்புத்தக அத்தியாயத்திலிருந்து ஏதேனும் கேள்வியைக் கேளுங்கள்.",
        "refusal": "உங்கள் பாடப்புத்தக அத்தியாயத்தில் இந்த தலைப்பு காணப்படவில்லை. இந்த அத்தியாயம் தொடர்பான கேள்வியைக் கேளுங்கள்.",
        "ui": {
            "ask_tab": "🗣️ ஆசிரியரிடம் கேளுங்கள்",
            "quiz_tab": "📝 பயிற்சி வினாடி வினா",
            "library_tab": "📚 எனது பாடங்கள்",
            "ask_placeholder": "இந்த அத்தியாயத்திலிருந்து ஒரு கேள்வி கேளுங்கள்...",
            "ask_btn": "🚀 கேள்வி கேளுங்கள்",
            "simpler_btn": "💡 எளிமையாக விளக்குங்கள்",
            "example_btn": "🔍 ஓர் உதாரணம் கொடுங்கள்",
            "audio_label": "🎙️ விளக்கத்தைக் கேளுங்கள்:",
            "tutor_response": "🗣️ வித்யாவாணி பதில்",
            "sources_title": "📖 பாடப்புத்தக ஆதாரங்கள் (பக்க குறிப்புகள்)",
            "no_subject_alert": "தயவுசெய்து பக்கவாட்டுப் பட்டியில் பாடப்புத்தகத்தைத் தேர்ந்தெடுக்கவும் அல்லது பதிவேற்றவும்.",
            "quiz_title": "அத்தியாய வினாடி வினா (5 கேள்விகள்)",
            "quiz_gen_btn": "🎯 வினாடி வினா உருவாக்குக",
            "quiz_submit_btn": "🏁 விடை சமர்ப்பிக்க"
        }
    },
    "Malayalam": {
        "name": "Malayalam",
        "native_name": "മലയാളം",
        "label": "മലയാളം (Malayalam)",
        "voice": "ml-IN-MidhunNeural",
        "gtts_lang": "ml",
        "bcp47": "ml-IN",
        "prompt_lang": "Malayalam language in Malayalam script (മലയാളം)",
        "greeting": "നമസ്കാരം! നിങ്ങളുടെ പാഠപുസ്തക അധ്യായത്തിൽ നിന്ന് ഏത് ചോദ്യവും ചോദിക്കാം.",
        "refusal": "നിങ്ങളുടെ പാഠപുസ്തക അധ്യായത്തിൽ ഈ വിഷയം കണ്ടെത്താനായില്ല. ഈ അധ്യായവുമായി ബന്ധപ്പെട്ട ഒരു ചോദ്യം ചോദിക്കുക.",
        "ui": {
            "ask_tab": "🗣️ അധ്യാപകനോട് ചോദിക്കുക",
            "quiz_tab": "📝 പരിശീലന ക്വിസ്",
            "library_tab": "📚 എന്റെ വിഷയങ്ങൾ",
            "ask_placeholder": "ഈ അധ്യായത്തിൽ നിന്ന് ഒരു ചോദ്യം ചോദിക്കുക...",
            "ask_btn": "🚀 ചോദ്യം ചോദിക്കുക",
            "simpler_btn": "💡 ലളിതമായി വിശദീകരിക്കുക",
            "example_btn": "🔍 ഒരു ഉദാഹരണം നൽകുക",
            "audio_label": "🎙️ വിശദീകരണം കേൾക്കൂ:",
            "tutor_response": "🗣️ വിദ്യാവാണി മറുപടി",
            "sources_title": "📖 പാഠപുസ്തക അവലംബങ്ങൾ (പേജ് നമ്പറുകൾ)",
            "no_subject_alert": "ദയവായി ആദ്യം സൈഡ്ബാറിൽ നിന്ന് ഒരു പാഠപുസ്തകം തിരഞ്ഞെടുക്കുകയോ അപ്‌ലോഡ് ചെയ്യുകയോ ചെയ്യുക.",
            "quiz_title": "അധ്യായ ക്വിസ് (5 ചോദ്യങ്ങൾ)",
            "quiz_gen_btn": "🎯 ക്വിസ് ആരംഭിക്കുക",
            "quiz_submit_btn": "🏁 സമർപ്പിക്കുക"
        }
    },
    "Marathi": {
        "name": "Marathi",
        "native_name": "मराठी",
        "label": "मराठी (Marathi)",
        "voice": "mr-IN-ManoharNeural",
        "gtts_lang": "mr",
        "bcp47": "mr-IN",
        "prompt_lang": "Marathi language in Devanagari script (मराठी)",
        "greeting": "नमस्कार! तुमच्या पाठ्यपुस्तकातील धड्यावरून कोणताही प्रश्न विचारा.",
        "refusal": "तुमच्या पाठ्यपुस्तकातील धड्यात हा विषय सापडला नाही. कृपया या धड्याशी संबंधित प्रश्न विचारा.",
        "ui": {
            "ask_tab": "🗣️ शिक्षकांना विचारा",
            "quiz_tab": "📝 सराव प्रश्नमंजुषा",
            "library_tab": "📚 माझे विषय",
            "ask_placeholder": "या धड्यातून प्रश्न विचारा...",
            "ask_btn": "🚀 प्रश्न विचारा",
            "simpler_btn": "💡 सोप्या भाषेत सांगा",
            "example_btn": "🔍 एक उदाहरण द्या",
            "audio_label": "🎙️ स्पष्टीकरण ऐका:",
            "tutor_response": "🗣️ विद्यावाणी उत्तर",
            "sources_title": "📖 पाठ्यपुस्तक संदर्भ (पृष्ठ क्रमांक)",
            "no_subject_alert": "कृपया प्रथम साइडबारमधून विषय निवडा किंवा अपलोड करा.",
            "quiz_title": "धड्यावरील प्रश्नमंजुषा (5 प्रश्न)",
            "quiz_gen_btn": "🎯 प्रश्नमंजुषा तयार करा",
            "quiz_submit_btn": "🏁 उत्तर तपासा"
        }
    },
    "Bengali": {
        "name": "Bengali",
        "native_name": "বাংলা",
        "label": "বাংলা (Bengali)",
        "voice": "bn-IN-BashkarNeural",
        "gtts_lang": "bn",
        "bcp47": "bn-IN",
        "prompt_lang": "Bengali language in Bengali script (বাংলা)",
        "greeting": "নমস্কার! আপনার পাঠ্যবইয়ের অধ্যায় থেকে যেকোনো প্রশ্ন জিজ্ঞাসা করুন।",
        "refusal": "আপনার পাঠ্যবইয়ের অধ্যায়ে এই বিষয়টি খুঁজে পাওয়া যায়নি। দয়া করে এই অধ্যায় সম্পর্কিত একটি প্রশ্ন জিজ্ঞাসা করুন।",
        "ui": {
            "ask_tab": "🗣️ শিক্ষককে জিজ্ঞাসা করুন",
            "quiz_tab": "📝 অনুশীলন কুইজ",
            "library_tab": "📚 আমার বিষয়",
            "ask_placeholder": "এই অধ্যায় থেকে একটি প্রশ্ন করুন...",
            "ask_btn": "🚀 প্রশ্ন জিজ্ঞাসা করুন",
            "simpler_btn": "💡 সহজ ভাষায় বুঝিয়ে দিন",
            "example_btn": "🔍 একটি উদাহরণ দিন",
            "audio_label": "🎙️ ব্যাখ্যা শুনুন:",
            "tutor_response": "🗣️ বিদ্যাবাণী উত্তর",
            "sources_title": "📖 পাঠ্যবইয়ের তথ্যসূত্র (পৃষ্ঠা নম্বর)",
            "no_subject_alert": "দয়া করে প্রথমে সাইডবার থেকে পাঠ্যবই নির্বাচন বা আপলোড করুন।",
            "quiz_title": "অধ্যায় কুইজ (৫টি প্রশ্ন)",
            "quiz_gen_btn": "🎯 কুইজ তৈরি করুন",
            "quiz_submit_btn": "🏁 কুইজ জমা দিন"
        }
    },
    "Gujarati": {
        "name": "Gujarati",
        "native_name": "ગુજરાતી",
        "label": "ગુજરાતી (Gujarati)",
        "voice": "gu-IN-NiranjanNeural",
        "gtts_lang": "gu",
        "bcp47": "gu-IN",
        "prompt_lang": "Gujarati language in Gujarati script (ગુજરાતી)",
        "greeting": "નમસ્તે! તમારા પાઠ્યપુસ્તકના પ્રકરણમાંથી કોઈપણ પ્રશ્ન પૂછો.",
        "refusal": "તમારા પાઠ્યપુસ્તકના પ્રકરણમાં આ વિષય મળ્યો નથી. કૃપા કરીને આ પ્રકરણ સંબંધિત પ્રશ્ન પૂછો.",
        "ui": {
            "ask_tab": "🗣️ શિક્ષકને પૂછો",
            "quiz_tab": "📝 પ્રેક્ટિસ ક્વિઝ",
            "library_tab": "📚 મારા વિષયો",
            "ask_placeholder": "આ પ્રકરણમાંથી પ્રશ્ન પૂછો...",
            "ask_btn": "🚀 પ્રશ્ન પૂછો",
            "simpler_btn": "💡 સરળ ભાષામાં સમજાવો",
            "example_btn": "🔍 એક ઉદાહરણ આપો",
            "audio_label": "🎙️ સમજૂતી સાંભળો:",
            "tutor_response": "🗣️ વિદ્યાવાણી ઉત્તર",
            "sources_title": "📖 પાઠ્યપુસ્તક સંદર્ભ (પૃષ્ઠ નોંધો)",
            "no_subject_alert": "કૃપા કરીને પહેલા સાઇડબારમાંથી પાઠ્યપુસ્તક પસંદ કરો અથવા અપલોડ કરો.",
            "quiz_title": "પ્રકરણ ક્વિઝ (5 પ્રશ્નો)",
            "quiz_gen_btn": "🎯 ક્વિઝ બનાવો",
            "quiz_submit_btn": "🏁 ક્વિઝ સબમિટ કરો"
        }
    }
}
