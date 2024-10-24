import os

import requests
import streamlit as st

RESEARCHER_API_ENDPOINT = os.getenv("RESEARCHER_API_ENDPOINT")


def get_messages_by_thread_id(thread_id, cookies):
    response = requests.get(
        f"{RESEARCHER_API_ENDPOINT}/get_messages_by_thread_id/{thread_id}",
        cookies={"access_token": cookies.get("access_token")},
    )
    if response.status_code == 200:
        return response.json()["messages"]
    st.error("Failed to fetch messages for the selected thread")
    return []
