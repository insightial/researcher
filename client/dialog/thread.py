import time
import streamlit as st
from hooks import update_thread_name, delete_thread


@st.dialog("Change thread name")
def update_thread_name_dialog(cookies, thread_id, current_name):
    new_name = st.text_input("Enter new thread name:", value=current_name)
    if st.button("Update Name"):
        update_thread_name(cookies, thread_id, new_name)
        st.toast("Thread name updated")
        time.sleep(1)
        st.empty()
        st.rerun()


@st.dialog("Delete Thread")
def delete_thread_dialog(cookies, thread_id):
    st.subheader("Are you sure you want to delete?")
    if st.button("Delete"):
        status_code = delete_thread(cookies, thread_id)
        if status_code == 200:
            st.toast("Thread deleted")
        else:
            st.toast("Error deleting the thread")
        time.sleep(1)
        st.empty()
        st.rerun()
