"""
VidyaVaani Speech Synthesis & Recognition Module
Uses Microsoft Azure Neural voices via edge-tts with automatic gTTS fallback.
Provides clean speech synthesis for all 9 regional languages and voice input support.
"""

import os
import re
import time
import asyncio
import tempfile
import threading
from pathlib import Path
from typing import Optional

# edge-tts
try:
    import edge_tts
except ImportError:
    edge_tts = None

# gTTS fallback
try:
    from gtts import gTTS
except ImportError:
    gTTS = None

from config import LANGUAGES


def clean_text_for_speech(text: str) -> str:
    """
    Strips markdown formatting, bullet symbols, and raw code while
    preserving citations as natural phrases (e.g., '[Page 2]' -> 'Page 2').
    """
    if not text:
        return ""
    # Transform citations like [Page 2] or [Page 10] into spoken words
    cleaned = re.sub(r'\[Page\s*(\d+)\]', r'Page \1', text, flags=re.IGNORECASE)
    # Remove markdown formatting characters: *, #, _, `, ~, >
    cleaned = re.sub(r'[*#_`~>]', '', cleaned)
    # Remove URL links
    cleaned = re.sub(r'https?://\S+', '', cleaned)
    # Replace multiple spaces/newlines with a single space
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


async def _synthesize_edge_tts(text: str, voice: str, output_path: str):
    """Internal async coroutine for edge-tts."""
    communicator = edge_tts.Communicate(text, voice)
    await communicator.save(output_path)


def synthesize_speech(
    text: str,
    language_key: str,
    output_dir: Optional[Path] = None
) -> Optional[str]:
    """
    Synthesizes speech audio for the given text and regional language.
    Primary engine: edge-tts (Microsoft Neural Voice).
    Fallback engine: gTTS (Google Text-to-Speech).
    
    Returns:
        Path to the generated MP3 file, or None if synthesis fails.
    """
    cleaned = clean_text_for_speech(text)
    if not cleaned:
        return None

    lang_info = LANGUAGES.get(language_key, LANGUAGES["English"])
    voice_name = lang_info.get("voice", "en-IN-PrabhatNeural")
    gtts_code = lang_info.get("gtts_lang", "en")

    if output_dir is None:
        target_dir = Path(tempfile.gettempdir())
    else:
        target_dir = Path(output_dir)
        target_dir.mkdir(parents=True, exist_ok=True)

    filename = f"vidyavaani_{int(time.time() * 1000)}.mp3"
    output_path = str(target_dir / filename)

    # 1. Primary: edge-tts
    if edge_tts is not None:
        try:
            err_box = []

            def _worker():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(_synthesize_edge_tts(cleaned, voice_name, output_path))
                    loop.close()
                except Exception as exc:
                    err_box.append(exc)

            thread = threading.Thread(target=_worker)
            thread.start()
            thread.join(timeout=15)

            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path
        except Exception:
            pass

    # 2. Fallback: gTTS
    if gTTS is not None:
        try:
            tts = gTTS(text=cleaned, lang=gtts_code, slow=False)
            tts.save(output_path)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path
        except Exception:
            pass

    return None
