import streamlit as st
from auth.cognito import authenticate_user


def show_signin(cookies):
    email = st.text_input("Email", key="email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Log in"):
        if email and password:
            user = authenticate_user(email, password, cookies)
            if user:
                st.success("Login successful!")
                st.switch_page("pages/chat.py")
            else:
                st.error("Login failed. Please check your credentials.")
        else:
            st.warning("Please enter both email and password.")
