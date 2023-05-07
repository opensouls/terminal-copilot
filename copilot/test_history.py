import os

from unittest.mock import patch
import unittest

from history import get_history


class TestHistory(unittest.TestCase):
    def test_get_history_add_fish_user_history_context(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/fish"
        # act
        with patch('copilot.history_file.fish_history_file_lines') as mock_fish_history_file_lines:
            mock_fish_history_file_lines.return_value = [
                "- cmd: ls\n",
                "- cmd: cd /home/username\n",
            ]
            history = get_history()
        # assert
        self.assertTrue("The user has recently run these last 2 commands:" in history)

    def test_get_history_adds_zsh_user_history_context(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/zsh"
        # act
        with patch('copilot.history_file.zsh_history_file_lines') as mock_zsh_history_file_lines:
            mock_zsh_history_file_lines.return_value = [
                ": 1611234567:0;ls",
                ": 1611234568:0;cd /home/username",
            ]
            history = get_history()
        # assert
        self.assertTrue("The user has recently run these last 2 commands:" in history)

    def test_get_history_limits_the_history_length_to_history_context_size(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/fish"
        # act
        with patch('copilot.history_file.fish_history_file_lines') as mock_fish_history_file_lines:
            mock_fish_history_file_lines.return_value = [
                "- cmd: ls\n",
                "  when: 1664698037\n",
                "- cmd: cd /home/username\n",
                "  paths:\n",
                "  - /home/username\n",
            ]
            history = get_history(1)
        # assert
        self.assertTrue("The user has recently run these last 1 commands:" in history)
        self.assertFalse("ls" in history)

    def test_get_history_returns_empty_string_if_no_history_file_exists_or_empty(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/fish"
        # act
        with patch('copilot.history_file.fish_history_file_lines') as mock_fish_history_file_lines:
            mock_fish_history_file_lines.return_value = []
            history = get_history()
        # assert
        self.assertEqual(history, "")

    def test_get_history_returns_history_if_alternative_fish_location(self):
        # arrange
        os.environ["SHELL"] = "/other/fish"
        # act
        with patch('copilot.history_file.fish_history_file_lines') as mock_fish_history_file_lines:
            mock_fish_history_file_lines.return_value = [
                "- cmd: ls\n",
            ]
            history = get_history()
        # assert
        self.assertTrue("ls" in history)

    def test_get_history_returns_empty_string_if_shell_is_not_set(self):
        # arrange
        os.environ["SHELL"] = ""
        # act
        with patch('copilot.history_file.fish_history_file_lines') as mock_fish_history_file_lines:
            mock_fish_history_file_lines.return_value = [
                "- cmd: ls\n",
                "- cmd: cd /home/username\n",
            ]
            history = get_history()
        # assert
        self.assertEqual(history, "")

    def test_get_history_strips_cmd_prefix_from_commands(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/fish"
        # act
        with patch('copilot.history_file.fish_history_file_lines') as mock_fish_history_file_lines:
            mock_fish_history_file_lines.return_value = [
                "- cmd: ls\n",
            ]
            history = get_history()
        # assert
        self.assertTrue("ls" in history)
        self.assertFalse("- cmd:" in history)

    def test_get_history_only_appends_commands(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/fish"
        # act
        with patch('copilot.history_file.fish_history_file_lines') as mock_fish_history_file_lines:
            mock_fish_history_file_lines.return_value = [
                "- cmd: ls\n",
                "  when: 1611234567\n",
            ]
            history = get_history()
        # assert
        self.assertTrue("ls" in history)
        self.assertFalse("when:" in history)
        self.assertFalse("1611234567" in history)

    def test_get_history_only_limits_the_max_command_length_for_context_to_100(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/fish"
        short_command = "ls -l /short/command"
        long_command = "ls -l /home/username/very/long/path/that/should/be/truncated/and/this/should/be/truncated/too/this/sh"  # 101 characters
        # act
        with patch('copilot.history_file.fish_history_file_lines') as mock_fish_history_file_lines:
            mock_fish_history_file_lines.return_value = [
                f"- cmd: {long_command}",
                f"- cmd: {short_command}",
            ]
            history = get_history()
        # assert
        self.assertTrue(short_command in history)
        self.assertFalse(long_command in history)

    def test_get_history_returns_empty_string_fish_history_file_is_empty(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/fish"
        # act
        with patch('copilot.history_file.fish_history_file_lines') as mock_fish_history_file_lines:
            mock_fish_history_file_lines.return_value = []
            history = get_history()
        # assert
        self.assertEqual(history, "")

    def test_get_history_returns_empty_string_if_zsh_history_file_is_empty(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/zsh"
        # act
        with patch('copilot.history_file.zsh_history_file_lines') as mock_zsh_history_file_lines:
            mock_zsh_history_file_lines.return_value = []
            history = get_history()
        # assert
        self.assertEqual(history, "")

    def test_get_history_does_not_include_duplicate_fish_commands(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/fish"
        # act
        with patch('copilot.history_file.fish_history_file_lines') as mock_fish_history_file_lines:
            mock_fish_history_file_lines.return_value = [
                "- cmd: ls\n",
                "- cmd: ls\n",
            ]
            history = get_history()
        # assert
        self.assertEqual(history.count("ls"), 1)

    def test_get_history_does_not_include_duplicate_zsh_commands(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/zsh"
        # act
        with patch('copilot.history_file.zsh_history_file_lines') as mock_zsh_history_file_lines:
            mock_zsh_history_file_lines.return_value = [
                ": 1611234567:0;ls",
                ": 1611234567:0;ls",
            ]
            history = get_history()
        # assert
        self.assertEqual(history.count("ls"), 1)

    # bash

    def test_get_history_returns_empty_string_if_bash_history_file_is_empty(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/bash"
        # act
        with patch('copilot.history_file.bash_history_file_lines') as mock_bash_history_file_lines:
            mock_bash_history_file_lines.return_value = []
            history = get_history()
        # assert
        self.assertEqual(history, "")

    def test_get_history_does_not_include_duplicate_bash_commands(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/bash"
        # act
        with patch('copilot.history_file.bash_history_file_lines') as mock_bash_history_file_lines:
            mock_bash_history_file_lines.return_value = [
                "ls",
                "ls",
            ]
            history = get_history()
        # assert
        self.assertEqual(history.count("ls"), 1)

    def test_get_history_processed_bash_history_file(self):
        # arrange
        os.environ["SHELL"] = "/usr/bin/bash"
        # act
        with patch('copilot.history_file.bash_history_file_lines') as mock_bash_history_file_lines:
            mock_bash_history_file_lines.return_value = [
                "ls",
                "cd /home/username",
            ]
            history = get_history()
        # assert
        self.assertTrue("ls" in history)
        self.assertTrue("cd /home/username" in history)
