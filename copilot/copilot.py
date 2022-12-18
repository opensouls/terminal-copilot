# Program to serve as a terminal copilot for the user
import sys
import argparse
import subprocess
import openai
import pyperclip
import os
from urllib.parse import quote
import platform

if platform.system().lower().startswith("lin") or platform.system().lower().startswith("dar"):
    from simple_term_menu import TerminalMenu
elif platform.system().lower().startswith("win"):
    from inquirer import prompt, List


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

    # run history -40 to get the last 40 commands
    # TODO to get more terminal context to work with..
    # TODO save history of previous user questions and answers

    keys = ["HOME", "USER", "SHELL"]
    environs = ""
    for key in keys:
        if key in os.environ:
            environs += f"{key}={os.environ[key]}\n"

    operating_system = platform.system()
    if operating_system.lower().startswith("lin") or operating_system.lower().startswith("dar"):
        shell = os.environ.get("SHELL")
    elif operating_system.lower().startswith("win"):
        shell = "cmd"

    # get the current directory
    current_dir = os.getcwd()

    # list the files in the current directory
    directory_list = os.listdir()
    
    prompt = f"""
You are an AI Terminal Copilot. Your job is to help users find the right terminal command in a {shell} on {operating_system}.

The user is asking for the following command:
'{" ".join(args.command)}'

The user is currently in the following directory:
{current_dir}
That directory contains the following files:
{directory_list}
The user has several environment variables set, some of which are:
{environs}
"""
    if args.with_aliases and operating_system.lower().startswith("lin") or operating_system.lower().startswith("dar"):
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
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        stop=["`"],
        frequency_penalty=0,
        presence_penalty=0
    )
    # strip all whitespace from the response start or end
    cmd = response.choices[0].text.strip()
    print(f"\033[94m> {cmd}\033[0m")
    
    options = ["execute", "copy", "explainshell"]
    if operating_system.lower().startswith("lin") or operating_system.lower().startswith("dar"):
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
    elif operating_system.lower().startswith("win"):
        questions = [
            List('action',
                message="Choose",
                choices=options,
            ),
        ]
        answer = prompt(questions)
        menu_entry_index = options.index(answer["action"])
    
    if menu_entry_index == 0:
        os.system(cmd)
    elif menu_entry_index == 1:
        print("> copied")
        pyperclip.copy(cmd)
    elif menu_entry_index == 2:
        link = "https://explainshell.com/explain?cmd=" + quote(cmd)
        print("> explainshell: " + link)
        subprocess.run(["open", "https://explainshell.com/explain?cmd=" + quote(cmd)])
