#!/usr/bin/env python3
""" Manage API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ A template for all authentication system
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns False for now...
        `path` and `excluded_paths` will be used later
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns None now...
        `request` will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None for now...
        `request` will be the Flask request object
        """
        return None
