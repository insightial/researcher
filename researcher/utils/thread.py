"""
Thread utilities for the Researcher app.
"""

from .database import get_db_connection


# Create the threads table if it doesn't exist
async def init_db():
    """
    Initialize the threads table in the database if it doesn't exist.

    This function is a no-op if the table already exists.
    """
    async with get_db_connection() as connection:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS threads (
            thread_id VARCHAR(36) PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            thread_name VARCHAR(100) NOT NULL
        );
        """
        await cursor.execute(create_table_query)


# Save a new thread to the database
async def save_thread_to_db(thread_id: str, username: str, thread_name: str):
    """
    Save a new thread to the database.

    This function creates a new row in the `threads` table with the given thread_id,
    username, and thread_name.

    :param thread_id: The ID of the thread to save.
    :param username: The username of the user who owns the thread.
    :param thread_name: The name of the thread.
    """
    async with get_db_connection() as connection:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO threads (thread_id, username, thread_name)
        VALUES (%s, %s, %s);
        """
        await cursor.execute(insert_query, (thread_id, username, thread_name))


# Update thread name in the database
async def update_thread_name_in_db(thread_id: str, new_name: str):
    """
    Update the name of a thread in the database.

    This function updates the name of a thread in the `threads` table with the given
    thread_id to the new name provided.

    :param thread_id: The ID of the thread to update.
    :param new_name: The new name of the thread.
    """
    async with get_db_connection() as connection:
        cursor = connection.cursor()
        update_query = """
        UPDATE threads
        SET thread_name = %s
        WHERE thread_id = %s;
        """
        await cursor.execute(update_query, (new_name, thread_id))


# Retrieve all threads for a specific user from the database
async def get_threads_for_user_from_db(username: str):
    """
    Retrieve all threads for a specific user from the database.

    This function executes a SQL query to retrieve all threads associated with a
    specific user. The query returns a list of tuples, where each tuple contains
    the thread_id, username, and thread_name of a thread belonging to the user.

    :param username: The username of the user to retrieve threads for.
    :return: A list of dictionaries, where each dictionary contains the
        thread_id, username, and thread_name of a thread belonging to the user.
    """
    async with get_db_connection() as connection:
        cursor = connection.cursor()
        select_query = """
        SELECT thread_id, username, thread_name
        FROM threads
        WHERE username = %s;
        """
        await cursor.execute(select_query, (username,))
        threads = await cursor.fetchall()
        return [
            {"id": thread[0], "user": thread[1], "name": thread[2]}
            for thread in threads
        ]


# Delete a thread from the database
async def delete_thread_from_db(thread_id: str):
    """
    Delete a thread from the database.

    This function executes a SQL query to delete a thread with the given thread_id
    from the `threads` table.

    :param thread_id: The ID of the thread to delete.
    """
    async with get_db_connection() as connection:
        cursor = connection.cursor()
        delete_query = """
        DELETE FROM threads
        WHERE thread_id = %s;
        """
        await cursor.execute(delete_query, (thread_id,))
