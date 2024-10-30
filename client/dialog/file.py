import time
import streamlit as st
from hooks.file import get_files  # Ensure you have access to get_files


@st.dialog("Select Files")
def file_selection_dialog(files):
    file_mapping = {
        file["file_name"]: file["s3_location"] for file in files if not file["deleted"]
    }
    file_options = list(file_mapping.keys())
    selected_file_names = st.multiselect(
        "Select files to send", options=[""] + file_options
    )

    if st.button("Confirm Selection"):
        st.session_state.file_selection = selected_file_names
        st.toast("Files selected")
        st.rerun()
