from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()
  
long_description = """
Are you tired of Googling basic terminal commands every time you forget the syntax? Look no further! terminal-copilot is here to help.

With terminal-copilot, you can quickly and easily access commonly used terminal commands right from the command line. Simply type copilot followed by your question and let terminal-copilot do the rest.

For example, if you want to find a file ending in .txt, simply type:
```copilot find a file ending in .txt```
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
"""

setup(
        name ='terminal-copilot',
        version ='1.0.9',
        author ='Methexis',
        author_email ='joelkronander@gmail.com',
        url ='https://github.com/Methexis-Inc/terminal-copilot',
        description ='A smart terminal assistant that helps you find the right command',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='Apache License 2.0',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'copilot=copilot.copilot:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
        ),
        keywords ='terminal copilot openai gpt3',
        install_requires = requirements,
        zip_safe = False
)