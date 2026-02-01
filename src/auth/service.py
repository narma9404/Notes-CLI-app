"""
Authentication service.
Handles user signup and login.

CSV format:
    username,salt,password_hash

Responsibilities:
- Signup users with password validation
- Login users securely 
"""

import csv
from pathlib import Path
import secrets
import hashlib
import logging

from src.utils.helpers import safe_input
from .validator import validate_password_strength

from configs.paths import CREDENTIALS_FILE
from configs.security import PBKDF2_ITERATIONS, SALT_BYTES

logger = logging.getLogger(__name__)


class UserService:
    """
    Handles user signup and login using a CSV file.
    """

    def __init__(
        self,
        credentials_file: Path = CREDENTIALS_FILE,
        iterations: int = PBKDF2_ITERATIONS,
        salt_bytes: int = SALT_BYTES
    ):
        """
        Initialize the authentication service.

        Args:
            credentials_file: Path to the CSV file storing credentials
            iterations: PBKDF2 iteration count
            salt_bytes: Number of bytes for generated salt
        """
        self.users_file = credentials_file
        self.iterations = iterations
        self.salt_bytes = salt_bytes

        # Create CSV file with header 
        if not self.users_file.exists():
            self.users_file.parent.mkdir(parents=True, exist_ok=True)
            with self.users_file.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["username", "salt", "password_hash"])
            logger.info("Credentials file created: %s", self.users_file)

    def _hash_password(self, password: str, salt: str) -> str:
        """
        Hash password using PBKDF2-HMAC-SHA256.

        Args:
            password: Plaintext password
            salt: Salt in hex string

        Returns:
            Hexadecimal password hash
        """
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            self.iterations
        ).hex()

    def _user_exists(self, username: str) -> bool:
        """
        Check if a username already exists.

        Args:
            username: The username to check

        Returns:
            True if user exists, False otherwise
        """
        with self.users_file.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username:
                    return True
        return False

    def signup(self) -> None:
        """
        Signup a new user.

        Raises:
            ValueError: if username exists, is empty, or password is weak
        """
        username = safe_input("Enter username: ")
        password = safe_input("Enter password: ")

        if not username:
            raise ValueError("Username cannot be empty")
        if self._user_exists(username):
            raise ValueError("Username already exists")
        if not validate_password_strength(password):
            raise ValueError(
                "Password must be at least 8 characters, include uppercase, "
                "lowercase, number, and special character"
            )

        salt = secrets.token_hex(self.salt_bytes)
        pwd_hash = self._hash_password(password, salt)

        with self.users_file.open("a", newline="",) as f:
            writer = csv.writer(f)
            writer.writerow([username, salt, pwd_hash])

        logger.info("User registered: %s", username)

    def login(self) -> str:
        """
        Authenticate an existing user.

        Returns:
            The authenticated username

        Raises:
            ValueError: if username or password is invalid
        """
        username = safe_input("Enter username: ")
        password = safe_input("Enter password: ")

        with self.users_file.open(newline="",) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username:
                    expected_hash = row["password_hash"]
                    salt = row["salt"]
                    computed_hash = self._hash_password(password, salt)
                    if secrets.compare_digest(computed_hash, expected_hash):
                        logger.info("User authenticated: %s", username)
                        return username
                    break

        raise ValueError("Invalid username or password")
