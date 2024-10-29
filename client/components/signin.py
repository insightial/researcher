import streamlit as st
from auth.cognito import authenticate_user


def show_signin(cookies):
    email = st.text_input("Email", key="email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Log in"):
        if email and password:
            user = authenticate_user(email, password, cookies)
            if user:
                st.toast("Login successful!")
                st.rerun()
            else:
                st.toast("Login failed. Please check your credentials.")
        else:
            st.warning("Please enter both email and password.")
