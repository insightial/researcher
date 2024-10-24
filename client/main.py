"""Streamlit app for Insightial Researcher"""

import os

import streamlit as st
from auth.cognito import check_auth_status
from streamlit_cookies_manager import CookieManager


def app():
    """
    Main function for the Streamlit app.
    """

    # Initialize cookie manager
    cookies = CookieManager()

    # Apply custom CSS
    css_path = os.path.join(os.path.dirname(__file__), "style", "main.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Check authentication status
    try:
        if check_auth_status(cookies):
            st.switch_page("pages/chat.py")
    except Exception as e:
        st.error(f"An error occurred while checking authentication status: {str(e)}")
        return

    st.switch_page("pages/home.py")


if __name__ == "__main__":
    app()
