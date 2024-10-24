import os

import requests
import streamlit as st

RESEARCHER_API_ENDPOINT = os.getenv("RESEARCHER_API_ENDPOINT")


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
