MAX_MESSAGES=20



class ConversationMemory:
    def __init__(self,system_prompt):
        self.messages=[]
        self.messages.append({
            "role":"system",
            "content":system_prompt
        })

    def add_user_message(self,content):
        
        self.messages.append(
            {
                "role":"user",
                "content":content
            }
        )
        self.trim_history()
    
    def add_assistant_message(self,content):
        self.messages.append(
            {
                "role":"assistant",
                "content":content
            }
        )
    
    def get_messages(self):
        return self.messages
    
    def clear(self):
        system_prompt=self.messages[0]
        self.messages=[system_prompt]

    def trim_history(self):
        while len(self.messages) > MAX_MESSAGES:
            self.messages.pop(1)
    
    def stats(self):
        return {
            "message_count":len(self.messages)
        }