import os
import time
import requests
import streamlit as st

RESEARCHER_API_ENDPOINT = os.getenv("RESEARCHER_API_ENDPOINT")


def get_user_threads(cookies):
    response = requests.get(
        f"{RESEARCHER_API_ENDPOINT}/threads",
        cookies={"access_token": cookies.get("access_token")},
    )
    if response.status_code == 200:
        return response.json()["threads"]
    st.toast("Failed to fetch user threads")
    return []


def clear_thread_history(cookies):
    response = requests.delete(
        f"{RESEARCHER_API_ENDPOINT}/clear_thread",
        cookies={"access_token": cookies.get("access_token")},
        json={"thread_id": st.session_state.current_thread},
    )
    if response.status_code != 200:
        st.toast("Failed to clear thread history")


def get_messages_by_thread_id(thread_id, cookies):
    response = requests.get(
        f"{RESEARCHER_API_ENDPOINT}/messages/thread/",
        cookies={"access_token": cookies.get("access_token")},
        params={"thread_id": thread_id},
    )
    if response.status_code == 200:
        return response.json()["messages"]
    st.toast("Failed to fetch messages for the selected thread")
    return []


def create_new_thread(cookies):
    response = requests.post(
        f"{RESEARCHER_API_ENDPOINT}/thread",
        cookies={"access_token": cookies.get("access_token")},
    )
    if response.status_code == 200:
        thread_id = response.json()["thread_id"]
        st.session_state.current_thread = thread_id
        st.toast(f"New thread created: {thread_id}")
        time.sleep(1)
    else:
        st.toast("Failed to create a new thread")
        time.sleep(1)


def update_thread_name(cookies, thread_id: str, new_name: str) -> None:
    response = requests.put(
        f"{RESEARCHER_API_ENDPOINT}/thread",
        cookies={"access_token": cookies.get("access_token")},
        params={"thread_id": thread_id, "name": new_name},
    )
    return response.status_code


def delete_thread(cookies, thread_id: str) -> None:
    response = requests.delete(
        f"{RESEARCHER_API_ENDPOINT}/thread",
        cookies={"access_token": cookies.get("access_token")},
        params={"thread_id": thread_id},
    )
    return response.status_code
