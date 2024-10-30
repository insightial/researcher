import streamlit as st
from auth.cognito import check_auth_status
from dialog import (
    update_thread_name_dialog,
    delete_thread_dialog,
    file_selection_dialog,
)
from components.message import message
from hooks import (
    create_new_thread,
    get_ai_response,
    get_messages_by_thread_id,
    get_user_threads,
)
from hooks.file import get_files  # Import get_files to fetch user files


def research_page(cookies):

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
            create_new_thread(cookies)

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
                    st.session_state.file_selection = []
            with col2:
                # Button to update the thread with a wrench icon
                if st.button(":material/edit:", key=f"update_{thread['id']}"):
                    update_thread_name_dialog(cookies, thread["id"], thread["name"])

            with col3:
                # Button to delete the thread with a warning icon
                if st.button(":material/delete:", key=f"delete_{thread['id']}"):
                    delete_thread_dialog(cookies, thread["id"])

    # Main chat
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Fetch files
    files = get_files(cookies)

    # Create a mapping of file_name to s3_location for easy lookup
    file_mapping = {
        file["file_name"]: file["s3_location"] for file in files if not file["deleted"]
    }

    # File selection dialog
    if "file_selection" not in st.session_state:
        st.session_state.file_selection = []
    files = get_files(cookies)
    if st.button("Select Files"):
        file_selection_dialog(files)

    # Display selected files
    selected_file_locations = [
        file_mapping.get(selected_file_name)
        for selected_file_name in st.session_state.file_selection
    ]

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

        # Get AI response, using s3_location if a file was selected
        response = get_ai_response(
            cookies,
            prompt,
            files=selected_file_locations if selected_file_locations else [],
        )

        # Display assistant response in chat message container
        message(response, is_user=False)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
