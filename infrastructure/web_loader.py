# infrastructure/web_loader.py
import requests
from urllib.parse import urlparse

def is_valid_txt_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        # recommend .txt but allow others (we only accept plain text)
        return True
    except:
        return False

def load_text_from_url(url: str, timeout: int = 10) -> str:
    if not is_valid_txt_url(url):
        raise ValueError("Invalid URL")
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    content_type = r.headers.get("content-type", "")
    # allow plain text and text/*, fall back to raw text
    if "text" not in content_type and "html" in content_type:
        # still allow HTML pages if they contain text - but generally expect .txt
        return r.text
    return r.text
