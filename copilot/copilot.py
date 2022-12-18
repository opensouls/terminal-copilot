# Program to serve as a terminal copilot for the user
import sys
import argparse
import subprocess
import openai
import pyperclip
import os
from urllib.parse import quote
from simple_term_menu import TerminalMenu
import platform

import history

def main():
    parser = argparse.ArgumentParser(prog='copilot', description='Terminal Copilot')
    parser.add_argument('command', type=str, nargs='+',
                        help='Describe the command you are looking for.')
    parser.add_argument('-a', '--with-aliases', action='store_true',
                        help='include aliases in the prompt')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')

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

    shell = os.environ["SHELL"]
    operating_system = platform.system()

    prompt = f"""
You are an AI Terminal Copilot. Your job is to help users find the right terminal command in a {shell} on {operating_system}.

The user is asking for the following command:
'{" ".join(args.command)}'

The user is currently in the following directory:
{subprocess.run(["pwd"], capture_output=True).stdout.decode("utf-8")}
That directory contains the following files:
{subprocess.run(["ls"], capture_output=True).stdout.decode("utf-8")}
{history.get_history()}
The user has several environment variables set, some of which are:
{environs}
"""
    if args.with_aliases:
        prompt += f"""
The user has the following aliases set:
{subprocess.run(["alias"], capture_output=True, shell=True).stdout.decode("utf-8")}
"""
    prompt += """

The command the user is looking for is:
`
"""

    if args.verbose:
        print("Sent this prompt to OpenAI:")
        print(prompt)

    # Call openai api to get the command completion
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if openai.api_key is None:
        print("To use copilot please set the OPENAI_API_KEY environment variable")
        print("You can get an API key from https://beta.openai.com/account/api-keys")
        print("To set the environment variable, run:")
        print("export OPENAI_API_KEY=<your key>")
        sys.exit(1)
    cmd = request_cmds(prompt, n=1)[0]
    show_command_options(prompt, cmd)

def show_command_options(prompt, cmd):
    print(f"\033[94m> {cmd}\033[0m")
    options = ["execute", "copy", "explainshell", "show more options"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        os.system(cmd)
    elif menu_entry_index == 1:
        print("> copied")
        pyperclip.copy(cmd)
    elif menu_entry_index == 2:
        link = "https://explainshell.com/explain?cmd=" + quote(cmd)
        print("> explainshell: " + link)
        subprocess.run(["open", "https://explainshell.com/explain?cmd=" + quote(cmd)])
    elif menu_entry_index == 3:
        show_more_cmd_options(prompt)

def show_more_cmd_options(prompt):
    cmds = request_cmds(prompt, n=5)
    print("Here are more options:")
    options = [repr(cmd) for cmd in cmds]
    cmd_terminal_menu = TerminalMenu(options)
    cmd_menu_entry_index = cmd_terminal_menu.show()
    if cmd_menu_entry_index is not None:
        show_command_options(prompt, cmds[cmd_menu_entry_index])


def request_cmds(prompt, n=1):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        stop=["`"],
        frequency_penalty=0,
        presence_penalty=0,
        n=n,
    )
    choices = response.choices
    cmds = strip_all_whitespaces_from(choices)
    if len(cmds) > 1:
        cmds = list(dict.fromkeys(cmds))
    return cmds


def strip_all_whitespaces_from(choices):
    return [choice.text.strip() for choice in choices]


if __name__ == "__main__":
    main()
