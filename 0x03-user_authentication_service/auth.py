#!/usr/bin/env python3
"""Auth module for handling password hashing
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns the salted hash as bytes
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
