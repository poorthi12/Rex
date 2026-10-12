
from collections.abc import Callable
from typing import Any

ActionFunction = Callable[..., Any]

_ACTIONS: dict[str, ActionFunction] = {}


def register_action(name: str, function: ActionFunction) -> None:
    """Register a Python function as an available assistant action."""
    if not name or not name.strip():
        raise ValueError("Action name cannot be empty.")

    if not callable(function):
        raise TypeError("Action must be callable.")

    if name in _ACTIONS:
        raise ValueError(f"Action already registered: {name}")

    _ACTIONS[name] = function


def get_action(name: str) -> ActionFunction | None:
    """Return a registered action, if available."""
    return _ACTIONS.get(name)


def list_actions() -> list[str]:
    """Return all registered action names."""
    return sorted(_ACTIONS.keys())


def clear_actions() -> None:
    """Clear the registry, primarily for tests."""
    _ACTIONS.clear()
