import streamlit as st
from auth.cognito import check_auth_status
from dialog import update_thread_name_dialog, delete_thread_dialog
from components.message import message
from hooks import (
    create_new_thread,
    get_ai_response,
    get_messages_by_thread_id,
    get_user_threads,
)


def research_page(cookies):

    # Create a container for the message
    message_container = st.empty()

    # Check if user is authenticated
    if not cookies.ready() and not check_auth_status(cookies):
        st.warning("Please log in to access the chat.")
        st.rerun()

    st.title("Research Assistant")

    with st.sidebar:
        st.markdown("**Chat Threads**")
        if st.button(
            ":heavy_plus_sign:", help="Create a new chat thread", key="new_thread"
        ):
            create_new_thread(cookies, message_container)

        threads = get_user_threads(cookies)
        for thread in threads:
            # Using columns to arrange buttons in a single row
            col1, col2, col3 = st.columns([6, 1, 1])

            with col1:
                # Main button for selecting the thread
                if st.button(
                    (
                        f"{thread['name'][:20]}..."
                        if len(thread["name"]) > 20
                        else thread["name"]
                    ),
                    key=thread["id"],
                ):
                    st.session_state.current_thread = thread["id"]
                    st.session_state.messages = []

            with col2:
                # Button to update the thread with a wrench icon
                if st.button(":material/edit:", key=f"update_{thread['id']}"):
                    update_thread_name_dialog(
                        cookies, thread["id"], thread["name"], message_container
                    )

            with col3:
                # Button to delete the thread with a warning icon
                if st.button(":material/delete:", key=f"delete_{thread['id']}"):
                    delete_thread_dialog(cookies, thread["id"], message_container)

    # Main chat
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    if st.session_state.get("current_thread"):
        messages = get_messages_by_thread_id(st.session_state.current_thread, cookies)
        for msg in messages:
            if msg["content"]:
                message(msg["content"], is_user=(msg["type"] == "human"))

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
