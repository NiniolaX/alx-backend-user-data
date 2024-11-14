#!/usr/bin/env python3
"""
Handles Session Authentication
"""
import uuid
from api.v1.auth.auth import Auth


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
