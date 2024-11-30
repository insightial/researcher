# Multi Agent Researcher

The Multi Agent Researcher project is an advanced research tool designed to automate and enhance the process of gathering, analyzing, and synthesizing information from both web and local sources. It integrates various components such as document processing, embeddings, chat history management, and state management, leveraging technologies like OpenAI's language models and PostgreSQL for data persistence.

## Overview

This project is organized into several modules, each with its own README file providing detailed information:

- **[Infrastructure Setup](./infra/README.md)**: Contains Terraform configuration files for setting up the necessary AWS infrastructure, including modules for Cognito, S3, and Aurora.

- **[API Module](./api/README.md)**: Describes the FastAPI application that handles user authentication, file management, messaging, and research functionalities.

- **[Researcher Module](./researcher/README.md)**: Details the core logic of the Researcher project, including document loading, embeddings, chat history, and state management.

- **[Initialization SQL Scripts](./init/README.md)**: Provides SQL scripts for setting up the database schema, including tables for chat history, checkpoints, and user files.

- **[Client Module](./client/README.md)**: Describes the client-side components of the project, built using Streamlit, providing a user-friendly interface for interacting with the Researcher project.

## Key Features

- **PGEmbeddings**: Utilized for PostgreSQL tables, offering superior performance [compared to PGVector](https://neon.tech/blog/pg-embedding-extension-for-vector-search) for storing and querying vector data.
- **Streamlit Frontend**: Provides an interactive and user-friendly interface for users to manage files, conduct research, and collaborate.
- **FastAPI Backend**: Handles API requests efficiently, managing user authentication, file operations, and research functionalities.
- **Langgraph AI Agent**: Implements a cyclic agentic loop for researching any topic, inspired by [GPT Researcher](https://github.com/assafelovic/gpt-researcher/tree/master)
- **Vectorstore**: Used for storing and searching documents and chat history, ensuring efficient retrieval and management of data.

## Installation

To install the necessary dependencies, use the `pyproject.toml` file with Poetry:

```bash
poetry install
```

Ensure you have Python 3.10 or higher installed, as specified in the `pyproject.toml`.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for more details.

## Contribution

Contributions are welcome! Please follow the guidelines outlined in the project's documentation and ensure that all code is well-documented and tested.

## Langgraph Studio Support

The project supports Langgraph Studio, which allows for visualizing and managing the Langchain graph. The configuration for Langgraph Studio is specified in the [langgraph.json](./langgraph.json) file, and the main graph logic is implemented in the [langgraph_api/api.py](./langgraph_api/api.py).

## Notes

This README provides a high-level overview of the Researcher project. For more detailed information, please refer to the individual README files in each module. Adjustments may be necessary for different environments or specific project requirements.
