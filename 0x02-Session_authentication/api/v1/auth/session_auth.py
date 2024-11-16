#!/usr/bin/env python3
"""
Handles Session Authentication
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """ Class for session authentication """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session for a user ID

        Args:
            user_id(str): User ID

        Returns:
            (str): Newly created session's ID
        """
        if not isinstance(user_id, str):
            return

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a user ID based on a session ID

        Args:
            session_id(str): Session ID

        Returns:
            (str): User ID associated with session ID
        """
        if not isinstance(session_id, str):
            return
        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns a User instance based on a cookie value

        Args:
            request (obj): Request object

        Returns:
            (obj): User object
        """
        if not request:
            return

        session_id = self.session_cookie(request)
        if not session_id:
            return

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return

        user = User.get(user_id)

        return user

    def destroy_session(self, request=None) -> bool:
        """ Deletes user session or logs out user

        Args:
            request (obj): Request object

        Returns:
            None
        """
        if not request:
            return False

        # Check if request contains session ID
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        # Delete session ID
        self.user_id_by_session_id.pop(session_id)

        return True
