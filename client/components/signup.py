import streamlit as st
from auth.cognito import sign_up_user


def show_signup():
    new_username = st.text_input("Username", key="signup_username")
    new_password = st.text_input("Password", type="password", key="signup_password")
    email = st.text_input("Email")
    if st.button("Sign up"):
        if new_username and new_password and email:
            if sign_up_user(new_username, new_password, email):
                st.toast(
                    "Sign up successful! Please check your email for verification."
                )
        else:
            st.warning("Please fill in all fields.")
