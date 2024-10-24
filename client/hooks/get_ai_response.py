import os

import requests
import streamlit as st

RESEARCHER_API_ENDPOINT = os.getenv("RESEARCHER_API_ENDPOINT")


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
