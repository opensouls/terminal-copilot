[![PyPI version](https://badge.fury.io/py/terminal-copilot.svg)](https://badge.fury.io/py/terminal-copilot)

# Terminal-copilot
Are you tired of Googling basic terminal commands every time you forget the syntax?  
Look no further! terminal-copilot is here to help.

With terminal-copilot, you can quickly and easily access commonly used terminal commands right from the command line. Simply type copilot followed by your desired command in natural language and let terminal-copilot do the rest.

For example, if you want to find a file ending in .txt, simply type:
```copilot find a file ending in .txt```
terminal-copilot will then display the correct syntax for the command you need:
```find . -name "*.txt"```
With options to execute, copy, or explain the proposed terminal command.

### Installation
To use terminal-copilot, you must first install it on your system. The easiest way to do this is using pip:
```pip install terminal-copilot```
Once terminal-copilot is installed, you can access it from the command line by typing copilot followed by your question.
### Example Usage
terminal-copilot is designed to be simple and intuitive to use. Simply type copilot followed by your question and terminal-copilot will display the correct syntax for the command you need.

Here are some examples of how you can use terminal-copilot:

1. `copilot list the compute instances in gcloud`
2. `copilot find all mp3 files in my home directory`
3. `copilot install the openai package for python`
4. `copilot clean up my docker images`


### Arguments
Terminal-copilot can be called with optional command line arguments:

- `-a`, `--alias`: Enables the inclusion of aliases in the prompt sent to the OpenAI API. May potentially send sensitive information to OpenAI.
- `-v`, `--verbose`: Increases output verbosity of the tool.
- `-g`, `--git`: This flag enables the inclusion of Git context in the prompt sent to the OpenAI API. This can be useful for users working with Git repositories and may include the current branch name, repository status, recent commit messages, and file history.
- `-hist`, `--history`: Enables the inclusion of terminal history in the prompt sent to the OpenAI API. May potentially send sensitive information to OpenAI and increase the number of tokens used.

### Requirements
Python 3.7+ 

### Sensitive Information
Please note that terminal-copilot has the ability to send sensitive information to OpenAI as part of the prompt used to generate terminal commands. This includes the `--alias`,`--history`, `--git` command line arguments, which may include sensitive information such as aliases and terminal history. If you are concerned about the potential for sensitive information to be sent to OpenAI, we recommend not using these flags. We recommend that users exercise caution when using these optional features and consider the potential risks before enabling them.

## Development
### Contributing
We welcome contributions to terminal-copilot! If you have an idea for a new feature or have found a bug, please open an issue. If you would like to contribute code, please open a pull request!

Thank you for considering contributing to terminal-copilot! Together, we can make it an even better tool for accessing terminal commands.

### Local Installation
1. Clone the repo
2. `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
3. `python setup.py install`

### Packaging for PyPi
1. `python setup.py sdist bdist_wheel`
2. `twine upload dist/*`

