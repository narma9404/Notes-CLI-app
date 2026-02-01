import logging
from src.utils.helpers import safe_input

logger = logging.getLogger("notes.app")


def main_menu() -> int:
    """Main menu."""
    logger.info("\n===== NOTES APP =====")
    logger.info("1. Signup")
    logger.info("2. Login")
    logger.info("3. Exit")

    try:
        return int(safe_input("Enter choice: "))
    except ValueError:
        return 0
