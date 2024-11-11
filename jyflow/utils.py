import importlib
from typing import Any

import toml


def load_system_prompt() -> Any:
    with importlib.resources.open_text('jyflow', 'prompts.toml') as file:
        config = toml.load(file)
    return config["summary_processor"]["system_prompt"]
