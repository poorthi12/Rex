
from app.actions import register_builtin_actions
from app.execution.executor import execute_intent
from app.intelligence.intent_detector import detect_intent
from app.models.intent import ActionResult


# Register built-in actions when this service is imported.
register_builtin_actions()


async def process_command(user_text: str) -> ActionResult:
    """Interpret a user's command and safely execute a supported action."""

    try:
        intent = await detect_intent(user_text)
    except ValueError as exc:
        return ActionResult(status="rejected", message=str(exc))
    except Exception:
        return ActionResult(
            status="failed",
            message="REX couldn't understand the request right now. Please try again.",
        )

    # Normalize common spoken arithmetic phrases.
    if intent.name == "calculate":
        expression = intent.parameters.get("expression")

        if isinstance(expression, str):
            replacements = {
                " plus ": " + ",
                " minus ": " - ",
                " times ": " * ",
                " multiplied by ": " * ",
                " divided by ": " / ",
            }

            normalized = f" {expression.strip().lower()} "
            for phrase, symbol in replacements.items():
                normalized = normalized.replace(phrase, symbol)

            intent.parameters["expression"] = normalized.strip()

    return execute_intent(intent)
