# chatbot.py

import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from retryy import retry_with_backoff
from tool_schemas import TOOLS
from tool_executor import execute_tool
from logger import log_event

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
    log_event("Sending request to model")
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
    except Exception as error:
        log_event(f"Model request failed: {error}")
        raise RuntimeError(f"Model request failed: {error}") from error

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

            try:
                tool_result = execute_tool(
                    tool_name=tool_name,
                    arguments=arguments
                )
            except Exception as error:
                log_event(f"Tool execution failed: {error}")
                tool_result = {"error": str(error)}
            log_event(
                f"Result: "
                f"{tool_result}"
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

        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True
            )
        except Exception as error:
            log_event(f"Streaming request failed: {error}")
            raise RuntimeError(f"Streaming request failed: {error}") from error

    else:

        # ----------------------------------
        # No Tool Needed
        # ----------------------------------

        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True
            )
        except Exception as error:
            log_event(f"Streaming request failed: {error}")
            raise RuntimeError(f"Streaming request failed: {error}") from error

    # ----------------------------------
    # Stream Final Response
    # ----------------------------------

    full_response = ""

    print("\nAssistant:")

    try:
        for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta.content:
                print(delta.content, end="", flush=True)
                full_response += delta.content
    except Exception as error:
        log_event(f"Stream consumption failed: {error}")
        raise RuntimeError(f"Stream consumption failed: {error}") from error

    print("\n")
    log_event("Model response streamed successfully")
    return full_response
