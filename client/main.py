"""Streamlit app for Insightial Researcher"""

import os

import streamlit as st
from auth.cognito import check_auth_status
from components import show_signin, show_signup
from streamlit_cookies_manager import CookieManager


def main():
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

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Insightial Researcher")
        st.markdown(
            """
        - **Intelligent query processing**
        - **Vast knowledge bases**
        - **Real-time information synthesis**
        - **Customizable research parameters**
        - **Collaborative research environment**
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
        <div style="padding: 20px; border-radius: 10px; text-align: center;">
            <h2 style="margin-bottom: 10px;">Get Started</h2>
            <p style="color: #6a6a8c; font-size: 14px;">
                Unlock the power of AI-assisted research. Log in or sign up to explore intelligent query processing, 
                vast knowledge bases, and real-time information synthesis.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        tab1, tab2 = st.tabs(["Log in", "Sign up"])
        with tab1:
            show_signin(cookies)
        with tab2:
            show_signup()

    # Footer
    st.markdown(
        """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background-color: #0f0f23;">
        <p style="color: #b19cd9; margin: 0;">© 2024 Insightial. All rights reserved.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
