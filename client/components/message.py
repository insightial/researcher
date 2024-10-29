import streamlit as st


def message(content, is_user=False):
    """
    Display a chat message in the Streamlit app.

    Args:
    content (str): The message content to display.
    is_user (bool): True if the message is from the user, False if from the assistant.
    key (str): An optional unique key for the message component.
    """
    if is_user:
        st.chat_message("user").write(content)
    else:
        st.chat_message("assistant").write(content)
