import os
from datetime import datetime
from pathlib import Path
from files import create, read, delete, ls, ls_cache
from executor import run_python
from ai import chat, chat_once
from memory import update_memory, build_context, memory
from config import CACHE_DIR, FILES_DIR

def clean_code(text):
    skip_patterns = {"pip install", "make sure", "this code", "example","below", "output:", "here is", "here's", "certainly","# example", "# this is", }
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            continue
        if any(p in s.lower() for p in skip_patterns):
            continue
        out.append(line)
    return "\n".join(out).strip()

def validate_python(code):
    try:
        compile(code, "<string>", "exec")
        return True, None
    except SyntaxError as e:
        return False, str(e)


def _parse(cmd):
    if "|" in cmd:
        left, right = cmd.split("|", 1)
        return left.strip().split(), right.strip()
    parts = cmd.split(maxsplit=2)
    return parts, parts[2] if len(parts) > 2 else ""

def _tool(module, fn):
    try:
        import importlib
        mod = importlib.import_module(f"tools.{module}")
        func = getattr(mod, fn, None)
        return func if callable(func) else None
    except (ImportError, AttributeError):
        return None


def route(cmd):
    cmd_stripped = cmd.strip()
    cmd_lower = cmd_stripped.lower()
    if cmd_lower in ("who am i", "what is my name"):
        return f"You are {memory.get('name', 'Mathesh')}"
    if cmd_lower in ("who are you", "what is your name"):
        return f"I am {memory.get('assistant_name', 'Jarvis')}"
    parts, content = _parse(cmd_stripped)
    if not parts:
        return None
    command = parts[0].lower()
    if command == "!create":
        if len(parts) < 2:
            return "❌ Usage: !create <file> | <content>"
        return create(parts[1], content)
    if command == "!read":
        if len(parts) < 2:
            return "❌ Usage: !read <file>"
        return read(f"{FILES_DIR}/{parts[1]}")
    if command == "!delete":
        if len(parts) < 2:
            return "❌ Usage: !delete <file>"
        return delete(parts[1])
    if command == "!ls":
        return ls()
    if command == "!ls_cache":
        return ls_cache()
    if command == "!gen":
        if not content:
            return "❌ Usage: !gen <file> | <task description>"
        filename = parts[1] if len(parts) > 1 else ""
        prompt = (
            "You are a Python code generator. "
            "Return ONLY valid, compact Python code — no markdown, no explanations, no comments. "
            "It must be correct in syntax and logic and produce no runtime errors. "
            "If data is needed and not given, use reasonable sample data.\n"
            f"Task: {content}"
        )
        raw = chat_once(prompt)
        code = clean_code(raw)
        valid, err = validate_python(code)
        if not valid:
            return f"❌ Generated code has syntax error:\n{err}"
        if filename:
            os.makedirs(FILES_DIR, exist_ok=True)
            path = Path(FILES_DIR) / filename
        else:
            os.makedirs(CACHE_DIR, exist_ok=True)
            stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = Path(CACHE_DIR) / f"gen_{stamp}.py"
        path.write_text(code, encoding="utf-8")
        return f"✅ Generated → {path}\n\n{code}"
    if command == "!run":
        return run_python(parts[1] if len(parts) > 1 else "")
    if command == "!fetch":
        if len(parts) < 2:
            return "❌ Usage: !fetch <url or search query>"
        fn = _tool("web", "fetch")
        return fn(" ".join(parts[1:])) if fn else "❌ web.py not found"
    if command == "!ocr":
        if len(parts) < 2:
            return "❌ Usage: !ocr <file>"
        fn = _tool("ocr", "extract_text")
        return fn(parts[1]) if fn else "❌ ocr.py not found"
    if command == "!readsmart":
        fn = _tool("smart_read", "read_smart")
        return fn(parts[1] if len(parts) > 1 else "") if fn else "❌ smart_read.py not found"
    if command == "!debug":
        fn = _tool("debug", "debug")
        return fn(parts[1] if len(parts) > 1 else "") if fn else "❌ debug.py not found"
    if command == "!sys":
        if len(parts) < 2:
            return "❌ Usage: !sys <command>"
        fn = _tool("system", "run_cmd")
        return fn(" ".join(parts[1:])) if fn else "❌ system.py not found"
    if command == "!gen-img":
        if not content:
            return "❌ Usage: !gen-img | <prompt>"
        fn = _tool("diffusion", "generate_image")
        return fn(content) if fn else "❌ diffusion.py not found"
    if command == "!img2img":
        if len(parts) < 2 or not content:
            return "❌ Usage: !img2img <image.png> | <prompt>"
        fn = _tool("diffusion", "img2img")
        return fn(parts[1], content) if fn else "❌ diffusion.py not found"
    if command == "!upscale":
        if len(parts) < 2:
            return "❌ Usage: !upscale <image.png>"
        fn = _tool("diffusion", "upscale")
        return fn(parts[1]) if fn else "❌ diffusion.py not found"
    if command == "!sd-model":
        fn = _tool("diffusion", "current_model")
        return fn() if fn else "❌ diffusion.py not found"
    if command == "!switch-model":
        if len(parts) < 2:
            return "❌ Usage: !switch-model <model_name>"
        fn = _tool("diffusion", "switch_model")
        return fn(parts[1]) if fn else "❌ diffusion.py not found"
    if command.startswith("!"):
        return f"❌ Unknown command: {command}  (type !help)"
    update_memory(cmd_stripped)
    chat(cmd_stripped, build_context())
    return None