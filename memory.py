import json
import os
from config import MEMORY_FILE

PROFILE_FILE = "MEMORY.md"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_memory(mem):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2)


def load_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
    return ""


memory = load_memory()


def update_memory(prompt):
    global memory
    p = prompt.lower()

    if "my name is" in p:
        memory["name"] = prompt.split("is", 1)[-1].strip()
    if "your name is" in p:
        memory["assistant_name"] = prompt.split("is", 1)[-1].strip()
    if "i like" in p:
        like = prompt.split("like", 1)[-1].strip().lower()
        if like:
            likes = memory.setdefault("likes", [])
            if like not in likes:
                likes.append(like)

    save_memory(memory)


def build_context():
    parts = []
    profile = load_profile()
    if profile:
        parts.append(profile.strip())
    if "assistant_name" in memory:
        parts.append(f"You are {memory['assistant_name']}.")
    if "name" in memory:
        parts.append(f"User name is {memory['name']}.")
    if "likes" in memory:
        parts.append(f"User prefers: {', '.join(memory['likes'])}.")
    parts.append(
        "Follow the identity strictly.\n"
        "Do not say you are another AI model.\n"
        "Be concise and practical."
    )
    return "\n\n".join(parts)