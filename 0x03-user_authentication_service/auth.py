#!/usr/bin/env python3
""" Auth module

Classes:
    Auth: Class to interact with the authentication database
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """ Hashes a password

    Args:
        password (str): Password to hash

    Returns:
        (bytes): A salted hash of the input password or None if no password
            was passed.

    Raises:
        None

    Example:
        >>> hashed_pwd = _hash_password("Password")
    """
    if not password:
        return

    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hash


def _generate_uuid() -> str:
    """ Returns the string representation of a new UUID

    Args:
        None

    Returns:
        (str): String representation of UUID

    Raises:
        None
    """
    return str(uuid.uuid4())


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

        Raises:
            ValueError if
                - email already exists
                - no email was passed
                - no password was passed
                - email or password is not a str

        Example:
            >>> auth = Auth()
            >>> user = auth.register_user("bob@hbtn.io", "pass1234")
            >>> print(user)
            <user.User object at 0x7fd4d0caded0>
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

    def valid_login(self, email: str, password: str) -> bool:
        """ Validates a user's credentials

        Args:
            email (str): User's email
            password (str): User's password

        Returns:
            (bool): True if valid, otherwise, False

        Raises:
            None

        Example:
            >>> auth = Auth()
            >>> auth.valid_login("bob@hbtn.io", "pass1234")
        """
        if not email or not password:
            return False

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:  # If no user is found
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """ Creates a session for a user

        Args:
            email (str): User's email

        Returns:
            (str): session ID if successful, otherwise, None

        Raises:
            None

        Example:
            >>> auth = Auth()
            >>> auth.create_session("bob@hbtn.io")
            5a006849-343e-4a48-ba4e-bbd523fcca58
        """
        if not email:
            return

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()  # Generate session ID
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:  # If no user is found or update_user fails
            return

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Returns user associated with a session ID

        Args:
            session_id (str): Session ID

        Returns:
            (obj): Corresponding user object or None is no user was found

        Raises:
            None

        Example:
            >>> auth = Auth()
            >>> user = auth.get_user_from_session_id("5a0068-***-***-***-**")
            >>> print(user)
            <user.User object at 0x7fd4d0caded0>
        """
        if not session_id:
            return

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """ Destroys as user's session

        Updates the user's session_ID argument to None

        Args:
            (user_id): User's ID

        Return:
            None

        Raises:
            None
        """
        if not user_id:
            return

        try:
            self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
            return
        except Exception:
            return

    def get_reset_password_token(self, email: str) -> str:
        """ Generates a reset password token for a user

        Args:
            email(str): User's email

        Returns:
            (str): User's reset token

        Raises:
            ValueError: If associated user is not found
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

        except Exception:  # If no user is found or update_user fails
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates a user's password

        Args:
            reset_token (str): Password reset token
            password (str): User's new password

        Returns:
            None

        Raises:
            ValueError: If reset token does not match any registered user
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
            return

        except Exception:  # If no user is found or update_user fails
            raise ValueError
