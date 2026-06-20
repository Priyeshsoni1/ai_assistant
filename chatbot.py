# chatbot.py

import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from retryy import retry_with_backoff
from tool_schemas import TOOLS
from tool_executor import execute_tool


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

MODEL = os.getenv("MODEL")


@retry_with_backoff
def stream_response(messages,memory):
    """
    Handles:
    1. Tool calling
    2. Tool execution
    3. Final streaming response
    """

    # ----------------------------------
    # First LLM Call
    # ----------------------------------

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message

    # ----------------------------------
    # Tool Call Flow
    # ----------------------------------

    if assistant_message.tool_calls:



        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            tool_result = execute_tool(
                tool_name=tool_name,
                arguments=arguments
            )
            messages.append(
    {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(tool_result)
    }
)
 

        # ----------------------------------
        # Second LLM Call (Stream)
        # ----------------------------------

        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )

    else:

        # ----------------------------------
        # No Tool Needed
        # ----------------------------------

        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )

    # ----------------------------------
    # Stream Final Response
    # ----------------------------------

    full_response = ""

    print("\nAssistant:")

    for chunk in stream:

        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        if delta.content:

            print(
                delta.content,
                end="",
                flush=True
            )

            full_response += delta.content

    print("\n")

    return full_response