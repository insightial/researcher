import os

import requests
import streamlit as st
from auth.cognito import check_auth_status, logout
from components.message import message
from streamlit_cookies_manager import CookieManager

RESEARCHER_API_ENDPOINT = os.getenv("RESEARCHER_API_ENDPOINT")


def chat_page():
    # Initialize cookie manager
    cookies = CookieManager()

    # Check if user is authenticated
    try:
        if not check_auth_status(cookies):
            st.warning("Please log in to access the chat.")
            st.switch_page("main.py")
            return
    except Exception as e:
        st.error(f"An error occurred while checking authentication status: {str(e)}")
        return

    st.title("AI Chat Assistant")

    # Create a layout with two columns
    col1, col2 = st.columns([1, 4])

    # Thread management column (hidden on mobile)
    with col1:
        st.markdown(
            """
            <style>
            @media (max-width: 640px) {
                [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="column"]:first-child {
                    display: none;
                }
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.subheader("Chat Threads")
        if st.button("New Thread"):
            create_new_thread(cookies)

        threads = get_user_threads(cookies)
        for thread in threads:
            if st.button(f"Thread {thread['id']}", key=f"thread_{thread['id']}"):
                st.session_state.current_thread = thread["id"]
                st.session_state.messages = []

    # Main chat column
    with col2:
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        if st.session_state.get("current_thread"):
            messages = get_messages_by_thread_id(
                st.session_state.current_thread, cookies
            )
            for i, msg in enumerate(messages):
                message(
                    msg["content"], is_user=(msg["type"] == "human"), key=f"msg_{i}"
                )

        # Move chat input to the bottom of the page
        st.markdown(
            """
            <style>
            .stChatInput {
                position: fixed;
                bottom: 0;
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # React to user input
        if prompt := st.chat_input("What would you like to know?"):
            # Display user message in chat message container
            message(prompt, is_user=True)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Get AI response
            response = get_ai_response(prompt, cookies)

            # Display assistant response in chat message container
            message(response, is_user=False)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})


def create_new_thread(cookies):
    response = requests.post(
        f"{RESEARCHER_API_ENDPOINT}/create_thread",
        cookies={"access_token": cookies.get("access_token")},
    )
    if response.status_code == 200:
        thread_id = response.json()["thread_id"]
        st.session_state.current_thread = thread_id
        st.success(f"New thread created: {thread_id}")
    else:
        st.error("Failed to create a new thread")


def get_user_threads(cookies):
    response = requests.get(
        f"{RESEARCHER_API_ENDPOINT}/get_threads",
        cookies={"access_token": cookies.get("access_token")},
    )
    if response.status_code == 200:
        return response.json()["threads"]
    st.error("Failed to fetch user threads")
    return []


def get_ai_response(prompt, cookies):
    response = requests.post(
        f"{RESEARCHER_API_ENDPOINT}/chat",
        cookies={"access_token": cookies.get("access_token")},
        json={"prompt": prompt, "thread_id": st.session_state.current_thread},
    )
    if response.status_code == 200:
        return response.json()["response"]
    st.error("Failed to get AI response")
    return "I'm sorry, I couldn't process your request at the moment."


def get_messages_by_thread_id(thread_id, cookies):
    response = requests.get(
        f"{RESEARCHER_API_ENDPOINT}/get_messages_by_thread_id/{thread_id}",
        cookies={"access_token": cookies.get("access_token")},
    )
    if response.status_code == 200:
        return response.json()["messages"]
    st.error("Failed to fetch messages for the selected thread")
    return []


def clear_thread_history(cookies):
    response = requests.post(
        f"{RESEARCHER_API_ENDPOINT}/clear_thread",
        cookies={"access_token": cookies.get("access_token")},
        json={"thread_id": st.session_state.current_thread},
    )
    if response.status_code != 200:
        st.error("Failed to clear thread history")


if __name__ == "__main__":
    chat_page()
