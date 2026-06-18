from chatbot import stream_response
from memory import ConversationMemory
from personas import PERSONAS
from tokenizer import count_message_tokens,count_text_tokens



def main():
    
    print("="*30,"AI Assistant","="*30)
    print("Type 'exit' to quit. \n")

    memory=ConversationMemory(PERSONAS["general"])


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
        print(f"\n Prompt Tokens: {prompt_tokens}")

        assistant_response=stream_response(messages=messages)

        assistant_tokens=count_text_tokens(text=assistant_response)
        print(f"\n Assistant Tokens: {assistant_tokens}")

        memory.add_assistant_message(content=assistant_response)


if __name__=="__main__":
    main()