import os


def is_fish():
    return os.environ["SHELL"].endswith("fish")


def is_zsh():
    return os.environ["SHELL"].endswith("zsh")


def is_bash():
    return os.environ["SHELL"].endswith("bash")
