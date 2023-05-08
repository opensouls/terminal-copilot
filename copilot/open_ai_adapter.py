import sys

import openai

from conversation import Conversation
from strip import strip_cmd, strip_choices


def _create_chat_completion(conversation, n, stream=False):
    return openai.ChatCompletion.create(
        model=conversation.model.value,
        messages=conversation.messages,
        temperature=0,
        max_tokens=1000,
        top_p=0.2,
        stop=["`"],
        frequency_penalty=0,
        presence_penalty=0,
        n=n,
        stream=stream,
    )


def request_cmds(conversation: Conversation, n=1):
    response = _create_chat_completion(conversation, n)
    choices = response.choices
    cmds = strip_choices(choices)
    if len(cmds) > 1:
        cmds = list(dict.fromkeys(cmds))
    return cmds


def stream_cmd_into_terminal(conversation: Conversation) -> str:
    response = _create_chat_completion(conversation, n=1, stream=True)
    print(f"\033[94m> ", end='')
    cmd = ""
    for chunk in response:
        if "content" in chunk["choices"][0]["delta"]:
            cmd_delta = chunk["choices"][0]["delta"]["content"]
            cmd_delta = strip_cmd(cmd_delta)
            print(cmd_delta, end='')
            sys.stdout.flush()
            cmd += cmd_delta
    print("\033[0m")
    return strip_cmd(cmd)
