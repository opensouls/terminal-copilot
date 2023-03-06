# Program to serve as a terminal copilot for the user
import sys
import argparse
import subprocess
import openai
import pyperclip
import os
from urllib.parse import quote
import platform
import json

from copilot import history
from messages_builder import Context, build_messages


def is_unix_system():
    return platform.system().lower().startswith("lin") or platform.system().lower().startswith("dar")


if is_unix_system():
    from simple_term_menu import TerminalMenu
elif platform.system().lower().startswith("win"):
    import inquirer


def main():
    parser = argparse.ArgumentParser(prog="copilot", description="Terminal Copilot")
    parser.add_argument(
        "command", type=str, nargs="+", help="Describe the command you are looking for."
    )
    parser.add_argument(
        "-a",
        "--alias",
        action="store_true",
        help="Include aliases in the prompt. Note: This feature may potentially send sensitive information to OpenAI.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )
    parser.add_argument(
        "-g", "--git", action="store_true", help="Include git info if available"
    )
    parser.add_argument(
        "-hist",
        "--history",
        action="store_true",
        help="Include terminal history in the prompt. Note: This feature may potentially send sensitive information to OpenAI and increase the number of tokens used.",
    )
    parser.add_argument(
        "-j", "--json", action="store_true", help="Output data as JSON instead of using an interactive prompt."
    )
    parser.add_argument(
        "-c", "--count", help="The number of commands to output when JSON output is specified."
    )

    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled")

    # TODO to get more terminal context to work with..
    # TODO save history of previous user questions and answers

    keys = ["HOME", "USER", "SHELL"]
    environs = ""
    for key in keys:
        if key in os.environ:
            environs += f"{key}={os.environ[key]}\n"

    operating_system = platform.system()
    if is_unix_system():
        shell = os.environ.get("SHELL")
    elif operating_system.lower().startswith("win"):
        shell = "cmd"

    # get the current directory
    current_dir = os.getcwd()

    # list the files in the current directory
    directory_list = os.listdir()

    context = Context(
        shell=shell,
        operating_system=operating_system,
        directory=current_dir,
        directory_list=directory_list,
        history=history.get_history() if args.history and is_unix_system() else "",
        command=" ".join(args.command),
        git=git_info() if args.git else "",
    )

    messages = build_messages(context)

    if args.verbose:
        print("Sent this messages to OpenAI:")
        print(messages)

    # Call openai api to get the command completion
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if openai.api_key is None:
        print("To use copilot please set the OPENAI_API_KEY environment variable")
        print("You can get an API key from https://beta.openai.com/account/api-keys")
        print("To set the environment variable, run:")
        print("export OPENAI_API_KEY=<your key>")
        sys.exit(1)
    cmds = request_cmds(messages, n=int(args.count) if args.json and args.count else 1)

    if args.json:
        print(json.dumps({
            "commands": cmds,
            "explainshell_links": list(map(get_explainshell_link, cmds))
        }))
    else:
        show_command_options(messages, cmds[0])


def show_command_options(messages, cmd):
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
        execute(messages, cmd)
    elif menu_entry_index == 1:
        refine_command(messages, cmd)
    elif menu_entry_index == 2:
        print("> copied")
        pyperclip.copy(cmd)
    elif menu_entry_index == 3:
        link = get_explainshell_link(cmd)
        print("> explainshell: " + link)
        subprocess.run(["open", link])
    elif menu_entry_index == 4:
        show_more_cmd_options(messages)


def create_terminal_menu(options):
    return TerminalMenu(options)


def read_input():
    return input("> ")


def refine_command(messages, cmd):
    refinement = read_input()
    messages.append({"role": "assistant", "content": cmd})
    refinement_command = f"""The user requires a command for the following prompt: `{refinement}`.
ONLY OUTPUT THE COMMAND. No description, no explanation, no nothing.
Do not add any text in front of it and do not add any text after it.
The command the user is looking for is: `"""
    messages.append({"role": "user", "content": refinement_command})
    cmd = request_cmds(messages, n=1)[0]
    show_command_options(messages, cmd)

def execute(messages, cmd):
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        out = result.stdout
        error = result.stderr
        print(out)
        print(error)
        if error != "" and error is not None:
            refine_failed_command(messages, cmd, error)
    except Exception as e:
        print(e)
        refine_failed_command(messages, cmd, str(e))


def refine_failed_command(messages, cmd, error):
    messages.append({"role": "assistant", "content": cmd})
    failed_command = f"The last suggested command of the assistant failed with the error: `{error}`." \
                     f"The corrected command (and only the command) is:`"
    messages.append({"role": "user", "content": failed_command})
    cmd = request_cmds(messages, n=1)[0]
    print("The last command failed. Here is suggested corrected command:")
    show_command_options(messages, cmd)


def show_more_cmd_options(messages):
    operating_system = platform.system()

    cmds = request_cmds(messages, n=5)
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
        show_command_options(messages, cmds[cmd_menu_entry_index])


def request_cmds(messages, n=1):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
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

import re


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
