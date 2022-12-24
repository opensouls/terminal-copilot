import os
from time import time
import platform


def _fish_history_file_location():
    possible_paths = [
        os.path.join(os.environ["HOME"], ".local/share/fish/fish_history"),
        os.path.join(os.environ["HOME"], ".config/fish/fish_history"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def fish_history_file_lines():
    history_file = _fish_history_file_location()
    if history_file is None:
        return []
    with open(history_file, "r") as history:
        lines = history.readlines()
        return lines


def _zsh_history_file_location():
    possible_paths = [
        os.path.join(os.environ["HOME"], ".zsh_history"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def zsh_history_file_lines():
    history_file = _zsh_history_file_location()
    if history_file is None:
        return []
    with open(history_file, 'rb') as history:
        lines = history.read().decode(errors='replace').splitlines()
        return lines


def bash_history_file_lines():
    history_file = _bash_history_file_location()
    if history_file is None:
        return []
    with open(history_file, "r") as history:
        lines = history.readlines()
        return lines


def _bash_history_file_location():
    possible_paths = [
        os.path.join(os.environ["HOME"], ".bash_history"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def _get_fish_history_line(command_script):
    return "- cmd: {}\n  when: {}\n".format(command_script, int(time()))


def _get_zsh_history_line(command_script):
    return "{}\n".format(command_script)


def _get_bash_history_line(command_script):
    return "{}\n".format(command_script)


def save(cmd):
    if platform.system().lower().startswith("win"):
        return
    if os.environ["SHELL"].endswith("fish"):
        formatted_line = _get_fish_history_line(cmd)
        history_file = _fish_history_file_location()
        _append_line(formatted_line, history_file)
    elif os.environ["SHELL"].endswith("zsh"):
        formatted_line = cmd
        history_file = _zsh_history_file_location()
        _append_line(formatted_line, history_file)
    elif os.environ["SHELL"].endswith("bash"):
        formatted_line = cmd
        history_file = _bash_history_file_location()
        _append_line(formatted_line, history_file)


def _append_line(formatted_line, history_file):
    if history_file and os.path.isfile(history_file):
        with open(history_file, "a") as history:
            history.write(formatted_line)
