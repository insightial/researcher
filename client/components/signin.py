import streamlit as st
from auth.cognito import authenticate_user
from dialog.auth import verify_email_dialog


def show_signin(cookies):
    email = st.text_input("Email", key="email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Log in"):
        if email and password:
            response = authenticate_user(email, password, cookies)
            if response.get("success"):
                st.toast("Login successful!")
                st.rerun()
            elif response.get("error"):
                if (
                    "detail" in response.get("error")
                    and "message" in response.get("error")["detail"]
                    and response["error"]["detail"]["message"] == "User not confirmed"
                ):
                    verify_email_dialog(email)
                else:
                    st.toast(
                        response.get("error").get("detail")
                        if response.get("error")["detail"]
                        else response.get("error")
                    )
        else:
            st.warning("Please enter both email and password.")
