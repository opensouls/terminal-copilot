from dataclasses import dataclass

from copilot.conversation import Model
from copilot.parse_os import OperatingSystem

# dataclass for context
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
