# Terminal-copilot
Are you tired of Googling basic terminal commands every time you forget the syntax? Look no further! terminal-copilot is here to help.

With terminal-copilot, you can quickly and easily access commonly used terminal commands right from the command line. Simply type copilot followed by your question and let terminal-copilot do the rest.

For example, if you want to find a file ending in .txt, simply type:
```copilot how do I find a file ending in .txt?```
terminal-copilot will then display the correct syntax for the command you need:
```find . -name "*.txt"```
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

## Development
### Contributing
We welcome contributions to terminal-copilot! If you have an idea for a new feature or have found a bug, please open an issue. If you would like to contribute code, please open a pull request!

Thank you for considering contributing to terminal-copilot! Together, we can make it an even better tool for accessing terminal commands.

### Local Installation
1. Clone the repo
2. `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
3. `python setup.py install`

### Packaging for PyPi
1. `python setup.py sdist bdist_wheel`
2. `twine upload dist/*`