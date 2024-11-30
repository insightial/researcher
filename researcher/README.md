# Researcher Module

The Researcher module is designed to facilitate research by leveraging various utilities for document loading, embeddings, chat history management, and state management. It integrates with PostgreSQL for data persistence and utilizes OpenAI's language models for generating responses. This module is a core component of the Langchain graph, enabling complex workflows and interactions.

## Components

### Checkpoint Management

- **[checkpoint.py](./checkpoint/checkpoint.py)**: Manages the checkpointing process, allowing for both in-memory and PostgreSQL-backed checkpoints. This is crucial for tracking the progress of long-running tasks and ensuring that operations can resume from a known state in case of interruptions.

### Document Loading

- **[document.py](./document/document.py)**: Responsible for loading documents from various formats, including PDF, Word, Excel, and more. It provides a flexible interface for document ingestion, supporting a wide range of file types.

### Embeddings

- **[embeddings.py](./embeddings/embeddings.py)**: Provides an interface for generating embeddings using OpenAI's models. These embeddings are used for semantic search and document representation, enabling efficient information retrieval.

### Researcher Graph

- **[researcher.py](./graph/researcher.py)**: Implements the core logic of the Researcher module, integrating various components to process user queries and generate responses. It manages the flow of data through the Langchain graph, coordinating interactions between different components.

### Chat History Management

- **[history.py](./history/history.py)**: Manages chat history using PostgreSQL or in-memory storage. It provides methods for storing and retrieving chat messages, ensuring that user interactions are preserved and accessible.

### LLM Provider

- **[provider.py](./llm/provider.py)**: Handles the integration with language models, specifically OpenAI's models. It provides methods for generating responses to user queries, leveraging the capabilities of advanced language models.

### State Management

- **[graph.py](./state/graph.py)**: Implements a state graph to manage the flow of queries and responses. It defines the states and transitions within the Langchain graph, ensuring that data is processed efficiently and accurately.

### Vector Store

- **[vectorstore.py](./store/vectorstore.py)**: Supports similarity search through vector embeddings. It provides methods for loading and querying vector data, enabling efficient retrieval of relevant information.

### Utilities

- **[utils/database.py](./utils/database.py)**: Provides utility functions for database interactions, including connection management and query execution.
- **[utils/message.py](./utils/message.py)**: Contains helper functions for managing chat messages, including retrieval and formatting.
- **[utils/thread.py](./utils/thread.py)**: Provides utilities for managing chat threads, including creation, updating, and deletion.

## Notes

This module is designed to be modular and extensible, allowing for easy integration with other components and services. It is a key part of the Langchain graph, enabling complex workflows and interactions within the Researcher project.

This setup is tailored for the Researcher project and may require adjustments for other environments or projects.
