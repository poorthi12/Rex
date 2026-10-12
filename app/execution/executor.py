
from app.execution.registry import get_action
from app.models.intent import ActionResult, Intent


def execute_intent(intent: Intent) -> ActionResult:
    """Validate and execute a registered REX action."""

    if intent.needs_clarification:
        return ActionResult(
            status="clarification",
            message=(
                intent.clarification_question
                or "Could you clarify what you want me to do?"
            ),
        )

    action = get_action(intent.name)

    if action is None:
        return ActionResult(
            status="unsupported",
            message="I don't know how to perform that action yet.",
        )

    try:
        result = action(**intent.parameters)

        return ActionResult(
            status="success",
            message="Done.",
            data=result if isinstance(result, dict) else {"result": result},
        )

    except (ValueError, TypeError) as exc:
        return ActionResult(
            status="rejected",
            message=str(exc),
        )

    except Exception:
        return ActionResult(
            status="failed",
            message="Something went wrong while executing that action.",
        )
