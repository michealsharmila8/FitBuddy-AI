from functools import lru_cache

from google import genai

from .config import GOOGLE_API_KEY


@lru_cache(maxsize=1)
def get_gemini_client():

    if not GOOGLE_API_KEY:
        return None

    client = genai.Client(
        api_key=GOOGLE_API_KEY
    )

    return client


def generate_text(
    prompt: str,
    model: str
) -> str:

    client = get_gemini_client()

    if client is None:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured."
        )

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()