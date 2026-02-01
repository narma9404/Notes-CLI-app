"""
Reusable helper utilities.
"""

import os
import sys
import subprocess
import logging

logger = logging.getLogger(__name__)

def safe_input(prompt: str) -> str:
    """Read input trim spaces."""
    try:
        return input(prompt).strip()
    except EOFError:
        logger.error("Input stream closed")
        raise

def open_file_cross_platform(path: str) -> None:
    """Open a file using the default system application (silently)."""
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    try:
        if sys.platform.startswith("win"):
            os.startfile(path)

        elif sys.platform.startswith("darwin"):
            subprocess.run(
                ["open", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
            )

        else:  
            subprocess.run(
                ["xdg-open", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
            )

    except Exception:
        logger.exception("Failed to open file: %s", path)
        raise

