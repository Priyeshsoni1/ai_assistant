# gradio_app.py

import os
import time

import gradio as gr
from dotenv import load_dotenv

from chatbot import stream_response
from analytics import UsageAnalytics
from memory import ConversationMemory
from personas import PERSONAS
from pricing import calculate_cost
from tokenizer import count_message_tokens, count_text_tokens


load_dotenv()


# --------------------------------------------------
# Session Memory
# --------------------------------------------------

memory = ConversationMemory(
    PERSONAS["ai_engineer"]
)
analytics = UsageAnalytics()


# --------------------------------------------------
# Chat Function
# --------------------------------------------------

def chat(message, history, persona):

    global memory

    history = history or []

    try:
        current_system_prompt = memory.messages[0]["content"]

        if current_system_prompt != PERSONAS[persona]:
            memory = ConversationMemory(PERSONAS[persona])
            history = []

        memory.add_user_message(message)
        messages = memory.get_messages()

        prompt_tokens = count_message_tokens(messages=messages)
        start_time = time.time()
        response = stream_response(messages=messages, memory=memory)
        end_time = time.time()
        analytics.add_latency(latency=(end_time - start_time))

        assistant_tokens = count_text_tokens(text=response)
        cost_data = calculate_cost(
            prompt_tokens=prompt_tokens,
            completion_tokens=assistant_tokens,
            model=os.getenv("MODEL")
        )
        analytics.add_usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=assistant_tokens,
            cost=cost_data[2]
        )
        memory.add_assistant_message(response)

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})

        return "", history
    except Exception as error:
        history.append({"role": "user", "content": message})
        history.append(
            {
                "role": "assistant",
                "content": f"Error: {error}"
            }
        )
        return "", history


# --------------------------------------------------
# Clear Chat
# --------------------------------------------------

def clear_chat(persona):

    global memory

    memory = ConversationMemory(PERSONAS[persona])

    return "", []


# --------------------------------------------------
# UI
# --------------------------------------------------

with gr.Blocks(title="Production AI Assistant") as demo:

    gr.Markdown(
        """
# 🚀 Production AI Assistant

Streaming • Memory • Personas • Tools
"""
    )

    with gr.Row():

        persona = gr.Dropdown(
            choices=[
                "general",
                "python_mentor",
                "ai_engineer",
                "interviewer",
                "architect"
            ],
            value="ai_engineer",
            label="Persona"
        )

        clear_btn = gr.Button(
            "Clear Chat"
        )

    chatbot = gr.Chatbot(
        label="Conversation",
        height=500
    )

    with gr.Row():

        message = gr.Textbox(
            placeholder="Ask something...",
            scale=8
        )

        send_btn = gr.Button(
            "Send",
            scale=1
        )

    send_btn.click(
        fn=chat,
        inputs=[
            message,
            chatbot,
            persona
        ],
        outputs=[
            message,
            chatbot
        ]
    )

    message.submit(
        fn=chat,
        inputs=[
            message,
            chatbot,
            persona
        ],
        outputs=[
            message,
            chatbot
        ]
    )

    clear_btn.click(
        fn=clear_chat,
        inputs=[persona],
        outputs=[message, chatbot]
    )


# --------------------------------------------------
# Launch
# --------------------------------------------------

if __name__ == "__main__":

    demo.launch()
