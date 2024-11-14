#!/usr/bin/env python3
"""
Handles Basic Authentication
"""
import base64
from api.v1.auth.auth import Auth
from models.base import DATA
from models.user import User
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """ Handles Basic Authentication """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Returns the Base64 part of the Authorization header

        Args:
            authorization_header (str): Authorization header

        Returns:
            (str): Base64 section of Authorization header
        """
        if not authorization_header:
            return

        if not isinstance(authorization_header, str):
            return

        try:
            auth_name, base64_part = authorization_header.split()
            if auth_name != 'Basic':
                return

            return base64_part
        except ValueError:  # String doesn't have space after auth_name
            return

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ Returns the decoded value of a Base64 string

        Args:
            base64_authorization_header(str): Base64 auth header string to be
                decoded.
        """
        if not base64_authorization_header:
            return

        if not isinstance(base64_authorization_header, str):
            return

        try:
            decoded_auth_header = base64.b64decode(base64_authorization_header,
                                                   validate=True)
            return decoded_auth_header.decode('utf-8')
        except Exception:  # If invalid base64 encoded bytes
            return

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """ Returns user email and password from a Base64 decoded value

        Args:
            decoded_base64_authorization_header (str): Base64 decoded value

        Returns:
            (tuple[str, str]): User email and password
        """
        if not decoded_base64_authorization_header:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        try:
            email, password = decoded_base64_authorization_header.split(':')
            return email, password
        except Exception:
            return None, None

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password

        Args:
            user_email (str): User email
            user_pwd (str): User password

        Returns:
            (obj): User object
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return
        if not DATA:
            return

        try:
            users = User.search({"email": user_email})
            # Assume emails are unique, we ar extracting the first match
            user = users[0]
            if user.is_valid_password(user_pwd):
                return user
        except Exception:
            return
        return
