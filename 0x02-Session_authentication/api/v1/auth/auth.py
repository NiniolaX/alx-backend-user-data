#!/usr/bin/env python3
"""
Manages API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """ Template for API authentication system """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required for a given path.

        Compares a path with a list of paths which are excluded from
        authentication.
        - If `path` is present in `excluded_paths`, False is returned
        indicating that path is excluded.
        - If `path` is not present in `excluded_paths`, True is
        returned indicating that path is not excluded from auth.

        Args:
            path(str): Path to validate
            excluded_paths(list of str): Paths excluded from authentication

        Return:
            (bool): True if authentication is required, otherwise, False.
        """
        if not path or not excluded_paths:
            return True
        if len(excluded_paths) == 0:
            return True

        # Normalized path
        normalized_path = path.rstrip('/')
        for exluded_path in excluded_paths:
            # Check if the normalized path matches the excluded path
            if exluded_path.rstrip('/') == normalized_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Retrieve authorization header from request

        Args:
            request: Request object

        Return:
            (str): Authorization header
        """
        if not request:
            return

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves current user from request

        Args:
            request: Request object

        Returns:
            (obj): User object
        """
        return
