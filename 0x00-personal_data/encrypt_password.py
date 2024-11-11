#!/usr/bin/env python3
""" Manages password encryption

Functions:
    hash_password: Hashes a given password using bcrypt
    is_valid: Validates that a provided password matches a given hashed
              password
"""
from bcrypt import checkpw, hashpw, gensalt


def hash_password(password: str) -> bytes:
    """ Hashes a given password
    Args:
        password(str): Password to hash
    Returns:
        (bytes): Salted hashed password
    """
    if not password:
        return b""
    salt = gensalt()
    return hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validates that a provided password matches a given hased password

    Args:
        hashed_password(bytes): Hashed password
        password(str): Password to validate

    Returns:
        (bool): True if hash matches password, otherwise, False
    """
    if not hashed_password or not password:
        return False
    return checkpw(password.encode('utf-8'), hashed_password)
