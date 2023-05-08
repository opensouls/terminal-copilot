import re


def strip_cmd(cmd):
    return re.sub('`[^`]*(`|$)', r'\1', cmd)


def strip_choices(choices):
    return [strip_cmd(choice.message.content) for choice in choices]

