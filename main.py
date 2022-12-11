# Program to serve as a terminal copilot for the user
import sys
import argparse
import os
import subprocess
import openai
import os


def main(argv):
    parser = argparse.ArgumentParser(description='Terminal Copilot')
    parser.add_argument('command', type=str, nargs='+',
                        help='Describe the command you are looking for.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')  
    args = parser.parse_args(args=argv)
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
{os.environ.keys()}
The user has the following aliases set:
{subprocess.run(["alias"], capture_output=True).stdout.decode("utf-8")}

The command the user is looking for is:

"""

    if args.verbose:
        print("Sent this prompt to OpenAI:")
        print(prompt)

    # Call openai api to get the command completion
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if  openai.api_key is None:
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
    print(response.choices[0].text)

if __name__ == "__main__":
    main(sys.argv[1:])