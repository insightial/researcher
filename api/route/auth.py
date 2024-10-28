"""Description: This file contains the backend code for the Property Hunter app."""

import os
from datetime import timedelta

import boto3
from dotenv import load_dotenv
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.auth import (
    calculate_secret_hash,
    create_access_token,
    get_user,
    get_user_details,
    get_username,
    user_exists,
    verify_jwt_token,
)

load_dotenv()

COGNITO_CLIENT_SECRET = os.environ.get("COGNITO_CLIENT_SECRET")
COGNITO_REGION = os.environ.get("COGNITO_REGION")
COGNITO_CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")
COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")

router = APIRouter()

cognito_client = boto3.client("cognito-idp", region_name=COGNITO_REGION)


class LoginModel(BaseModel):
    """
    Class to define the login model.
    """

    email: str
    password: str


class SignupModel(LoginModel):
    """
    Class to define the login model.
    """

    email: str
    password: str
    username: str


@router.post("/signup")
async def sign_up(login_model: SignupModel):
    """
    Function to register a user.
    """
    username = login_model.username
    email = login_model.email
    password = login_model.password

    if await get_user(cognito_client, email, COGNITO_USER_POOL_ID):
        return JSONResponse(
            content={"message": "An account with this email already exists."},
            status_code=300,
        )

    secret_hash = calculate_secret_hash(
        username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
    )
    try:
        cognito_client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            SecretHash=secret_hash,
            Username=username,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
            ],
        )
        return JSONResponse(
            content={
                "message": "User registered successfully. Please check your email for verification.",
                "redirect": "/email-verification",
            },
            status_code=200,
        )
    except cognito_client.exceptions.CodeDeliveryFailureException:
        return JSONResponse(
            content={
                "message": "Failed to send verification code. Please try again later."
            },
            status_code=500,
        )
    except cognito_client.exceptions.ClientError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/login")
async def login_user(login_model: LoginModel, response: Response):
    """
    Function to login a user.
    """
    identifier = login_model.email
    password = login_model.password

    users = await get_user(cognito_client, identifier, COGNITO_USER_POOL_ID)
    if not user_exists(users):
        raise HTTPException(status_code=404, detail="User not Found")
    username = get_username(users)
    user_details = get_user_details(users)
    secret_hash = calculate_secret_hash(
        username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
    )
    try:
        cognito_response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": secret_hash,
            },
        )

        access_token = create_access_token(
            data={"sub": username, "email": user_details["email"]},
            expires_delta=timedelta(hours=1),
            secret_key=COGNITO_CLIENT_SECRET,
        )

        # Set the token in an HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,  # Use secure cookies in production
            samesite="lax",
            max_age=3600,
        )

        return {
            "message": "Login successful",
            "user_details": user_details,
        }

    except cognito_client.exceptions.UserNotConfirmedException:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "User not confirmed",
                "user_details": user_details,
                "redirect": "/email-verification",
            },
        )
    except cognito_client.exceptions.ClientError as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from e


class VerificationModel(BaseModel):
    """
    Class to define the login model.
    """

    username: str
    code: str


@router.post("/verify-email")
async def verify_email(verification_model: VerificationModel, response: Response):
    """
    Function to verify a user's email.
    """
    username = verification_model.username
    code = verification_model.code
    secret_hash = calculate_secret_hash(
        username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
    )
    try:
        cognito_client.confirm_sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=username,
            ConfirmationCode=code,
            SecretHash=secret_hash,
        )

        # After successful verification, log the user in
        access_token = create_access_token(
            data={"sub": username},
            expires_delta=timedelta(hours=1),
            secret_key=COGNITO_CLIENT_SECRET,
        )

        # Set the token in an HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,  # Use secure cookies in production
            samesite="lax",
            max_age=3600,
        )

        return JSONResponse(
            content={
                "message": "Email verified successfully. You are now logged in.",
                "redirect": "/chat",
            },
            status_code=200,
        )
    except cognito_client.exceptions.ExpiredCodeException:
        return JSONResponse(
            content={"message": "Verification code has expired"}, status_code=400
        )
    except cognito_client.exceptions.CodeMismatchException:
        return JSONResponse(
            content={"message": "Invalid verification code"}, status_code=400
        )
    except cognito_client.exceptions.ClientError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class ResendModel(BaseModel):
    """
    Class to define the Resend model.
    """

    username: str


@router.post("/resend-code")
async def resend_code(resend_model: ResendModel):
    """
    Function to resend verification code to the user
    """
    username = resend_model.username
    secret_hash = calculate_secret_hash(
        username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET
    )
    try:
        cognito_client.resend_confirmation_code(
            ClientId=COGNITO_CLIENT_ID,
            Username=username,
            SecretHash=secret_hash,
        )
        return {"message": "Verification code resent successfully"}
    except cognito_client.exceptions.ClientError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/logout")
async def logout(response: Response):
    """
    Function to logout a user.
    """
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}


async def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = verify_jwt_token(access_token, COGNITO_CLIENT_SECRET)
        username: str = payload.get("sub", None)
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "email": payload.get("email")}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e


@router.get("/check_auth")
async def check_auth(_: dict = Depends(get_current_user)):
    """
    Function to check if the user is authenticated
    """
    return {"authenticated": True}
