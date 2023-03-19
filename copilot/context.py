from dataclasses import dataclass

from conversation import Model


@dataclass
class Context:
    shell: str
    operating_system: str
    directory: str
    directory_list: list[str]
    history: str
    command: str
    git: str
    model: Model
