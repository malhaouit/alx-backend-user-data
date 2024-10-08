#!/usr/bin/env python3
""" Covers a Basic Authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """ Implements a Basic Authentication
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Extracts the Base64 part from the Authorization header
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decodes the value of a Base64 string
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(
                    base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> str:
        """ Extracts the user credentials for the the decoded
        authorization header
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)

        if auth_header is None:
            return None

        extracted_val = self.extract_base64_authorization_header(auth_header)
        if extracted_val is None:
            return None

        decoded_val = self.decode_base64_authorization_header(extracted_val)
        if decoded_val is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_val)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
