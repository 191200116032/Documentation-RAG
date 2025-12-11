# infrastructure/web_loader.py
import requests
from typing import Tuple

def load_text_from_url(url: str) -> Tuple[str, str]:
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        return None, "❌ URL must start with http:// or https://"

    try:
        r = requests.get(url, timeout=10)
    except Exception as e:
        return None, f"❌ Could not fetch URL: {e}"

    if r.status_code != 200:
        return None, f"❌ Failed to load document (HTTP {r.status_code})"

    if "text" not in r.headers.get("Content-Type", ""):
        return None, "❌ URL does not appear to contain plain text."

    return r.text, None
