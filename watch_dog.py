import subprocess
import requests
import time
import psutil
from config import OLLAMA_BASE, OLLAMA_GENERATE_URL, OLLAMA_PATH, MODEL, TIMEOUT


def is_ollama_running():
    try:
        return requests.get(OLLAMA_BASE, timeout=2).status_code == 200
    except Exception:
        return False


def kill_existing():
    for p in psutil.process_iter(["name"]):
        try:
            if p.info["name"] and p.info["name"].lower() == "ollama.exe":
                p.kill()
        except Exception:
            pass


def start_ollama():
    print("🚀 Starting Ollama...")
    try:
        subprocess.Popen(
            [OLLAMA_PATH, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception as e:
        print(f"❌ Failed to start Ollama: {e}")
        return False


def wait_until_ready():
    print("⏳ Waiting for Ollama...")
    deadline = time.time() + TIMEOUT
    while time.time() < deadline:
        if is_ollama_running():
            print("✅ Ollama is running")
            return True
        time.sleep(1)
    print("❌ Ollama failed to start in time")
    return False


def load_model():
    print(f"📦 Warming model: {MODEL}")
    try:
        requests.post(
            OLLAMA_GENERATE_URL,
            json={"model": MODEL, "prompt": "hi", "stream": False},
            timeout=30,
        )
        print("✅ Model warmed")
    except Exception:
        print("⚠️ Model warmup skipped")


def ensure_ollama():
    if is_ollama_running():
        print("✅ Ollama already running")
        return True
    kill_existing()
    if not start_ollama():
        return False
    if not wait_until_ready():
        return False
    load_model()
    return True


if __name__ == "__main__":
    ensure_ollama()
