#!/usr/bin/env python3
""" Manage API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ A template for all authentication system
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a path require authentication.

        Returns:
            True if path is None
            True if excluded_paths is None or empty
            False if path is in excluded_paths
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the value of the Authorization header
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None for now...
        `request` will be the Flask request object
        """
        return None
