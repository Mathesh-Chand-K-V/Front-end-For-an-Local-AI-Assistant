import os
import readline
from rich.console import Console
from rich.markdown import Markdown
from watch_dog import ensure_ollama
from router import route
console = Console()
HISTORY_FILE = ".history"
def smart_print(text):
    if not text:
        return    
    try:
        text_str = str(text)
        has_markdown = any(c in text_str for c in ("#", "*", "`", "[", "|"))
        if has_markdown and len(text_str) > 10:
            console.print(Markdown(text_str))
        else:
            print("Jarvis:", text_str)
    except Exception:
        print("Jarvis:", text)

HELP = """
⚡ JARVIS COMMANDS

FILES:
  !create <file> | <content>   Create a file (omit content to use cache)
  !read   <file>               Print file contents
  !delete <file>               Delete a file
  !ls                          List files/
  !ls_cache                    List cache_files/

AI / CODE:
  !gen  <file> | <task>        Generate Python code (file optional)
  !run  <file.py>              Run a Python file (blank = last cache)
  !debug <file>                AI-debug a Python file (blank = last cache)

TOOLS:
  !readsmart <file>            AI summarise a file
  !ocr <file>                  Extract text from image/PDF
  !fetch <url>                 Fetch and clean a web page
  !sys <shell command>         Run a system command

IMAGE GENERATION:
  !gen-img | <prompt>          Generate image from text
  !img2img <image> | <prompt>  Modify existing image
  !upscale <image>             Enhance image resolution
  !sd-models                   List available models
  
CHAINING:
  Use ~ to run multiple commands in sequence
  Example: !gen test.py | write hello world ~ !run test.py

TYPE  exit  to quit.
"""

def main():
    ensure_ollama()
    if os.path.exists(HISTORY_FILE):
        try:
            readline.read_history_file(HISTORY_FILE)
        except Exception:
            pass
    readline.set_history_length(1000)
    print("⚡ Jarvis ready  (!help)\n")
    while True:
        try:
            user = input("You: ").strip()
            
            if not user:
                continue
            
            if user.lower() == "exit":
                break
            
            if user == "!help":
                print(HELP)
                continue

            for cmd in user.split("~"):
                cmd = cmd.strip()
                if not cmd:
                    continue
                
                result = route(cmd)
                if result is not None:
                    smart_print(result)
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted — type 'exit' to quit")
        except EOFError:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    try:
        readline.write_history_file(HISTORY_FILE)
    except Exception:
        pass
    print("👋 Bye")

if __name__ == "__main__":
    main()