import os
from dotenv import load_dotenv
from openai import OpenAI
from personas import PERSONAS

load_dotenv()

client=OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

MODEL=os.getenv("MODEL")


def stream_response(messages):
    
    stream=client.chat.completions.create(
        messages=messages,
        model=MODEL,
        stream=True
    )

    full_responses=""

    for chunk in stream:
        content=chunk.choices[0].delta.content
        if content:
            print(content,end="",flush=True)
            full_responses+=content
    
    print()

    return full_responses