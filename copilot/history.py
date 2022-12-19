import os
import platform

from copilot import history_file


def _is_command(line):
    return line.startswith("- cmd: ")


def _formatted(command):
    return command.replace("- cmd: ", "").strip()[:100]


def _fish_history(n):
    lines = history_file.fish_history_file_lines()
    if len(lines) == 0:
        return ""
    commands = [_formatted(command) for command in lines if _is_command(command)]
    commands = list(dict.fromkeys(commands))
    most_recent_commands = "\n".join(commands[-n:])
    history = f"""
The user has recently run these last {min(len(lines), n)} commands:
{most_recent_commands}
    """
    return history


def _zsh_history(n):
    lines = history_file.zsh_history_file_lines()
    if len(lines) == 0:
        return ""
    commands = [command.strip() for command in lines if command != ""]
    commands = list(dict.fromkeys(commands))
    most_recent_commands = "\n".join(commands[-n:])
    history = f"""
The user has recently run these last {min(len(lines), n)} commands:
{most_recent_commands}
    """
    return history


def get_history(history_context_size=40):
    if os.environ["SHELL"].endswith("fish"):
        return _fish_history(history_context_size)
    if os.environ["SHELL"].endswith("zsh"):
        return _zsh_history(history_context_size)
    else:
        return ""


def save(cmd):
    if platform.system().lower().startswith("win"):
        return
    
    if os.environ["SHELL"].endswith("fish"):
        history_file.save(cmd)
