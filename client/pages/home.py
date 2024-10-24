import streamlit as st
from components import footer, show_signin, show_signup
from streamlit_cookies_manager import CookieManager


def home_page():
    cookies = CookieManager()

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

    footer()


if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed",
        page_title="Insightial Researcher",
    )
    home_page()
