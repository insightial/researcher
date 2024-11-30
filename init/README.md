# Initialization SQL Scripts

This directory contains SQL scripts necessary for setting up the database schema for the `langgraph` project. These scripts create the required tables and extensions to support the application's functionality.

## SQL Files

### create_chat_history_table.sql

- **Purpose**: This script creates the `chat_history` table, which stores chat messages associated with a session. Each message is stored as a JSONB object, allowing for flexible storage of message data.
- **Usage**: This table is essential for maintaining a history of user interactions, which can be used for analytics, debugging, or enhancing user experience by providing context in ongoing sessions.

### create_checkpoints_table.sql

- **Purpose**: This script sets up several tables related to checkpoints, including `checkpoint_migrations`, `checkpoints`, `checkpoint_blobs`, and `checkpoint_writes`. These tables are used to manage the state and progress of various tasks within the application.
- **Usage**: Checkpoints are crucial for tracking the progress of long-running tasks, enabling the application to resume operations from a known state in case of interruptions. This is particularly useful in complex workflows where tasks may depend on the completion of previous steps.

### create_files_table.sql

- **Purpose**: This script creates the `user_files` table, which stores metadata about files uploaded by users, including the file name, S3 location, and deletion status.
- **Usage**: This table is used to manage user-uploaded files, ensuring that metadata is easily accessible for file retrieval, management, and indexing operations.

### create_pgvector_extension.sql

- **Purpose**: This script creates the `embedding` extension, which is necessary for handling vector data within PostgreSQL.
- **Usage**: The `embedding` extension is used to store and query vector data, which is essential for applications involving machine learning models, such as those that use embeddings for natural language processing tasks.

### create_threads_table.sql

- **Purpose**: This script creates the `threads` table, which stores information about chat threads, including the thread ID, username, and thread name.
- **Usage**: This table is used to organize and manage chat sessions, allowing users to maintain multiple conversations and retrieve them as needed.

## Usage

1. Ensure you have a PostgreSQL database set up and accessible.
2. Run each SQL script in the order listed to set up the necessary tables and extensions.
3. Verify that each table and extension has been created successfully.

## Notes

- These scripts are designed to be idempotent, meaning they can be run multiple times without causing errors, as they use `IF NOT EXISTS` clauses.
- Ensure that the database user executing these scripts has the necessary permissions to create tables and extensions.

This setup is tailored for the `langgraph` project and may require adjustments for other environments or projects.
