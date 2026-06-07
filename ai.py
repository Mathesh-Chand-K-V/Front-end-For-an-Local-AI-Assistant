import requests
import json
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from config import OLLAMA_URL, MODEL, TIMEOUT, STREAM_TIMEOUT

console = Console(width=100)

BASE_SYSTEM_PROMPT = """\
You are Jarvis, a precise and structured AI assistant.
Rules:
- Always respond in clean Markdown
- Use proper headings (##, ###) and bullet points (-)
- Keep spacing clean and readable
- Be concise and technical
Language:
- Respond ONLY in English unless user writes in another language
- Do NOT mix languages
Accuracy:
- If unsure, give best-effort answer and note uncertainty
- Do NOT refuse unless the request is unsafe
- Correct wrong technical terms before answering
"""

def build_system_prompt(context=""):
    base = BASE_SYSTEM_PROMPT.strip()
    return f"{context.strip()}\n\n{base}" if context.strip() else base

def clean_text(text):
    if not isinstance(text, str):
        return str(text)
    return text.encode("utf-8", "ignore").decode("utf-8")

def chat_once(prompt, context=""):
    try:
        response = requests.post(OLLAMA_URL,json={"model": MODEL,"messages": [{"role": "system", "content": build_system_prompt(context)},{"role": "user",   "content": clean_text(prompt)},],"stream": False,},timeout=TIMEOUT,)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "❌ Empty response")
    except requests.Timeout:
        return f"❌ AI request timed out ({TIMEOUT}s) — try a shorter prompt"
    except requests.RequestException as e:
        return f"❌ AI Error: {e}"
    except (KeyError, ValueError) as e:
        return f"❌ AI response parse error: {e}"

def stream_from_model(prompt, context=""):
    try:
        response = requests.post(OLLAMA_URL,json={"model": MODEL,"messages": [{"role": "system", "content": build_system_prompt(context)},{"role": "user",   "content": clean_text(prompt)},],"stream": True,},stream=True,timeout=STREAM_TIMEOUT,)
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            try:
                chunk = json.loads(line.decode("utf-8"))
                if "message" in chunk:
                    yield clean_text(chunk["message"].get("content", ""))
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
    except requests.Timeout:
        yield f"\n❌ Streaming timed out ({STREAM_TIMEOUT}s)"
    except requests.RequestException as e:
        yield f"\n❌ Streaming Error: {e}"

def chat(prompt, context=""):
    buffer = ""
    try:
        with Live("", console=console, refresh_per_second=4) as live:
            live.update("🧠 Thinking...")
            for chunk in stream_from_model(prompt, context):
                buffer += chunk
                try:
                    live.update(Markdown(buffer, code_theme="monokai", justify="left"))
                except Exception:
                    live.update(buffer)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        print()