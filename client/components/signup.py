import streamlit as st
from auth.cognito import sign_up_user
from dialog.auth import verify_email_dialog


def show_signup():
    email = st.text_input("Email")
    new_username = st.text_input("Username", key="signup_username")
    new_password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign up"):
        if new_username and new_password and email:
            response = sign_up_user(new_username, new_password, email)
            if response.get("success"):
                st.toast(
                    "Sign up successful! Please check your email for verification."
                )
                verify_email_dialog(email)
            else:
                st.toast(response.get("error"))
        else:
            st.warning("Please fill in all fields.")
