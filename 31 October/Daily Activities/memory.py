# memory.py
from langchain.memory import ConversationBufferMemory

# Initialize memory with key as "chat_history" to store conversation context
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
