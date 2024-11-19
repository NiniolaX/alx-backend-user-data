#!/usr/bin/env python3
""" Auth module

Classes:
    Auth: Class to interact with the authentication database
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """ Hashes a password

    Args:
        password (str): Password to hash

    Returns:
        (bytes): A salted hash of the input password

    Example:
        >>> hashed_pwd = _hash_password("Password")
    """
    if not password:
        return

    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hash


class Auth:
    """ Auth class to interact with the authentication database.

    Methods:
        register_user: Registers a new user
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user

        Args:
            email (str): Email
            password (str): Password

        Returns:
            User object
        """
        if not email or not password:
            raise ValueError("Email and password is required")
        if not isinstance(email, str) or not isinstance(password, str):
            raise ValueError("String arguments only")

        # Check if user already exists
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # Hash password
            hashed_password = _hash_password(password)

            # Add user to database
            user = self._db.add_user(email, hashed_password)

            return user
        except InvalidRequestError:
            raise ValueError(f"Email and password is required")