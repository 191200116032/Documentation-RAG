# # loaders/url_loader.py
# import requests
# from urllib.parse import urlparse
#
# def is_valid_txt_url(url: str) -> bool:
#     """Return True for http(s) URLs that end with .txt"""
#     try:
#         p = urlparse(url)
#         return p.scheme in ("http", "https") and url.lower().endswith(".txt")
#     except Exception:
#         return False
#
# def fetch_text(url: str, timeout: int = 15) -> str:
#     """Fetch text content from URL. Raises requests.HTTPError on non-200."""
#     resp = requests.get(url, timeout=timeout)
#     resp.raise_for_status()
#     return resp.text
