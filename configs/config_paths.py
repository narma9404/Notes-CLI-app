"""
Filesystem paths for Notes application.
"""

from pathlib import Path

# Root directory of the project
ROOT = Path(__file__).resolve().parent.parent

# User data directories
DATA_DIR = ROOT / "user_data"
CREDENTIALS_DIR = ROOT / "auth_data"
CREDENTIALS_FILE = CREDENTIALS_DIR / "credentials.csv"

# Logging directories
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "app.log"
