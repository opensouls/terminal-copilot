import os


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
    with open(history_file, 'r') as history:
        lines = history.readlines()
        return lines
