#!/usr/bin/env python3
"""
Manages API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """ Template for API authentication system """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authorization is required for a given path

        Args:
            path(str): Path to check
            excluded_paths(list of str): List of paths requiring authorization

        Return:
            (bool): True if authorization is required, otherwise, False.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Retrieve authorization header from request

        Args:
            request: Request object

        Return:
            (str): Authorization header
        """
        return

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves current user from request

        Args:
            request: Request object

        Returns:
            (obj): User object
        """
        return
