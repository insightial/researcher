import time
import streamlit as st
from hooks import update_thread_name, delete_thread


@st.dialog("Change thread name")
def update_thread_name_dialog(cookies, thread_id, current_name, message_container):
    new_name = st.text_input("Enter new thread name:", value=current_name)
    if st.button("Update Name"):
        update_thread_name(cookies, thread_id, new_name)
        with message_container:
            st.success("Thread name updated")
            time.sleep(3)
            st.empty()
        st.rerun()


@st.dialog("Delete Thread")
def delete_thread_dialog(cookies, thread_id, message_comtainer):
    st.subheader("Are you sure you want to delete?")
    if st.button("Delete"):
        status_code = delete_thread(cookies, thread_id)
        with message_comtainer:
            if status_code == 200:
                st.success("Thread deleted")
            else:
                st.error("Error deleting the thread")
            time.sleep(3)
            st.empty()
        st.rerun()
