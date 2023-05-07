import unittest

from copilot.context import Context
from copilot.conversation import Model
from copilot.messages_builder import system_messages, system_prompt_message
from copilot.parse_os import OperatingSystem
from copilot.sample_conversations import unix_fish_sample_conversations, unix_bourne_sample_conversations, \
    windows_cmd_sample_conversations


class TestSystemMessages(unittest.TestCase):

    def _create_context(self, os, shell):
        return Context(
            shell=shell,
            operating_system=os,
            directory="path/to/directory",
            directory_list=["dir1", "dir2"],
            history="command history",
            command="test command",
            git="git status",
            model=Model.GPT_35_TURBO,
        )

    def test_system_messages_unix_fish(self):
        # arrange
        context = self._create_context(OperatingSystem.MACOS, "path/to/fish")
        # act
        result = system_messages(context)
        # assert
        for message in unix_fish_sample_conversations():
            self.assertIn(message, result)

    def test_system_messages_unix_bourne(self):
        # arrange
        context = self._create_context(OperatingSystem.LINUX, "path/to/bash")

        # act
        result = system_messages(context)

        # assert
        for message in unix_bourne_sample_conversations():
            self.assertIn(message, result)

    def test_system_messages_windows(self):
        # arrange
        context = self._create_context(OperatingSystem.WINDOWS, "path/to/cmd")
        # act
        result = system_messages(context)
        # assert
        for message in windows_cmd_sample_conversations():
            self.assertIn(message, result)

    def test_contains_system_prompt_message(self):
        # arrange
        context = self._create_context(OperatingSystem.WINDOWS, "path/to/cmd")
        # act
        result = system_messages(context)
        # assert
        self.assertIn(system_prompt_message(context), result)


if __name__ == '__main__':
    unittest.main()
