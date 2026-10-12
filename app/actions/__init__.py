
from app.actions.utility_actions import calculate, tell_date, tell_time
from app.actions.web_actions import open_website
from app.execution.registry import register_action, list_actions


def register_builtin_actions() -> None:
    actions = {
        "tell_time": tell_time,
        "tell_date": tell_date,
        "calculate": calculate,
        "open_website": open_website,
    }

    registered = set(list_actions())

    for name, function in actions.items():
        if name not in registered:
            register_action(name, function)
