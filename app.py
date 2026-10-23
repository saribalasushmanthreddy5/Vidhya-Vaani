"""
VidyaVaani Root Entrypoint Forwarder
Delegates execution to frontend/app.py
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_FRONTEND_APP = _ROOT / "frontend" / "app.py"

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
if str(_ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(_ROOT / "backend"))

with open(_FRONTEND_APP, "r", encoding="utf-8") as f:
    code = compile(f.read(), str(_FRONTEND_APP), "exec")
    exec(code, globals())
