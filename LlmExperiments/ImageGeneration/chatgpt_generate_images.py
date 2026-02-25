import os
from pathlib import Path
from typing import Any, Dict, List

from openai import OpenAI

from utils import (
    BASE_DIR,
    ensure_output_dir,
    load_config,
    load_prompts,
    save_base64_png,
    safe_filename,
)
OUTPUT_DIR = BASE_DIR / "results" / "imgs" / "chatGPT"


def get_chatgpt_models(config: Dict[str, Any]) -> List[str]:
    """
    Extract the ChatGPT (OpenAI) image model list from the loaded config.
    """
    models = config.get("chatgpt_models")
    if not models:
        raise KeyError("Config must contain key 'chatgpt_models' with a non-empty list of model names.")
    if not isinstance(models, list):
        raise TypeError("Config value for 'chatgpt_models' must be a list.")

    return [str(m) for m in models]


def create_openai_client() -> OpenAI:
    """
    Create an OpenAI client using the OPENAI_API_KEY environment variable.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Environment variable 'OPENAI_API_KEY' is not set.")

    return OpenAI(api_key=api_key)


def generate_images_for_all() -> None:
    """
    Main entry point:
    - Read prompts from prompts/
    - Read model list from config/models.json (chatgpt_models)
    - Generate one image per (model, prompt) pair using OpenAI image models
    - Save images to results/imgs/chatGPT/{model_name}__{prompt_name}.png
    """
    config = load_config()
    prompts = load_prompts()
    models = get_chatgpt_models(config)
    ensure_output_dir(OUTPUT_DIR)

    client = create_openai_client()

    for model_name in models:
        for prompt_name, prompt_text in prompts.items():
            out_name = f"{safe_filename(model_name)}__{safe_filename(prompt_name)}.png"
            output_path = OUTPUT_DIR / out_name
            print(f"Generating image with ChatGPT model '{model_name}' for prompt '{prompt_name}' -> {output_path}")

            response = client.images.generate(
                model=model_name,
                prompt=prompt_text,
                size="1024x1024",
                n=1,
            )

            if not response.data:
                print(f"Warning: No images generated for model={model_name}, prompt={prompt_name}")
                continue

            image_b64 = response.data[0].b64_json
            save_base64_png(image_b64, output_path)


if __name__ == "__main__":
    generate_images_for_all()
