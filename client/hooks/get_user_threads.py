import os

import requests
import streamlit as st

RESEARCHER_API_ENDPOINT = os.getenv("RESEARCHER_API_ENDPOINT")


def get_user_threads(cookies):
    response = requests.get(
        f"{RESEARCHER_API_ENDPOINT}/get_threads",
        cookies={"access_token": cookies.get("access_token")},
    )
    if response.status_code == 200:
        return response.json()["threads"]
    st.error("Failed to fetch user threads")
    return []
