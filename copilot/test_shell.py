import os
from unittest import TestCase

from copilot import shell_adapter


class Test(TestCase):
    def test_is_fish_checks_if_SHELL_env_ends_with_fish(self):
        # arrange
        for env_shell, expected in [
            ("fish", True),
            ("bash", False),
            ("zsh", False),
            ("some/path/to/fish", True),
            ("fish/some", False),
        ]:
            with self.subTest(env_shell=env_shell):
                os.environ["SHELL"] = env_shell
                # act
                is_fish = shell_adapter.is_fish()
                # assert
                self.assertEqual(is_fish, expected)

    def test_is_zsh_checks_if_SHELL_env_ends_with_zsh(self):
        # arrange
        for env_shell, expected in [
            ("fish", False),
            ("bash", False),
            ("zsh", True),
            ("some/path/to/zsh", True),
            ("zsh/some", False),
        ]:
            with self.subTest(env_shell=env_shell):
                os.environ["SHELL"] = env_shell
                # act
                zsh = shell_adapter.is_zsh()
                # assert
                self.assertEqual(zsh, expected)

    def test_is_bash_checks_if_SHELL_env_ends_with_bash(self):
        # arrange
        for env_shell, expected in [
            ("fish", False),
            ("bash", True),
            ("zsh", False),
            ("some/path/to/bash", True),
            ("bash/some", False),
        ]:
            with self.subTest(env_shell=env_shell):
                os.environ["SHELL"] = env_shell
                # act
                bash = shell_adapter.is_bash()
                # assert
                self.assertEqual(bash, expected)
