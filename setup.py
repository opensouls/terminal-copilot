from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()
  
long_description = "terminal-copilot"

setup(
        name ='terminal-copilot',
        version ='1.0.1',
        author ='Methexis',
        author_email ='joelkronander@gmail.com',
        url ='https://github.com/Methexis-Inc/terminal-copilot',
        description ='A terminal-copilot for goldfish memory programmers',
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
            "License :: OSI Approved :: Apache Software License 2.0",
            "Operating System :: MacOS :: Linux",
        ),
        keywords ='terminal copilot goldfish memory openai gpt3',
        install_requires = requirements,
        zip_safe = False
)