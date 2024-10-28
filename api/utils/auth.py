"""Module to hold helper functions for authentication."""

import base64
import datetime
import hashlib
import hmac
import os
from json import dumps

import httpx
import jwt
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv
from email_validator import EmailNotValidError, validate_email
from fastapi import Cookie, Depends, HTTPException, Request, status
from jwt import PyJWKClient
from jwt.exceptions import DecodeError, ExpiredSignatureError

load_dotenv()

ALGORITHM = os.environ.get("ALGORITHM")


def create_access_token(data: dict, expires_delta: datetime.timedelta, secret_key: str):
    """
    Function to create an access token.
    """
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token: str, secret_key: str):
    """
    Function to verify a JWT token.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload  # or True if you just need to know it's valid
    except ExpiredSignatureError:
        return {"error": "Token expired"}
    except DecodeError:
        return {"error": "Invalid token"}


def is_email(identifier: str) -> bool:
    """
    Function to check if a string is an email.
    """
    try:
        validate_email(identifier)
        return True
    except EmailNotValidError:
        return False


def get_username(users) -> str:
    """
    Function to get the username from Users Object from AWS Cognito
    """
    return users[0]["Username"]  # Return the username of the first matched user


def get_user_details(users) -> dict:
    """
    Function to get the name and email from Users Object from AWS Cognito
    """
    if not users or "Attributes" not in users[0]:
        return {"email": None, "username": None}

    attributes = users[0]["Attributes"]
    email = next(
        (item["Value"] for item in attributes if item["Name"] == "email"), None
    )

    return {"email": email, "username": get_username(users)}


async def get_user(cognito_client, identifier, user_pool_id):
    """
    Function to get username from AWS cognito, if the email exists
    """
    if is_email(identifier):
        response = cognito_client.list_users(
            UserPoolId=user_pool_id, Filter=f'email = "{identifier}"'
        )
        if not response["Users"]:
            return []
        return response["Users"]
    response = cognito_client.list_users(
        UserPoolId=user_pool_id, Filter=f'username = "{identifier}"'
    )
    if not response["Users"]:
        return []
    return response["Users"]


def user_exists(users: list):
    """
    Function to check if a uses exists on AWS Cognito
    """
    return len(users) > 0


def calculate_secret_hash(username, client_id, client_secret):
    """
    Calculate the secret hash to use with AWS Cognito requests.

    :param username: The username of the user.
    :param client_id: The client ID of the Cognito User Pool.
    :param client_secret: The client secret associated with the User Pool client.
    :return: The calculated secret hash.
    """
    message = username + client_id
    key = client_secret.encode("utf-8")
    message = message.encode("utf-8")

    dig = hmac.new(key, msg=message, digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()


def _jwks2PEM(jwks_key):
    """
    Function to convert a JWKS key to a PEM key.
    """
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(dumps(jwks_key))
    pem_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return pem_key


async def get_cognito_jwt_secret(cognito_region: str, cognito_user_pool_id: str) -> str:
    """
    Function to get the JWT secret from Cognito.
    """
    jwks_url = (
        f"https://cognito-idp.{cognito_region}.amazonaws.com/"
        f"{cognito_user_pool_id}/.well-known/jwks.json"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url)

    if response.status_code != 200:
        raise ValueError("Failed to fetch JWKS from Cognito")

    jwks = response.json()
    for key_data in jwks["keys"]:
        if key_data["alg"] == "RS256" and key_data["use"] == "sig":
            key = _jwks2PEM(key_data)
            return key.decode("utf-8")

    raise ValueError("Failed to find a suitable public key in JWKS")


async def get_token(request: Request):
    """
    Function to get the token from the request.
    """
    token = request.query_params.get("token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is required"
        )
    return token


async def check_user_exists(cognito_client, username, user_pool_id):
    """
    Function to check if a user exists.
    """
    try:
        await cognito_client.admin_get_user(UserPoolId=user_pool_id, Username=username)
        return True
    except cognito_client.exceptions.UserNotFoundException:
        return False


async def create_user(cognito_client, username, email, user_pool_id):
    """
    Function to create a user.
    """
    try:
        response = cognito_client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "email_verified", "Value": "true"},
            ],
            # MessageAction='SUPPRESS' # Use 'SUPPRESS' to prevent sending a welcome email
        )
        return response
    except cognito_client.exceptions.ClientError as error:
        raise error
