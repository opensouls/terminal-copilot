import os

from copilot import history_file


def _is_command(line):
    return line.startswith("- cmd: ")


def _formatted(command):
    return command.replace("- cmd: ", "").strip()[:100]


def _fish_commands():
    lines = history_file.fish_history_file_lines()
    commands = [_formatted(command) for command in lines if _is_command(command)]
    return commands


def _zsh_commands():
    lines = history_file.zsh_history_file_lines()
    commands = [command.strip() for command in lines if command != ""]
    return commands


def _bash_commands():
    lines = history_file.bash_history_file_lines()
    commands = [command.strip() for command in lines if command != ""]
    return commands


def history_prompt_for(commands, n):
    if len(commands) == 0:
        return ""
    commands = list(dict.fromkeys(commands))
    most_recent_commands = "\n".join(commands[-n:])
    history = f"""
The user has recently run these last {min(len(commands), n)} commands:
{most_recent_commands}
    """
    return history


def get_history(n=40):
    if os.environ["SHELL"].endswith("fish"):
        return history_prompt_for(_fish_commands(), n)
    if os.environ["SHELL"].endswith("zsh"):
        return history_prompt_for(_zsh_commands(), n)
    if os.environ["SHELL"].endswith("bash"):
        return history_prompt_for(_bash_commands(), n)
    else:
        return ""


def save(cmd):
    history_file.save(cmd)
