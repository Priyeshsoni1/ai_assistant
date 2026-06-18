import tiktoken

ENCODING=tiktoken.get_encoding("cl100k_base")

def count_text_tokens(text:str)->int:
    return len(ENCODING.encode(text))

def count_message_tokens(messages:list)->int:
    total_tokens=0
    for message in messages:
        total_tokens +=len(ENCODING.encode(message["content"]))
    return total_tokens


