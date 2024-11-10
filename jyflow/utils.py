from typing import Any

import toml


def load_system_prompt() -> Any:
    with open("./prompts.toml", "r") as file:
        config = toml.load(file)
    return config["summary_processor"]["system_prompt"]
