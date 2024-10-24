from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import PostgresChatMessageHistory


class BaseMemoryManager:
    def __init__(self, memory_type="buffer", **kwargs):
        if memory_type == "postgres":
            self.memory = PostgresChatMessageHistory(**kwargs)
        else:
            self.memory = ConversationBufferMemory(return_messages=True)

    def get_memory(self):
        return self.memory

    def clear_memory(self):
        if hasattr(self.memory, "clear"):
            self.memory.clear()
