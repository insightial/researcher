"""
Message utilities for the Researcher app.
"""

from .database import get_db_connection


async def get_messages_by_session_id(session_id: str):
    """
    Retrieve chat messages for a given session ID from the database.

    :param session_id: The session ID to retrieve messages for.
    :return: A list of dictionaries containing the message content and type.
    """
    async with get_db_connection() as connection:
        cursor = connection.cursor()
        select_query = """
        SELECT message->'data'->>'content' AS content, message->>'type' AS type
        FROM chat_history
        WHERE session_id = %s
        ORDER BY created_at;
        """
        await cursor.execute(select_query, (session_id,))
        messages = await cursor.fetchall()
        return [{"content": message[0], "type": message[1]} for message in messages]
