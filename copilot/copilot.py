# Program to serve as a terminal copilot for the user
import sys
import argparse
import subprocess
import openai
import os
from simple_term_menu import TerminalMenu


def call_openai(prompt, verbose=False):
    if verbose:
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
        best_of=5,
        n=3,
        frequency_penalty=0,
        presence_penalty=0,
    )
    # strip all whitespace from the response start or end
    responses = [c.text.strip() for c in response.choices]
    return responses

def construct_prompt(question):
    prompt = f"""
You are an AI Terminal Copilot. Your job is to help users find the right terminal command in a zsh shell.

The user is asking for the following command:
{question}

Uname-a returned the following information about the system:
{subprocess.run(["uname", "-a"], capture_output=True).stdout.decode("utf-8")}
The user is currently in the following directory:
{subprocess.run(["pwd"], capture_output=True).stdout.decode("utf-8")}
That directory contains the following files:
{subprocess.run(["ls"], capture_output=True).stdout.decode("utf-8")}
The user has the following environment variables set:
{os.environ.keys()}
The user has the following aliases set:
{subprocess.run(["alias"], capture_output=True).stdout.decode("utf-8")}

The command the user is looking for is:

"""
    return prompt

def main():
    parser = argparse.ArgumentParser(prog="copilot", description="Terminal Copilot")
    parser.add_argument(
        "command", type=str, help="Describe the command you are looking for in quotes", 
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )
    args = parser.parse_args()

    question = args.command

    if args.verbose:
        print("Verbose mode enabled")

    # run history -40 to get the last 40 commands
    # TODO to get more terminal context to work with..
    # TODO save history of previous user questions and answers

    prompt = construct_prompt(question)
    responses = call_openai(prompt, verbose=args.verbose)
    print("The command you are looking for is:")
    
    terminal_menu = TerminalMenu(responses)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {responses[menu_entry_index]}!")
    subprocess.run(["pbcopy"], input=responses[menu_entry_index], encoding="utf-8")
    print("The command has been copied to the clipboard")
    print(os.environ.keys())
    # exit with exit code 0
    sys.exit(0)
    

if __name__ == "__main__":
    main()
    cmd = response.choices[0].text.strip()
    options = [cmd]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        print(">", cmd)
        os.system(cmd)
