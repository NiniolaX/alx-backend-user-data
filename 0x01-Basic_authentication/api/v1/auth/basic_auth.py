#!/usr/bin/env python3
"""
Handles Basic Authentication
"""
from api.v1.auth.auth import Auth


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
