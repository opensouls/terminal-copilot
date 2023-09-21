# for asking general questions directly to gpt4

from typing import List

from copilot.context import Context
from copilot.conversation import Conversation
from copilot.open_ai_adapter import stream_cmd_into_terminal, request_cmds


def ask_question(context: Context, question: List[str]) -> None:
  prompt = " ".join(question)

  messages = []
  messages.append({"role": "system", "content": "You are an AI Copilot operating in a terminal. You are a general assistant to the user."})
  messages.append({"role": "user", "content": prompt})
  conversation = Conversation(
      messages=messages,
      model=context.model
  )

  response = stream_cmd_into_terminal(conversation)
  print(response)

  