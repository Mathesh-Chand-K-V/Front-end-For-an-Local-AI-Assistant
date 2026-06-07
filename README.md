# JARVIS - Local AI Assistant

A modular, local-first AI assistant powered by Ollama, designed to perform intelligent conversations, document processing, OCR, web searches, memory management, command routing, and AI-powered file analysis.

---

## Features

### AI Chat
- Local LLM powered by Ollama
- Streaming responses
- Conversation history support
- Context-aware interactions

### Smart File Reading
Supports:

- PDF
- DOCX
- TXT
- Images
- OCR Scanned PDFs

The assistant automatically determines the best method for extracting information.

### OCR Engine
Extract text from:

- Images
- Scanned PDFs
- Screenshots
- Documents

Powered by:

- Tesseract OCR
- Poppler

### Memory System
Persistent memory storage for:

- User preferences
- Important notes
- Long-term context

Memory is stored locally.

### Web Search
Search and summarize information from the internet.

### Diffusion Integration
Generate AI images through local Stable Diffusion API.

### Modular Command Routing
Commands are automatically routed to the correct subsystem.

Example:

```text
!read document.pdf
!ocr image.png
!web latest AI news
!create image of a futuristic city
```

### Watchdog Service
Monitors:

- Ollama status
- Required background services
- Automatic recovery

---

# Project Structure

```text
.
├── main.py
├── router.py
├── executor.py
├── ai.py
├── memory.py
├── files.py
├── system.py
├── watch_dog.py
├── config.py
├── MEMORY.md
├── memory.json
│
├── tools/
│   ├── debug.py
│   ├── diffusion.py
│   ├── ocr.py
│   ├── smart_read.py
│   └── web.py
│
└── README.md
```

---

# Module Overview

## main.py

Application entry point.

Responsibilities:

- Start assistant
- Accept user commands
- Manage execution flow
- Coordinate modules

---

## router.py

Command routing engine.

Responsibilities:

- Parse user input
- Detect command intent
- Forward request to proper module

---

## executor.py

Execution manager.

Responsibilities:

- Execute routed commands
- Handle responses
- Manage tool invocation

---

## ai.py

LLM communication layer.

Responsibilities:

- Connect to Ollama
- Send prompts
- Receive responses
- Stream output

---

## memory.py

Persistent memory handler.

Responsibilities:

- Store memories
- Retrieve memories
- Update memory database

---

## files.py

File management utilities.

Responsibilities:

- File validation
- Path management
- File indexing

---

## system.py

System utilities.

Responsibilities:

- Process management
- Health checks
- Environment validation

---

## watch_dog.py

Background monitoring service.

Responsibilities:

- Detect Ollama crashes
- Restart services
- Monitor dependencies

---

# Tools

## smart_read.py

Advanced document reader.

Capabilities:

- PDF extraction
- OCR fallback
- Text analysis
- Large document support

---

## ocr.py

OCR engine.

Capabilities:

- Image OCR
- Scanned PDF OCR
- Text extraction

Dependencies:

- Tesseract
- Poppler

---

## diffusion.py

Stable Diffusion integration.

Capabilities:

- Text-to-image generation
- Image saving
- Prompt processing

---

## web.py

Web search utility.

Capabilities:

- Search web resources
- Retrieve information
- Summarize content

---

## debug.py

Developer debugging tools.

Capabilities:

- Logging
- Diagnostics
- Error tracing

---

# Configuration

All configuration values are stored inside:

```python
config.py
```

## Example Configuration

```python
OLLAMA_BASE         = "http://127.0.0.1:11434"
OLLAMA_URL          = f"{OLLAMA_BASE}/api/chat"
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE}/api/generate"

MODEL               = "<MODEL NAME>"

FILES_DIR           = "<PATH TO WORKSPACE FILES>"
CACHE_DIR           = "<PATH TO WORKSPACE CACHE FILES>"
SMART_READ_DIR      = "<PATH TO SMART READ CACHE>"

MEMORY_FILE         = "<PATH TO MEMORY FILE>"

OLLAMA_PATH         = "<PATH TO OLLAMA EXECUTABLE>"

TIMEOUT             = 120
STREAM_TIMEOUT      = 300

POPPLER_PATH        = "<PATH TO POPPLER>\\Library\\bin"
TESSERACT_PATH      = "<PATH TO TESSERACT>\\tesseract.exe"
```

---

# Installation

## 1. Clone Repository

```bash
git clone [https://github.com/Mathesh-Chand-K-V/JARVIS---Local-AI-Assistant]
cd "JARVIS---Local-AI-Assistant"
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

### Linux

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Ollama

Download and install Ollama.

After installation:

```bash
ollama serve
```

Pull a model:

```bash
ollama pull qwen3-coder
```

or

```bash
ollama pull llama3
```

---

## 5. Install Tesseract OCR

Download:

https://github.com/tesseract-ocr/tesseract

Update:

```python
TESSERACT_PATH
```

inside `config.py`.

---

## 6. Install Poppler

Download:

https://github.com/oschwartz10612/poppler-windows

Update:

```python
POPPLER_PATH
```

inside `config.py`.

---

# Usage

Start assistant:

```bash
python main.py
```

---

## Example Commands

### Chat

```text
hello jarvis
```

### Read Document

```text
!read report.pdf
```

### OCR

```text
!ocr image.png
```

### Search Web

```text
!web latest AI developments
```

### Generate Image

```text
!create cyberpunk city at sunset
```

---

# Memory System

Memories are stored locally in:

```text
memory.json
```

and documented through:

```text
MEMORY.md
```

The memory system allows the assistant to:

- Remember user preferences
- Store long-term notes
- Maintain contextual awareness

---

# Stable Diffusion Setup

Ensure your Stable Diffusion API is available:

```text
http://127.0.0.1:7860
```

Default endpoint:

```text
/sdapi/v1/txt2img
```

The generated images are automatically saved to:

```text
CACHE_DIR/images
```

---

# Recommended Models

### Coding

- Qwen3-Coder
- DeepSeek-Coder
- CodeLlama

### General Assistant

- Qwen3
- Llama 3
- Gemma 3

### Lightweight

- Phi-4
- Gemma 3 4B

---

# Troubleshooting

## Ollama Not Running

Check:

```bash
ollama list
```

or

```bash
ollama serve
```

---

## OCR Not Working

Verify:

```python
POPPLER_PATH
TESSERACT_PATH
```

are configured correctly.

---

## Stable Diffusion Not Responding

Verify:

```text
http://127.0.0.1:7860
```

is accessible.

---

## Timeout Errors

Increase:

```python
TIMEOUT
STREAM_TIMEOUT
```

inside `config.py`.

---

# Security

- Runs locally
- No cloud dependency required
- User data remains on device
- Memory stored locally
- Documents processed locally

---

# Future Improvements

- Voice Input
- Wake Word Detection
- RAG Knowledge Base
- ERP Integration
- Multi-Agent Architecture
- Vision Models
- Local Function Calling
- Autonomous Task Execution

---

# License

This project is intended for educational and personal use.

Modify, extend, and customize as required.
