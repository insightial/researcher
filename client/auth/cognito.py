import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Cognito configuration
RESEARCHER_API_ENDPOINT = os.getenv("RESEARCHER_API_ENDPOINT")


def authenticate_user(email, password, cookies):
    """
    Authenticates a user with the provided email and password.
    Returns the user data if successful, None otherwise.
    """
    try:
        response = requests.post(
            f"{RESEARCHER_API_ENDPOINT}/login",
            json={"email": email, "password": password},
        )
        if response.status_code == 200:
            # Extract the cookie from the response
            session_cookie = response.cookies.get("access_token")
            if session_cookie:
                cookies["access_token"] = session_cookie
                cookies.save()
            return {"success": True, "data": response.json()}
        return {"error": json.loads(response.text)}
    except requests.exceptions.RequestException as e:
        return {"error": e}


def sign_up_user(username, password, email):
    """
    Signs up a new user with the provided username, password, and email.
    Returns True if successful, False otherwise.
    """
    try:
        response = requests.post(
            f"{RESEARCHER_API_ENDPOINT}/signup",
            json={"username": username, "password": password, "email": email},
        )
        if response.status_code == 200:
            return {"success": True}
        return {"error": f"Sign up failed: {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Sign up failed: {e}"}


def verify_email(email, code):
    """
    Verifies a user's email with the provided verification code.
    Returns True if successful, False otherwise.
    """
    try:
        response = requests.post(
            f"{RESEARCHER_API_ENDPOINT}/verify-email",
            json={"email": email, "code": code},
        )
        if response.status_code == 200:
            return True
        # print(f"Email verification failed: {response.text}")
        return False
    except requests.exceptions.RequestException as e:
        # print(f"Email verification failed: {e}")
        return False


def resend_verification_code(email):
    """
    Resends a verification code to the user's email.
    Returns True if successful, False otherwise.
    """
    try:
        response = requests.post(
            f"{RESEARCHER_API_ENDPOINT}/resend-code",
            json={"email": email},
        )
        if response.status_code == 200:
            return True
        print(f"Failed to resend verification code: {response.text}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to resend verification code: {e}")
        return False


def logout(cookies):
    """
    Logs out a user by clearing the access token cookie.
    Returns True if successful, False otherwise.
    """
    try:
        response = requests.post(
            f"{RESEARCHER_API_ENDPOINT}/logout",
            cookies={"access_token": cookies.get("access_token")},
        )
        if response.status_code == 200:
            cookies.delete("access_token")
            cookies.save()
            return True
        print(f"Logout failed: {response.text}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Logout failed: {e}")
        return False


def check_auth_status(cookies):
    """
    Checks if the user is authenticated using the session cookie.
    Returns True if authenticated, False otherwise.
    """
    try:
        response = requests.get(
            f"{RESEARCHER_API_ENDPOINT}/check_auth",
            cookies={"access_token": cookies.get("access_token")},
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
