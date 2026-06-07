import os
import base64
import requests
from datetime import datetime
from pathlib import Path
from config import CACHE_DIR
DIFFUSION_API      = "http://127.0.0.1:7860"
TXT2IMG_ENDPOINT   = f"{DIFFUSION_API}/sdapi/v1/txt2img"
IMG2IMG_ENDPOINT   = f"{DIFFUSION_API}/sdapi/v1/img2img"
UPSCALE_ENDPOINT   = f"{DIFFUSION_API}/sdapi/v1/extra-single-image"
OPTIONS_ENDPOINT   = f"{DIFFUSION_API}/sdapi/v1/options"
IMAGE_DIR          = os.path.join(CACHE_DIR, "images")
def _save_image(image_bytes, name):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name[:40])
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    out = Path(IMAGE_DIR) / f"{safe}_{stamp}.png"
    out.write_bytes(image_bytes)
    return str(out)
def generate_image(prompt,negative_prompt="blurry, low quality, watermark",steps=20,cfg_scale=7,width=1080,height=1080,):
    try:
        response = requests.post(TXT2IMG_ENDPOINT,json={"prompt":prompt,"negative_prompt": negative_prompt,"steps": steps,"cfg_scale": cfg_scale,"width": width,"height": height,"batch_size": 1,"n_iter": 1,"seed": -1,},timeout=180,)
        response.raise_for_status()
        result = response.json()
        if not result.get("images"):
            return "❌ No image returned"
        image_bytes = base64.b64decode(result["images"][0])
        saved = _save_image(image_bytes, prompt)
        return f"✅ Image saved → {saved}"
    except requests.ConnectionError:
        return "❌ WebUI/SD not running — start it first (python main.py in ComfyUI dir)"
    except Exception as e:
        return f"❌ Image Generation Error: {e}"
def img2img(input_path,prompt,strength=0.75,negative_prompt="blurry, low quality",steps=20,cfg_scale=7,):
    try:
        if not os.path.exists(input_path):
            return f"❌ File not found: {input_path}"
        image_data = base64.b64encode(Path(input_path).read_bytes()).decode("utf-8")
        response = requests.post(IMG2IMG_ENDPOINT,json={"prompt": prompt,"negative_prompt": negative_prompt,"init_images": [image_data],"denoising_strength": strength,"steps": steps,"cfg_scale": cfg_scale,"sampler_name": "Euler a",},timeout=180,)
        response.raise_for_status()
        result = response.json()
        if not result.get("images"):
            return "❌ No image returned"
        image_bytes = base64.b64decode(result["images"][0])
        saved = _save_image(image_bytes, f"img2img_{prompt}")
        return f"✅ Image saved → {saved}"
    except requests.ConnectionError:
        return "❌ WebUI/SD not running"
    except Exception as e:
        return f"❌ Img2Img Error: {e}"
def upscale(input_path, scale_factor=2, upscaler="RealESRGAN_x2plus"):
    try:
        if not os.path.exists(input_path):
            return f"❌ File not found: {input_path}"
        image_data = base64.b64encode(Path(input_path).read_bytes()).decode("utf-8")
        response = requests.post(UPSCALE_ENDPOINT,json={"image": image_data,"upscaling_resize": scale_factor,"upscaler_1": upscaler,},timeout=120,)
        response.raise_for_status()
        result = response.json()
        if "image" not in result:
            return "❌ No image returned"
        image_bytes = base64.b64decode(result["image"])
        saved = _save_image(image_bytes, f"upscaled_x{scale_factor}")
        return f"✅ Upscaled → {saved}"
    except requests.ConnectionError:
        return "❌ WebUI/SD not running"
    except Exception as e:
        return f"❌ Upscale Error: {e}"
def current_model():
    try:
        response = requests.get(OPTIONS_ENDPOINT, timeout=10)
        response.raise_for_status()
        return response.json().get("sd_model_checkpoint", "Unknown")
    except requests.ConnectionError:
        return "❌ WebUI/SD not running"
    except Exception as e:
        return f"❌ Model Error: {e}"
def switch_model(model_name):
    try:
        response = requests.post(OPTIONS_ENDPOINT,json={"sd_model_checkpoint": model_name},timeout=60,)
        response.raise_for_status()
        return f"✅ Model switched → {model_name}"
    except requests.ConnectionError:
        return "❌ WebUI/SD not running"
    except Exception as e:
        return f"❌ Model Switch Error: {e}"