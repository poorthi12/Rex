
import json

import httpx

from app.config import settings


async def generate_json(prompt: str) -> dict:
    """Ask the local Ollama model to return a JSON object."""

    url = f"{settings.ollama_host.rstrip('/')}/api/chat"

    payload = {
        "model": settings.ollama_model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are the language understanding engine for REX, "
                    "a voice-controlled assistant. Follow the user's task "
                    "instructions and return valid JSON when requested."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0},
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Check that Ollama is running."
        ) from exc

    try:
        content = response.json()["message"]["content"]
        result = json.loads(content)
    except (ValueError, KeyError, TypeError) as exc:
        raise RuntimeError("Ollama returned an invalid JSON response.") from exc

    if not isinstance(result, dict):
        raise RuntimeError("Ollama must return a JSON object.")

    return result

