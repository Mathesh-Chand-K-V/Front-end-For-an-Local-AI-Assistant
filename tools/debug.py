import os
from datetime import datetime
from pathlib import Path
from ai import chat_once
from files import read, cache
from config import CACHE_DIR
MAX_RETRIES = 3
def _clean_code(text):
    skip_patterns = {"pip install", "make sure", "this code", "example","below", "output:", "here is", "here's", "certainly", "i'm sorry", "i apologize", "as an ai", "i cannot", "i don't have", "i do not have"}
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            continue
        if any(p in s.lower() for p in skip_patterns):
            continue
        out.append(line)
    return "\n".join(out).strip()
def _validate(code):
    try:
        compile(code, "<string>", "exec")
        return True, None
    except SyntaxError as e:
        return False, str(e)
def _save(code, label):
    os.makedirs(CACHE_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path(CACHE_DIR) / f"debugged_{label}_{stamp}.py"
    path.write_text(code, encoding="utf-8")
    return path
def debug(file):
    if file:
        src_path = f"files/{file}"
        label = Path(file).stem
        original = read(src_path)
    else:
        cached = cache()
        if not cached:
            return "❌ Cache is empty"
        label = cached.stem
        try:
            original = cached.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            return f"❌ Cache read failed: {e}"
    if original.startswith("❌"):
        return original
    code = _clean_code(original)
    err = None
    for attempt in range(MAX_RETRIES):
        if attempt == 0:
            prompt = (
                "Fix this Python file so it runs without errors.\n"
                "Return ONLY valid Python code — no markdown, no comments, no explanations.\n"
                "Check for: syntax errors, logic bugs, wrong variable names, missing imports, "
                "UI framework misuse, state management problems.\n"
                "If data is missing, use reasonable sample data.\n\n"
                f"{code}"
            )
        else:
            prompt = (
                f"This Python code still has an error:\n{err}\n\n"
                "Fix it. Return ONLY valid Python code — no markdown, no comments.\n\n"
                f"{code}"
            )

        raw = chat_once(prompt)
        code = _clean_code(raw)
        valid, err = _validate(code)
        if valid:
            break
    else:
        return f"❌ Could not fix after {MAX_RETRIES} attempts. Last error:\n{err}"

    saved = _save(code, label)
    return f"✅ Debugged → {saved}\n\n{code}"