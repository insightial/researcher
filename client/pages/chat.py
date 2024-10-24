import streamlit as st
from auth.cognito import check_auth_status
from components.message import message
from hooks import (
    create_new_thread,
    get_ai_response,
    get_messages_by_thread_id,
    get_user_threads,
)
from streamlit_cookies_manager import CookieManager


def chat_page():
    # Initialize cookie manager
    cookies = CookieManager()

    # Check if user is authenticated
    try:
        if not check_auth_status(cookies):
            st.warning("Please log in to access the chat.")
            st.switch_page("pages/home.py")
            return
    except Exception as e:
        st.error(f"An error occurred while checking authentication status: {str(e)}")
        return

    st.title("Research Assistant")

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


if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed",
        page_title="Insightial Researcher",
    )
    chat_page()
