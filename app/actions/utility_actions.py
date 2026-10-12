
import ast
import operator
from datetime import datetime


def tell_time() -> dict:
    """Return the current local time."""
    now = datetime.now().astimezone()
    return {
        "time": now.strftime("%I:%M %p"),
        "timezone": str(now.tzinfo),
    }


def tell_date() -> dict:
    """Return today's local date."""
    now = datetime.now().astimezone()
    return {"date": now.strftime("%A, %d %B %Y")}


def calculate(expression: str) -> dict:
    """Safely evaluate basic arithmetic without using eval()."""

    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp):
            operation = operations.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported mathematical operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent is too large.")

            result = operation(left, right)

            if isinstance(result, complex) or abs(result) > 1e100:
                raise ValueError("Calculation result is too large.")

            return result

        if isinstance(node, ast.UnaryOp):
            operation = operations.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported mathematical operator.")
            return operation(evaluate(node.operand))

        raise ValueError("Invalid mathematical expression.")

    if not expression.strip() or len(expression) > 100:
        raise ValueError("Enter a valid mathematical expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)
        return {"expression": expression, "result": result}
    except (SyntaxError, TypeError, ZeroDivisionError, OverflowError):
        raise ValueError("Invalid or undefined calculation.") from None
