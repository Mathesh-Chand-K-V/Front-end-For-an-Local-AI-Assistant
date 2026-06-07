import subprocess


def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.stdout or result.stderr or "✅ Done (no output)"
    except subprocess.TimeoutExpired:
        return "❌ Command timed out"
    except Exception as e:
        return f"❌ {e}"
