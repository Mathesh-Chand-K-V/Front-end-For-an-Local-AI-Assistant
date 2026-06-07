import subprocess
from pathlib import Path
from config import CACHE_DIR, FILES_DIR
from files import cache


def run_python(file):
    """Execute a Python file and return output or error."""
    try:
        if file:
            path = Path(FILES_DIR) / file
            if not path.exists():
                return f"❌ File not found: {file}"
        else:
            cached_file = cache()
            if not cached_file:
                return "❌ Cache is empty"
            path = cached_file

        if not path.suffix == ".py":
            return f"❌ Not a Python file: {path.name}"

        result = subprocess.run(
            ["python", str(path)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return f"❌ Runtime error:\n{result.stderr or result.stdout}"
        
        return result.stdout.strip() or "✅ Executed with no output"

    except subprocess.TimeoutExpired:
        return "❌ Script timed out (30s limit)"
    except FileNotFoundError:
        return "❌ Python interpreter not found"
    except Exception as e:
        return f"❌ Execution failed: {e}"