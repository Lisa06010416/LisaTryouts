import os

from google import genai


def main() -> None:
    """
    List all available Gemini models using the GEMINI_API_KEY environment variable.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Environment variable 'GEMINI_API_KEY' is not set.")

    client = genai.Client(api_key=api_key)

    models = client.models.list()
    for m in models:
        print(m.name)


if __name__ == "__main__":
    main()
