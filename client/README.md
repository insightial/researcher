# Client Module

The client module is a Streamlit application designed to provide a user-friendly interface for interacting with the Researcher project. It includes features for user authentication, file management, and research functionalities, all integrated into a seamless web application.

## Main Application File

- **[streamlit_app.py](./streamlit_app.py)**: This is the main entry point for the Streamlit application. It sets up the application layout, handles navigation, and integrates various components and screens to provide a cohesive user experience.

## Components

### Authentication

- **[auth/cognito.py](./auth/cognito.py)**: Handles user authentication using AWS Cognito. It provides functions for logging in, signing up, verifying emails, and managing session cookies.

### Dialogs

- **[dialog](./dialog)**: Contains dialog components for user interactions, such as verifying email, selecting files, and managing threads. These dialogs enhance user experience by providing interactive pop-ups for specific actions.

### Hooks

- **[hooks](./hooks)**: Provides utility functions for interacting with the backend API. It includes functions for managing chat threads, fetching AI responses, and handling file operations.

### Screens

- **[screens](./screens)**: Defines the main pages of the application, including the research page and file management page. Each screen is responsible for rendering its respective UI components and handling user interactions.

### Components

- **[components](./components)**: Contains reusable UI components, such as the footer, sign-in, and sign-up forms. These components are used across different screens to maintain a consistent look and feel.

### Style

- **[style/main.css](./style/main.css)**: Provides custom CSS styling for the Streamlit app, ensuring a modern and cohesive design throughout the application.

## Streamlit Integration

The client app is built using Streamlit, a powerful framework for creating interactive web applications in Python. Streamlit allows for rapid development and deployment of data-driven applications, making it an ideal choice for the Researcher project.

## Usage

1. Ensure you have Streamlit installed. You can install it via poetry:
   ```bash
   poetry install
   ```
2. Run the Streamlit application:
   ```bash
   poetry run streamlit run streamlit_app.py
   ```
3. Access the application in your web browser at `http://localhost:8501`.

## Notes

This module is designed to be modular and extensible, allowing for easy integration with other components and services. It provides a user-friendly interface for interacting with the Researcher project, enabling users to manage files, conduct research, and collaborate effectively.

This setup is tailored for the Researcher project and may require adjustments for other environments or projects.
