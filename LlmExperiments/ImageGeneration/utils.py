import base64
import json
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR / "prompts"
CONFIG_PATH = BASE_DIR / "config" / "models.json"


def load_config() -> Dict[str, Any]:
    """
    Load model configuration from config/models.json.

    Expected JSON structure:
    {
        "gemini_models": ["imagen-4.0-generate-001", "gemini-2.5-flash-image", ...],
        "chatgpt_models": ["gpt-image-1", "..."]
    }
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_prompts() -> Dict[str, str]:
    """
    Load all prompt files from the prompts/ directory.
    Each file is treated as one prompt.
    - File name (without extension) is used as prompt_name.
    - File content (UTF-8 text) is used as the prompt text.
    """
    if not PROMPTS_DIR.exists():
        raise FileNotFoundError(f"Prompts directory not found: {PROMPTS_DIR}")

    prompts: Dict[str, str] = {}
    for path in PROMPTS_DIR.iterdir():
        if path.is_file() and not path.name.startswith("."):
            prompt_name = path.stem
            prompt_text = path.read_text(encoding="utf-8")
            if prompt_text.strip():
                prompts[prompt_name] = prompt_text.strip()

    if not prompts:
        raise ValueError("No prompt files found in prompts/ directory.")

    return prompts


def ensure_output_dir(path: Path) -> None:
    """
    Ensure that an output directory exists.
    """
    path.mkdir(parents=True, exist_ok=True)


def save_base64_png(b64_data: str, path: Path) -> None:
    """
    Decode base64 PNG data and save it to the given path.
    """
    image_bytes = base64.b64decode(b64_data)
    with path.open("wb") as f:
        f.write(image_bytes)


def safe_filename(s: str) -> str:
    """
    Normalize a string so it is safe for use as a filename.
    Shared between Gemini and ChatGPT image generators.
    """
    return s.replace("/", "__").replace(":", "_")


