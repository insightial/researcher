import os
import requests
import streamlit as st

RESEARCHER_API_ENDPOINT = os.getenv("RESEARCHER_API_ENDPOINT")


# Function to upload a file
def upload_file(cookies, file):
    response = requests.post(
        f"{RESEARCHER_API_ENDPOINT}/upload",
        cookies={"access_token": cookies.get("access_token")},
        files={"file": file},
    )
    st.toast("File uploaded successfully")
    return response.json()


# Function to fetch user's files
def get_files(cookies):
    response = requests.get(
        f"{RESEARCHER_API_ENDPOINT}/files/",
        cookies={"access_token": cookies.get("access_token")},
    )
    return response.json()


# Function to delete a file
def delete_file(cookies, file_id):
    response = requests.delete(
        f"{RESEARCHER_API_ENDPOINT}/file",
        params={"file_id": file_id},
        cookies={"access_token": cookies.get("access_token")},
    )
    st.toast("File deleted successfully")
    return response.json()


def update_file_name(cookies, file_id, new_filename):
    response = requests.put(
        f"{RESEARCHER_API_ENDPOINT}/file",
        json={"file_id": file_id, "new_filename": new_filename},
        cookies={"access_token": cookies.get("access_token")},
    )
    st.toast("File name updated successfully")
    return response.json()
