import os
from dotenv import load_dotenv
from openai import OpenAI
from retryy import retry_with_backoff

load_dotenv()

client=OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

MODEL=os.getenv("MODEL")

@retry_with_backoff
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