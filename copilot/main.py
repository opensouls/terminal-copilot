# Program to serve as a terminal copilot for the user
import enum
import sys
import argparse
import subprocess
import openai
import pyperclip
import os
from urllib.parse import quote
import platform
import json
import re

from copilot import history
from conversation import Conversation
from parse_os import parse_operating_system, OperatingSystem
from parse_args import parse_terminal_copilot_args
from messages_builder import Context, build_conversation


def is_unix_system():
    return platform.system().lower().startswith("lin") or platform.system().lower().startswith("dar")


if is_unix_system():
    from simple_term_menu import TerminalMenu
elif platform.system().lower().startswith("win"):
    import inquirer


def main():
    args = parse_terminal_copilot_args()

    if args.verbose:
        print("Verbose mode enabled")

    # TODO to get more terminal context to work with..
    # TODO save history of previous user questions and answers

    keys = ["HOME", "USER", "SHELL"]
    environs = ""
    for key in keys:
        if key in os.environ:
            environs += f"{key}={os.environ[key]}\n"

    operating_system = parse_operating_system(platform.system())
    if operating_system.is_unix():
        shell = os.environ.get("SHELL")
    elif operating_system == OperatingSystem.WINDOWS:
        shell = "cmd"

    current_dir = os.getcwd()
    directory_list = os.listdir()

    context = Context(
        shell=shell,
        operating_system=operating_system,
        directory=current_dir,
        directory_list=directory_list,
        history=history.get_history() if args.history and is_unix_system() else "",
        command=" ".join(args.command),
        git=git_info() if args.git else "",
        model=args.model,
    )

    conversation = build_conversation(context)

    if args.verbose:
        print("Sent this conversation to OpenAI:")
        print(conversation)

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if openai.api_key is None:
        print("To use copilot please set the OPENAI_API_KEY environment variable")
        print("You can get an API key from https://beta.openai.com/account/api-keys")
        print("To set the environment variable, run:")
        print("export OPENAI_API_KEY=<your key>")
        sys.exit(1)
    cmds = request_cmds(conversation, n=int(args.count) if args.json and args.count else 1)

    if args.json:
        print(json.dumps({
            "commands": cmds,
            "explainshell_links": list(map(get_explainshell_link, cmds))
        }))
    else:
        show_command_options(conversation, cmds[0])


def show_command_options(conversation: Conversation, cmd):
    operating_system = platform.system()

    print(f"\033[94m> {cmd}\033[0m")
    options = ["execute", "refine", "copy", "explainshell", "show more options"]

    if is_unix_system():
        terminal_menu = create_terminal_menu(options)
        menu_entry_index = terminal_menu.show()
    elif operating_system.lower().startswith("win"):
        questions = [
            inquirer.List(
                "menu_entry_index",
                message="What do you want to do?",
                choices=options,
            ),
        ]
        answers = inquirer.prompt(questions)
        menu_entry_index = options.index(answers["menu_entry_index"])

    if menu_entry_index == 0:
        execute(conversation, cmd)
    elif menu_entry_index == 1:
        refine_command(conversation, cmd)
    elif menu_entry_index == 2:
        print("> copied")
        pyperclip.copy(cmd)
    elif menu_entry_index == 3:
        link = get_explainshell_link(cmd)
        print("> explainshell: " + link)
        subprocess.run(["open", link])
    elif menu_entry_index == 4:
        show_more_cmd_options(conversation)


def create_terminal_menu(options):
    return TerminalMenu(options)


def read_input():
    return input("> ")


def refine_command(conversation: Conversation, cmd):
    refinement = read_input()
    conversation.messages.append({"role": "assistant", "content": cmd})
    refinement_command = f"""The user requires a command for the following prompt: `{refinement}`.
ONLY OUTPUT THE COMMAND. No description, no explanation, no nothing.
Do not add any text in front of it and do not add any text after it.
The command the user is looking for is: `"""
    conversation.messages.append({"role": "user", "content": refinement_command})
    cmd = request_cmds(conversation, n=1)[0]
    show_command_options(conversation, cmd)


def execute(conversation: Conversation, cmd):
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        out = result.stdout
        error = result.stderr
        print(out)
        print(error)
        if error != "" and error is not None:
            refine_failed_command(conversation, cmd, error)
        else:
            history.save(cmd)
    except Exception as e:
        print(e)
        refine_failed_command(conversation, cmd, str(e))


def refine_failed_command(conversation: Conversation, cmd, error):
    error = error[:300]
    conversation.messages.append({"role": "assistant", "content": cmd})
    failed_command = f"The last suggested command of the assistant failed with the error: `{error}`." \
                     f"The corrected command (and only the command) is:`"
    conversation.messages.append({"role": "user", "content": failed_command})
    cmd = request_cmds(conversation, n=1)[0]
    print("The last command failed. Here is suggested corrected command:")
    show_command_options(conversation, cmd)


def show_more_cmd_options(conversation: Conversation):
    operating_system = platform.system()

    cmds = request_cmds(conversation, n=5)
    print("Here are more options:")
    options = [repr(cmd) for cmd in cmds]

    if is_unix_system():
        cmd_terminal_menu = create_terminal_menu(options)
        cmd_menu_entry_index = cmd_terminal_menu.show()
    elif operating_system.lower().startswith("win"):
        questions = [
            inquirer.List(
                "cmd_menu_entry_index",
                message="Which command do you want to execute?",
                choices=options,
            ),
        ]
        answers = inquirer.prompt(questions)
        cmd_menu_entry_index = options.index(answers["cmd_menu_entry_index"])

    if cmd_menu_entry_index is not None:
        show_command_options(conversation, cmds[cmd_menu_entry_index])


def request_cmds(conversation: Conversation, n=1):
    response = openai.ChatCompletion.create(
        model=conversation.model.value,
        messages=conversation.messages,
        temperature=0,
        max_tokens=1000,
        top_p=0.2,
        stop=["`"],
        frequency_penalty=0,
        presence_penalty=0,
        n=n,
    )
    choices = response.choices
    cmds = strip(choices)
    if len(cmds) > 1:
        cmds = list(dict.fromkeys(cmds))
    return cmds


def get_explainshell_link(cmd):
    return "https://explainshell.com/explain?cmd=" + quote(cmd)


def strip(choices):
    return [re.sub('`[^`]*(`|$)', r'\1', choice.message.content) for choice in choices]


def git_info():
    git_installed = (
            subprocess.run(["which", "git"], capture_output=True).returncode == 0
    )
    if os.path.exists(".git") and git_installed:
        return f"""
User is in a git repo.
Branches are:
{subprocess.run(["git", "branch"], capture_output=True).stdout.decode("utf-8")}
Last 3 git history entries:
{subprocess.run(["git", "log", "-n3", "--oneline"], capture_output=True).stdout.decode("utf-8")}
Short git status:
{subprocess.run(["git", "status", "-s"], capture_output=True).stdout.decode("utf-8")}
"""
    else:
        return ""


if __name__ == "__main__":
    main()
