from langchain.memory import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_postgres import PostgresChatMessageHistory

from researcher.utils.database import get_db_connection


class BaseChatHistoryManager:
    @classmethod
    async def create_history(cls, memory_type="buffer", **kwargs):
        self = cls()
        self.session_id = kwargs.get("session_id", None)
        self.table_name = kwargs.get("table_name", None)
        self.async_connection = kwargs.get(
            "async_connection", get_db_connection
        )  # Store the function itself
        if memory_type == "postgres":
            self.memory = PostgresChatMessageHistory(
                self.table_name,
                self.session_id,
                async_connection=self.async_connection,
            )
            async with self.async_connection() as connection:  # Call as function
                await self.memory.acreate_tables(
                    connection,
                    self.table_name,
                )
        else:
            self.memory = ChatMessageHistory()
        return self

    def get_memory(self):
        return self.memory

    def clear_memory(self):
        if hasattr(self.memory, "clear"):
            self.memory.clear()

    async def add_memory(self, message, message_type="human"):
        """Add messages to memory, using async connection context."""
        if message_type not in {"human", "ai"}:
            raise ValueError(f"Invalid message type: {message_type}")

        async with self.async_connection() as connection:
            # Use the memory instance to add messages with the active connection
            self.memory._aconnection = connection  # Rebind connection temporarily
            if message_type == "human":
                await self.memory.aadd_messages([HumanMessage(content=message)])
            elif message_type == "ai":
                await self.memory.aadd_messages([AIMessage(content=message)])

    async def get_session_history(self):
        """Retrieve the session history using the memory’s async method."""
        async with self.async_connection() as connection:
            self.memory._aconnection = connection  # Ensure active connection
            return await self.memory.aget_messages()
