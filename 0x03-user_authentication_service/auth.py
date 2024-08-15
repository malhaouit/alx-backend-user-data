#!/usr/bin/env python3
"""Auth module for handling user authentication.
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from typing import Optional
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns the salted hash as bytes
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user if they don't already exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                    email, hashed_password.decode('utf-8'))
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                    password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a session for the user and return the session ID."""
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None


def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation"""
    return str(uuid.uuid4())
