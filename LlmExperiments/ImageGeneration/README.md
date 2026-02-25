# ImageGeneration (uv)

This folder contains two scripts that generate images using:
- Gemini API (`gemini_generate_images.py`)
- ChatGPT/OpenAI Images API (`chatgpt_generate_images.py`)

## Setup (uv)

Create a virtual environment and install dependencies:

```bash
cd LlmExperiments/ImageGeneration
uv sync
```

## Configuration

Create `config/models.json`:

```json
{
  "gemini_models": ["imagen-4.0-generate-001"],
  "chatgpt_models": ["gpt-image-1"]
}
```

Add prompt text files under `prompts/` (UTF-8). Each file is one prompt. The filename (without extension) becomes `{prompt_name}`.

## Environment variables

- `GEMINI_API_KEY`: required for Gemini script
- `OPENAI_API_KEY`: required for ChatGPT/OpenAI script

## Run

```bash
# Gemini
uv run  --env-file .env python gemini_generate_images.py

# ChatGPT/OpenAI
uv run  --env-file .env  python chatgpt_generate_images.py
```

## Output paths

- Gemini: `results/imgs/gemini/{model_name}_{prompt_name}.png`
- ChatGPT/OpenAI: `results/imgs/chatGPT/{model_name}_{prompt_name}.png`

