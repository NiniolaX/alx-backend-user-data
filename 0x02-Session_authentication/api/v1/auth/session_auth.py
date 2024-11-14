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
            user_id: User ID

        Returns:
            (str): Newly created session's ID
        """
        if not isinstance(user_id, str):
            return

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
