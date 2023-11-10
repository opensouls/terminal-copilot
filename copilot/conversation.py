import argparse
from dataclasses import dataclass
from enum import Enum


class Model(Enum):
    GPT_4 = "gpt-4"
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_4_TURBO = "gpt-4-1106-preview"


def argparse_model_type(model_str):
    try:
        return Model[model_str.upper().replace("-", "_")]
    except KeyError:
        raise argparse.ArgumentTypeError(f"Invalid model: {model_str}. Allowed values are 'gpt-4', 'gpt-4-turbo' and 'gpt-3.5-turbo'.")


@dataclass
class Conversation:
    messages: list[dict]
    model: Model
