
from app.intelligence.prompts import INTENT_PROMPT
from app.integrations.llm_client import generate_json
from app.models.intent import Intent


async def detect_intent(user_text: str) -> Intent:
    """Convert natural-language text into a validated intent."""

    cleaned_text = user_text.strip()

    if not cleaned_text:
        raise ValueError("Please provide a command.")

    prompt = INTENT_PROMPT.format(user_text=cleaned_text)
    result = await generate_json(prompt)

    try:
        return Intent.model_validate(result)
    except Exception as exc:
        raise RuntimeError("REX could not interpret the command safely.") from exc
