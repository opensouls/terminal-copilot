from copilot.context import Context
from copilot.conversation import Conversation
from copilot.sample_conversations import unix_fish_sample_conversations
from copilot.sample_conversations import (
    unix_bourne_sample_conversations,
    windows_cmd_sample_conversations,
)
from typing import Optional


def user_message(context: Context):
    return f"""
The user requires a command for the following prompt: `{context.command}`
The command the user is looking for is:`"""


def system_prompt(context: Context):
    return f"""
The user is currently in the directory {context.directory}
That directory contains the following files and directories: {context.directory_list}
{context.history}
{context.git}
###
You are a Terminal AI Copilot whose codename is Sky.
Sky's job is it to help users find the right terminal command in a {context.shell} shell on a {context.operating_system.value}
If Sky does not know the command, it will only output the keywords 'Command not found' in the terminal.

Sky output will be inserted directly into the terminal and it has to be able to run in the {context.shell} shell
Sky can correct the a suggested command that returns an error. Sky will suggest a command that fixes the error.
The user can refine the command in multiple following messages. Sky also here will only answer with the updated command.
Sky will always only output one command behind ` and mark the end of the command with a `
Format: The command the user is looking for is:`<sky enters command here>`

Sky is helpful, polite, and has an IQ of 300.
"""


def user_message(context: Context):
    return f"""The user requires a command for the following prompt: `{context.command}`
The command (or 'Command not found') the user is looking for is:`"""


def system_prompt_message(context):
    return {"role": "system", "content": system_prompt(context)}


def sample_conversations(context: Context) -> list:
    if context.operating_system.is_unix():
        return unix_sample_conversations(context)
    else:
        return windows_cmd_sample_conversations()


def unix_sample_conversations(context: Context) -> list:
    if context.shell.endswith("fish"):
        return unix_fish_sample_conversations()
    else:
        return unix_bourne_sample_conversations()


def system_messages(context: Context) -> list:
    messages = [system_prompt_message(context)]
    messages.extend(sample_conversations(context))
    return messages


def build_conversation(
    context: Context, usermessage: Optional[str] = None
) -> Conversation:
    messages = []
    messages.extend(system_messages(context))
    if not usermessage:
        usermessage = user_message(context)
    messages.append({"role": "user", "content": usermessage})
    return Conversation(messages=messages, model=context.model)
