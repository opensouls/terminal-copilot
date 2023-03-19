from dataclasses import dataclass

from conversation import Model
from parse_os import OperatingSystem


@dataclass
class Context:
    shell: str
    operating_system: OperatingSystem
    directory: str
    directory_list: list[str]
    history: str
    command: str
    git: str
    model: Model
