from chatbot import stream_response
from memory import ConversationMemory
from personas import PERSONAS




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

        memory.add_user_message(content=user_input)
        messages=memory.get_messages()
        assistant_response=stream_response(messages=messages)
        memory.add_assistant_message(content=assistant_response)


if __name__=="__main__":
    main()