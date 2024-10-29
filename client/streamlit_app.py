"""Streamlit app for Insightial Researcher"""

import os
import streamlit as st
from auth.cognito import check_auth_status
from streamlit_cookies_manager import CookieManager
from components import footer, show_signin, show_signup
from screens.research import research_page

# Initialize cookie manager once at the top
cookies = CookieManager()


def login():
    """
    Main function for the Streamlit app.
    """
    with st.container():
        # Apply custom CSS
        css_path = os.path.join(os.path.dirname(__file__), "style", "main.css")
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        col1, col2 = st.columns([5, 2])
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
                show_signin(cookies)  # Pass cookies as an argument
            with tab2:
                show_signup()

        footer()


def logout():
    cookies["access_token"] = None
    st.rerun()


if __name__ == "__main__":

    research_pages = [
        st.Page(
            lambda: research_page(cookies), title="Research", icon=":material/science:"
        )
    ]
    accounts_pages = [st.Page(logout, title="Logout", icon=":material/logout:")]

    # Check authentication status
    if cookies.ready() and check_auth_status(cookies):
        pg = st.navigation({"Research": research_pages, "Accounts": accounts_pages})
    else:
        pg = st.navigation([st.Page(login, title="Login", icon=":material/login:")])
    pg.run()
