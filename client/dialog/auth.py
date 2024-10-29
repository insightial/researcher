import streamlit as st
from auth.cognito import verify_email, resend_verification_code


@st.dialog("Verify Email")
def verify_email_dialog(email):
    st.write(f"Verify your email: {email}")
    verification_code = st.text_input("Verification Code")
    
    # Arrange buttons in a row
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Verify"):
            if verify_email(email, verification_code):
                st.toast("Email verified")
                st.rerun()
            else:
                st.toast("Invalid verification code")
    with col2:
        if st.button("Resend code"):
            resend_verification_code(email)
            st.toast("Verification code resent")
