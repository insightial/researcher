import os

import requests
import streamlit as st

RESEARCHER_API_ENDPOINT = os.getenv("RESEARCHER_API_ENDPOINT")


def clear_thread_history(cookies):
    response = requests.post(
        f"{RESEARCHER_API_ENDPOINT}/clear_thread",
        cookies={"access_token": cookies.get("access_token")},
        json={"thread_id": st.session_state.current_thread},
    )
    if response.status_code != 200:
        st.error("Failed to clear thread history")
