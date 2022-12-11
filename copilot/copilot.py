# Program to serve as a terminal copilot for the user
import sys
import argparse
import subprocess
import openai
import os
from simple_term_menu import TerminalMenu


def main():
    parser = argparse.ArgumentParser(prog='copilot', description='Terminal Copilot')
    parser.add_argument('command', type=str, nargs='+',
                        help='Describe the command you are looking for.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled")

    # run history -40 to get the last 40 commands
    # TODO to get more terminal context to work with..
    # TODO save history of previous user questions and answers

    prompt = f"""
You are an AI Terminal Copilot. Your job is to help users find the right terminal command in a zsh shell on mac os.

The user is asking for the following command:
{" ".join(args.command)}

The user is currently in the following directory:
{subprocess.run(["pwd"], capture_output=True).stdout.decode("utf-8")}
That directory contains the following files:
{subprocess.run(["ls"], capture_output=True).stdout.decode("utf-8")}
The user has the following environment variables set:
HOME={os.environ["HOME"]}
USER={os.environ["USER"]}
SHELL={os.environ["SHELL"]}
COMMAND_MODE={os.environ["COMMAND_MODE"]}

The user has the following aliases set:
{subprocess.run(["alias"], capture_output=True).stdout.decode("utf-8")}

The command the user is looking for is:

"""

    if args.verbose:
        print("Sent this prompt to OpenAI:")
        print(prompt)

    # Call openai api to get the command completion
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if openai.api_key is None:
        print("Please set OPENAI_API_KEY environment variable")
        print("You can get an API key from https://beta.openai.com/account/api-keys")
        print("To set the environment variable, run:")
        print("export OPENAI_API_KEY = <your key>")
        sys.exit(1)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # strip all whitespace from the response start or end
    cmd = response.choices[0].text.strip()
    print(f"\033[94m> {cmd}\033[0m")
    options = ["execute", "copy"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        os.system(cmd)
    elif menu_entry_index == 1:
        print("> copied")
        subprocess.run(["pbcopy"], input=cmd, encoding="utf-8")