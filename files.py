from datetime import datetime
import os
from pathlib import Path
from config import CACHE_DIR, FILES_DIR

def cache():
    try:
        folder = Path(CACHE_DIR)
        files = [f for f in folder.glob("*") if f.is_file()]
        return max(files, key=lambda f: f.stat().st_mtime) if files else None
    except Exception:
        return None

def create(p, content):
    try:
        os.makedirs(FILES_DIR, exist_ok=True)
        target = Path(FILES_DIR) / p
        if content:
            mode = "wb" if isinstance(content, bytes) else "w"
            enc = {} if isinstance(content, bytes) else {"encoding": "utf-8"}
            with open(target, mode, **enc) as f:
                f.write(content)
            return f"✅ Created {p}"
        os.makedirs(CACHE_DIR, exist_ok=True)
        cached_file = cache()
        if not cached_file:
            return "❌ Cache is empty"
        try:
            data = cached_file.read_bytes()
            try:
                target.write_text(data.decode("utf-8"), encoding="utf-8")
            except UnicodeDecodeError:
                target.write_bytes(data)
            return f"✅ Created {p} from cache ({cached_file.name})"
        except Exception as e:
            return f"❌ Cache read failed: {e}"
    except Exception as e:
        return f"❌ Create failed: {e}"

def read(p):
    try:
        return Path(p).read_text(encoding="utf-8")
    except FileNotFoundError:
        cached_file = cache()
        if cached_file:
            try:
                return cached_file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                return "❌ Cache read failed"
        return f"❌ File not found: {p}"
    except Exception as e:
        return f"❌ Read error: {e}"


def delete(p):
    try:
        target = Path(FILES_DIR) / p
        target.unlink()
        return f"🗑 Deleted {p}"
    except FileNotFoundError:
        return f"❌ File not found: {p}"
    except Exception as e:
        return f"❌ Delete failed: {e}"


def ls():
    try:
        entries = sorted(os.listdir(FILES_DIR))
        output = "\n".join(entries) if entries else "Empty"
        return output
    except FileNotFoundError:
        return "❌ Files dir not found"
    except Exception as e:
        return f"❌ List failed: {e}"

def ls_cache():
    try:
        entries = sorted(os.listdir(CACHE_DIR))
        output = "\n".join(entries) if entries else "Empty"
        return output
    except FileNotFoundError:
        return "❌ Cache dir not found"
    except Exception as e:
        return f"❌ List cache failed: {e}"