# API Module

This directory contains the FastAPI application and its associated routes for the Researcher project. The API is designed to handle various operations related to user authentication, file management, messaging, and research functionalities.

## Main Application File

- **[app.py](./app.py)**: This is the main entry point for the FastAPI application. It sets up the application, including middleware, routes, and the application lifespan. The application uses CORS middleware to allow requests from specified origins and includes routers for different functionalities.

## Routes

The API is organized into several route modules, each handling specific aspects of the application:

### Authentication Route

- **[auth.py](./route/auth.py)**: Manages user authentication using AWS Cognito. It includes endpoints for user signup, login, email verification, and logout. The module also provides helper functions for JWT token creation and verification.

### File Management Route

- **[file.py](./route/file.py)**: Handles file operations, including retrieving, adding, updating, and deleting file metadata in the database. It ensures that file operations are performed securely and efficiently.

### Messaging Route

- **[message.py](./route/message.py)**: Provides endpoints to retrieve messages by thread ID. It ensures that messages are only accessible to users who own the corresponding threads.

### Research Route

- **[research.py](./route/research.py)**: Manages research-related operations, including processing chat requests and managing chat history. It integrates with the Researcher graph to process user prompts and generate responses.

### S3 Operations Route

- **[s3.py](./route/s3.py)**: Handles file uploads to S3 and indexes them in the PGEmbedding vector store. It ensures that files are securely uploaded and indexed for efficient retrieval and processing.

### Thread Management Route

- **[thread.py](./route/thread.py)**: Manages chat threads, including creating, updating, retrieving, and deleting threads. It ensures that thread operations are restricted to the owning user.

## Utilities

- **[utils/auth.py](./utils/auth.py)**: Contains helper functions for authentication, including JWT token management, user verification, and secret hash calculation for AWS Cognito.

## Usage

1. Ensure you have Python and FastAPI installed.
2. Set up your environment variables, including AWS credentials and Cognito configuration.
3. Run the FastAPI application:
   ```bash
   uvicorn api.app:app --reload
   ```
4. Access the API documentation at `http://localhost:8000/docs` to explore available endpoints and their functionalities.

## Notes

- Ensure that the environment variables are correctly set up to enable seamless integration with AWS services.
- The API is designed to be modular, allowing for easy extension and maintenance.

This setup is tailored for the Researcher project and may require adjustments for other environments or projects.
