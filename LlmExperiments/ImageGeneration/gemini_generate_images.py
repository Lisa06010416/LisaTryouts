import base64
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

from utils import BASE_DIR, ensure_output_dir, load_config, load_prompts, safe_filename
OUTPUT_DIR = BASE_DIR / "results" / "imgs" / "gemini"


def get_gemini_models(config: Dict[str, Any]) -> List[str]:
    models = config.get("gemini_models")
    if not models:
        raise KeyError("Config must contain key 'gemini_models' with a non-empty list of model names.")
    if not isinstance(models, list):
        raise TypeError("Config value for 'gemini_models' must be a list.")
    return [str(m).strip() for m in models if str(m).strip()]


def create_gemini_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Environment variable 'GEMINI_API_KEY' is not set.")

    # Force Developer API v1 (avoid v1beta/predict pitfalls)
    return genai.Client(
        api_key=api_key,
        http_options={"api_version": "v1beta"},
    )

def normalize_model_name(model_name: str) -> str:
    """
    Accept both:
      - "models/gemini-2.5-flash-image"
      - "gemini-2.5-flash-image"
    Return the short id (without "models/") for better compatibility.
    """
    model_name = model_name.strip()
    if model_name.startswith("models/"):
        return model_name[len("models/") :]
    return model_name


def detect_model_kind(model_name_short: str) -> str:
    """
    Returns:
      - "imagen" for imagen-4.* models
      - "gemini_image" for gemini-*-image or nano-banana* models
      - "unsupported" otherwise
    """
    m = model_name_short.lower()
    if m.startswith("imagen-"):
        return "imagen"
    if ("-image" in m) or ("nano-banana" in m) or ("exp-image-generation" in m):
        # cover: gemini-2.5-flash-image, gemini-3-pro-image-preview, nano-banana-pro-preview,
        #        gemini-2.0-flash-exp-image-generation
        return "gemini_image"
    return "unsupported"


# ---------- Image generation implementations ----------

def generate_image_with_imagen(
    client,
    model_name_short: str,
    prompt_text: str,
) -> Optional[bytes]:
    resp = client.models.generate_images(
        model=model_name_short,
        prompt=prompt_text,
        config=types.GenerateImagesConfig(number_of_images=1),
    )

    imgs = getattr(resp, "generated_images", None) or []
    if not imgs:
        try:
            print("DEBUG Imagen response:", resp.model_dump())
        except Exception:
            print("DEBUG Imagen response:", repr(resp))
        return None

    g0 = imgs[0]

    image_bytes = getattr(g0, "image_bytes", None)
    if isinstance(image_bytes, (bytes, bytearray)):
        return bytes(image_bytes)

    img_obj = getattr(g0, "image", None)
    if img_obj is not None:
        b = getattr(img_obj, "image_bytes", None)
        if isinstance(b, (bytes, bytearray)):
            return bytes(b)

    return None


def generate_image_with_gemini_generate_content(
    client: genai.Client,
    model_name_short: str,
    prompt_text: str,
) -> Optional[bytes]:
    """
    Use Gemini image-capable models via generate_content with response_modalities.
    Returns image bytes (decoded) or None.
    """
    resp = client.models.generate_content(
        model=model_name_short,
        contents=[prompt_text],
        config={
            "response_modalities": ["IMAGE", "TEXT"],
        },
    )

    candidates = getattr(resp, "candidates", None) or []
    for cand in candidates:
        content = getattr(cand, "content", None)
        if not content:
            continue
        parts = getattr(content, "parts", None) or []
        for part in parts:
            inline = getattr(part, "inline_data", None)
            if inline is None:
                # also print any text the model returns (useful for debugging)
                txt = getattr(part, "text", None)
                if txt:
                    print("MODEL_TEXT:", txt)
                continue

            data = getattr(inline, "data", None)
            if data is None:
                continue

            # data might be base64 str or bytes
            if isinstance(data, str):
                try:
                    return base64.b64decode(data)
                except Exception:
                    pass
            elif isinstance(data, (bytes, bytearray)):
                return bytes(data)

    return None


def save_image_bytes(image_bytes: bytes, output_path: Path) -> None:
    """
    Normalize and save as PNG for consistency.
    """
    img = Image.open(BytesIO(image_bytes))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, format="PNG")


def generate_images_for_all() -> None:
    config = load_config()
    prompts = load_prompts()
    models_raw = get_gemini_models(config)
    ensure_output_dir(OUTPUT_DIR)

    client = create_gemini_client()

    for model_raw in models_raw:
        model_short = normalize_model_name(model_raw)
        kind = detect_model_kind(model_short)

        for prompt_name, prompt_text in prompts.items():
            out_name = f"{safe_filename(model_short)}__{safe_filename(prompt_name)}.png"
            output_path = OUTPUT_DIR / out_name

            print(f"[{kind}] model='{model_short}' prompt='{prompt_name}' -> {output_path}")

            if kind == "imagen":
                image_bytes = generate_image_with_imagen(client, model_short, prompt_text)
            elif kind == "gemini_image":
                image_bytes = generate_image_with_gemini_generate_content(client, model_short, prompt_text)
            else:
                print(f"Skip unsupported model for image generation: {model_short}")
                continue

            if not image_bytes:
                print(f"Warning: No image generated for model={model_short}, prompt={prompt_name}")
                continue

            save_image_bytes(image_bytes, output_path)

    print("Done.")


if __name__ == "__main__":
    generate_images_for_all()