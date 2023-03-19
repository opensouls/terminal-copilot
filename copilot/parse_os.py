import enum


class OperatingSystem(enum.Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "macOS"
    OTHER = "Other"

    def is_unix(self):
        return self == OperatingSystem.LINUX or self == OperatingSystem.MACOS


def parse_operating_system(operation_system_name: str):
    if operation_system_name.lower().startswith("win"):
        operating_system = OperatingSystem.WINDOWS
    elif operation_system_name.lower() == "linux":
        operating_system = OperatingSystem.LINUX
    elif operation_system_name.lower() == "darwin":
        operating_system = OperatingSystem.MACOS
    else:
        operating_system = OperatingSystem.OTHER
    return operating_system
