"""
Password validation.
"""

import re

def validate_password_strength(password: str) -> bool:
    """
    Validate password strength:
    - At least 8 characters
    - At least one uppercase, one lowercase, one number
    - At least one special character [@$!%?&*^]
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[@$!%?&*^]", password):
        return False
    return True
