import subprocess
import time
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
VENV_STREAMLIT = BASE_DIR / ".venv" / "Scripts" / "streamlit.exe"
CLOUDFLARED = Path(r"C:\Program Files (x86)\cloudflared\cloudflared.exe")
TUNNEL_URL_FILE = BASE_DIR / "tunnel_url.txt"
LOG_DIR = BASE_DIR / "data" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

streamlit_log = open(LOG_DIR / "streamlit.log", "w", encoding="utf-8")
tunnel_log = open(LOG_DIR / "tunnel.log", "w", encoding="utf-8")

print("[1/3] Starting Streamlit server from frontend/app.py...")
st_proc = subprocess.Popen(
    [str(VENV_STREAMLIT), "run", "frontend/app.py"],
    cwd=str(BASE_DIR),
    stdout=streamlit_log,
    stderr=streamlit_log
)

time.sleep(3)

print("[2/3] Starting Cloudflare Tunnel with HTTP/2 protocol...")
cf_proc = subprocess.Popen(
    [str(CLOUDFLARED), "tunnel", "--protocol", "http2", "--url", "http://127.0.0.1:8501"],
    cwd=str(BASE_DIR),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

tunnel_url = None
start_time = time.time()

print("[3/3] Waiting for public tunnel URL...")
for line in iter(cf_proc.stdout.readline, ''):
    tunnel_log.write(line)
    tunnel_log.flush()
    if not tunnel_url:
        match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
        if match:
            tunnel_url = match.group(0)
            TUNNEL_URL_FILE.write_text(tunnel_url, encoding="utf-8")
            print("=" * 60)
            print(f"PUBLIC_URL: {tunnel_url}")
            print("=" * 60)
            sys.stdout.flush()
    if time.time() - start_time > 30 and not tunnel_url:
        print("Timeout waiting for tunnel URL")
        break

# Keep running
try:
    while True:
        time.sleep(1)
        if st_proc.poll() is not None:
            print("Streamlit process ended unexpectedly.")
            break
        if cf_proc.poll() is not None:
            print("Cloudflare process ended unexpectedly.")
            break
except KeyboardInterrupt:
    st_proc.terminate()
    cf_proc.terminate()
