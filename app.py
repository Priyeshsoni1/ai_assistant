from chatbot import stream_response


def main():
    
    print("AI Assistant")
    print("Type 'exit' to quit. \n")

    while True:
        user_input=input("You: ")

        if user_input.lower()=='exit':
            print("Thank You ")
            break

        stream_response(user_input=user_input,persona="ai_engineer")


if __name__=="__main__":
    main()