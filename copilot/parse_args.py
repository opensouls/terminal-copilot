import argparse

from copilot.conversation import argparse_model_type, Model


def parse_terminal_copilot_args():
    parser = argparse.ArgumentParser(prog="copilot", description="Terminal Copilot")
    parser.add_argument(
        "command", type=str, nargs="+", help="Describe the command you are looking for."
    )
    parser.add_argument(
        "-a",
        "--alias",
        action="store_true",
        help="Include aliases in the prompt. Note: This feature may potentially send sensitive information to OpenAI.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )
    parser.add_argument(
        "-g", "--git", action="store_true", help="Include git info if available"
    )
    parser.add_argument(
        "-hist",
        "--history",
        action="store_true",
        help="Include terminal history in the prompt. Note: This feature may potentially send sensitive information to OpenAI and increase the number of tokens used.",
    )
    parser.add_argument(
        "-j", "--json", action="store_true", help="Output data as JSON instead of using an interactive prompt."
    )
    parser.add_argument(
        "-c", "--count", help="The number of commands to output when JSON output is specified."
    )
    parser.add_argument(
        "-m", "--model", type=argparse_model_type, default=Model.GPT_35_TURBO,
        help="The model to use. Defaults to gpt-3.5-turbo."
    )
    parser.add_argument(
        "-ns", "--no-stream", action="store_true",
        default=False,
        help="Disable streaming the command into the terminal (by default, streaming is enabled)."
    )
    parser.add_argument(
        "-q", "--question", action="store_true", default=False, help="Ask a general question to GPT-4."
    )
    args = parser.parse_args()
    return args
