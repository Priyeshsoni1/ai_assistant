from chatbot import stream_response
from memory import ConversationMemory
from personas import PERSONAS
from tokenizer import count_message_tokens,count_text_tokens
from analytics import UsageAnalytics
from pricing import calculate_cost
from dotenv import load_dotenv
import os


def main():
    
    print("="*30,"AI Assistant","="*30)
    print("Type 'exit' to quit. \n")

    load_dotenv()

    memory=ConversationMemory(PERSONAS["general"])
    analytics=UsageAnalytics()


    while True:
        user_input=input("You: ")

        

        if user_input.lower()=='exit':
            print("Thank You ")
            break

        if user_input=="/history":
            from pprint import pprint
            pprint(memory.get_messages())
            continue

        if user_input=="/reset":
            memory.clear()
            print("Memory Cleared..")
            continue

        if user_input=="/stats":
            print()
            print(f"messages:",f"{memory.stats()["message_count"]}")
            continue
        if user_input == "/tokens":

            messages = memory.get_messages()

            token_count = count_message_tokens(
                messages
            )

            print(
                f"\nCurrent Tokens: "
                f"{token_count}"
            )

            continue

        memory.add_user_message(content=user_input)
        messages=memory.get_messages()

        prompt_tokens=count_message_tokens(messages=messages)


        assistant_response=stream_response(messages=messages)

        assistant_tokens=count_text_tokens(text=assistant_response)

        cost_data=calculate_cost(prompt_tokens=prompt_tokens,completion_tokens=assistant_tokens,model=os.getenv("MODEL"))

        analytics.add_usage(prompt_tokens=prompt_tokens,completion_tokens=assistant_tokens,cost=cost_data[2])

        memory.add_assistant_message(content=assistant_response)

        # print("\n-----After Every Response : Usage of Per Request -----")
        # print(f"prompt Tokens:",prompt_tokens)
        # print(f"assistant_ Tokens",assistant_tokens)
        # print(f"Total Tokens:",prompt_tokens+assistant_tokens)
        # print(f"Cost:f ${cost_data[2]:.2f}")


if __name__=="__main__":
    main()