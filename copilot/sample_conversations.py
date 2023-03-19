def unix_sample_conversations():
    return [
        {"role": "system", "name": "example_user", "content": "list files in directory"},
        {"role": "system", "name": "example_assistant", "content": "ls -la"},
        {"role": "system", "name": "example_user", "content": "list all branches"},
        {"role": "system", "name": "example_assistant", "content": "git branch -a"},
        {"role": "system", "name": "example_user", "content": "find all txt and wav files in the home directory"},
        {"role": "system", "name": "example_assistant", "content": "find . -name \"*.txt\" -o -name \"*.wav\""},
        {"role": "system", "name": "example_user", "content": "I meant mp4 files not wav files"},
        {"role": "system", "name": "example_assistant", "content": "find . -name \"*.txt\" -o -name \"*.mp4\""},
        {"role": "system", "name": "example_user", "content": "google GPT and write the results into Excel"},
        {"role": "system", "name": "example_assistant", "content": "Command not found"},
    ]


def unix_bourne_sample_conversations():
    shared_conversations = unix_sample_conversations()
    specific_conversations = [
        {"role": "system", "name": "example_user", "content": "update Copyright [yyyy] [name of copyright owner]"},
        {"role": "system", "name": "example_assistant",
         "content": """sed -i '' 's/\[yyyy\] \[name of copyright owner\]/2023 Copilot/g'"""},
        {"role": "system", "name": "example_user",
         "content": """sed: -I or -i may not be used with stdin"""},
        {"role": "system", "name": "example_assistant",
         "content": """sed -i '' 's/\[yyyy\] \[name of copyright owner\]/2023 Copilot/g' LICENSE"""},
        {"role": "system", "name": "example_user", "content": "output in a loop all numbers from 1 to 5"},
        {"role": "system", "name": "example_assistant", "content": "for i in {1..5}; do echo $i; done"},
    ]

    return shared_conversations + specific_conversations


def unix_fish_sample_conversations():
    shared_conversations = unix_sample_conversations()
    specific_conversations = [
        {"role": "system", "name": "example_user", "content": "update Copyright [yyyy] [name of copyright owner]"},
        {"role": "system", "name": "example_assistant",
         "content": "sed -i '' 's/\[yyyy\] \[name of copyright owner\]/2023 Copilot/g'"},
        {"role": "system", "name": "example_user",
         "content": """sed: -I or -i may not be used with stdin"""},
        {"role": "system", "name": "example_assistant",
         "content": "sed -i '' 's/\[yyyy\] \[name of copyright owner\]/2023 Copilot/g' LICENSE"},
        {"role": "system", "name": "example_user", "content": "set and export an environment variable in Fish shell"},
        {"role": "system", "name": "example_assistant", "content": "set -gx MY_VARIABLE \"example_value\""},
        {"role": "system", "name": "example_user", "content": "output in a loop all numbers from 1 to 5"},
        {"role": "system", "name": "example_assistant", "content": "for i in (seq 1 5); echo $i; end"},
    ]

    return shared_conversations + specific_conversations


def windows_cmd_sample_conversations():
    return [
        {"role": "system", "name": "example_user", "content": "list files in directory"},
        {"role": "system", "name": "example_assistant", "content": "dir"},
        {"role": "system", "name": "example_user", "content": "list all branches"},
        {"role": "system", "name": "example_assistant", "content": "git branch -a"},
        {"role": "system", "name": "example_user", "content": "find all txt and wav files in the current directory"},
        {"role": "system", "name": "example_assistant", "content": "dir /b /s *.txt *.wav"},
        {"role": "system", "name": "example_user", "content": "I meant mp4 files not wav files"},
        {"role": "system", "name": "example_assistant", "content": "dir /b /s *.txt *.mp4"},
        {"role": "system", "name": "example_user", "content": "google GPT and write the results into Excel"},
        {"role": "system", "name": "example_assistant", "content": "Command not found"},
        {"role": "system", "name": "example_user", "content": "update Copyright [yyyy] [name of copyright owner]"},
        {"role": "system", "name": "example_assistant", "content": "Command not found"},
        {"role": "system", "name": "example_user", "content": "FILENAME: No such file or directory"},
        {"role": "system", "name": "example_assistant", "content": "Command not found"}
    ]
