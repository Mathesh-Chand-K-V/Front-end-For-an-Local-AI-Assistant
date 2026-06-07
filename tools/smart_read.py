import os
import time
from files import read, cache
from ai import chat_once
from config import CACHE_DIR, SMART_READ_DIR
def read_smart(file):
    if file:
        content = read(file)
    else:
        c = cache()
        if not c:
            return "❌ Cache is empty"
        content = open(f"{CACHE_DIR}/{c}", encoding="utf-8", errors="replace").read()
    prompt = f"Summarize this clearly and concisely:\n\n{content}"
    result = chat_once(prompt)
    os.makedirs(SMART_READ_DIR, exist_ok=True)   
    path = f"{SMART_READ_DIR}/{int(time.time())}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(result)
    return result
