from datetime import datetime
import requests
import os
import re
import html
from pathlib import Path
from config import CACHE_DIR
try:
    from googlesearch import search as google_search
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

def _clean_html(fragment):
    fragment = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', fragment, flags=re.S | re.I)
    fragment = re.sub(r'<!--.*?-->', ' ', fragment, flags=re.S)
    fragment = re.sub(r'<[^>]+>', ' ', fragment)
    fragment = html.unescape(fragment)
    fragment = re.sub(r'\s+', ' ', fragment)
    return fragment.strip()


def _extract_text(html_content):
    cleaned = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html_content, flags=re.S | re.I)
    chunks = []
    for tag in ['h1', 'h2', 'h3', 'h4', 'p', 'li', 'td', 'th', 'blockquote']:
        matches = re.findall(rf'<{tag}[^>]*>(.*?)</{tag}>', cleaned, flags=re.S | re.I)
        for m in matches:
            text = _clean_html(m)
            if len(text) >= 20:
                chunks.append(text)

    if chunks:
        return "\n".join(chunks)
    return _clean_html(cleaned)


def _duckduckgo_url(query):
    try:
        resp = requests.post("https://html.duckduckgo.com/html/",data={"q": query},headers={"User-Agent": "Mozilla/5.0"},timeout=10,)
        resp.raise_for_status()
        match = re.search(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"', resp.text)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def _first_url(query):
    if query.startswith("http://") or query.startswith("https://"):
        return query

    if GOOGLE_AVAILABLE:
        try:
            urls = list(google_search(query, num_results=1, lang="en"))
            if urls:
                return urls[0]
        except Exception:
            pass

    return _duckduckgo_url(query)


def fetch(query):
    url = _first_url(query)
    if not url:
        return f"❌ No results found for: {query}"
    try:
        r = requests.get(url,timeout=10,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},)
        r.raise_for_status()
        os.makedirs(CACHE_DIR, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        cache_path = Path(CACHE_DIR) / f"web_{stamp}.txt"
        cache_path.write_text(r.text, encoding="utf-8", errors="replace")
        text = _extract_text(r.text)
        if not text:
            return f"❌ No readable text found at: {url}"
        return f"Source: {url}\n\n{text[:8000]}"
    except requests.RequestException as e:
        return f"❌ Fetch error: {e}"