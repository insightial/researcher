import streamlit as st


def footer():
    # Footer
    st.markdown(
        """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background-color: #0f0f23;">
        <p style="color: #b19cd9; margin: 0;">© 2024 Insightial. All rights reserved.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
