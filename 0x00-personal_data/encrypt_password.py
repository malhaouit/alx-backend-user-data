#!/usr/bin/env python3
"""
This module provides functionality to hash passwords
and validate them using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns
    the hashed password as a byte string."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
