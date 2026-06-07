import os
from pdf2image import convert_from_path
import pytesseract
import pdfplumber
from PIL import Image
from config import CACHE_DIR,POPPLER_PATH, TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def _is_scanned(path, threshold=30):
    try:
        with pdfplumber.open(path) as pdf:
            total = sum(len((p.extract_text() or "").strip()) for p in pdf.pages)
        return total < threshold
    except Exception:
        return True

def _extract_pdf_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(p.extract_text() or "" for p in pdf.pages).strip()

def _ocr_pdf(path):
    images = convert_from_path(path, dpi=200, poppler_path=POPPLER_PATH)
    return "\n".join(
        pytesseract.image_to_string(img, config="--psm 6") for img in images
    ).strip()

def _ocr_image(path):
    return pytesseract.image_to_string(Image.open(path), config="--psm 6").strip()

def _save(text, source_path):
    os.makedirs(CACHE_DIR, exist_ok=True)
    base = os.path.splitext(os.path.basename(source_path))[0]
    out = f"{CACHE_DIR}/{base}_ocr.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    return out

def extract_text(path, save=True):
    try:
        if path.lower().endswith(".pdf"):
            text = _ocr_pdf(path) if _is_scanned(path) else _extract_pdf_text(path)
        else:
            text = _ocr_image(path)
        if save:
            saved = _save(text, path)
            return f"✅ OCR saved → {saved}\n\n{text}"
        return text
    except Exception as e:
        return f"❌ OCR Error: {e}"
