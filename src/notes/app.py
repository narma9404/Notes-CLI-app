"""
CLI entry point for Notes Application.
"""

import logging
from src.notes.auth.service import UserService

from src.notes.utils.logger import configure_logging
from src.notes.cli.main_menu import main_menu
from src.notes.cli.workspace_menu import workspace_menu

configure_logging()
logger = logging.getLogger("notes.app")


def run() -> None:
    """Application entry point."""
    user_service = UserService()

    while True:
        try:
            choice = main_menu()

            if choice == 1:
                try:
                    user_service.signup()
                    logger.info("Signup successful")
                except Exception as exc:
                    logger.error("Signup failed: %s", exc)

            elif choice == 2:
                try:
                    username = user_service.login()
                    workspace_menu(username)  
                except Exception as exc:
                    logger.error("Login failed: %s", exc)

            elif choice == 3:
                logger.info("Exiting application")
                return

            else:
                logger.error("Invalid choice")

        except KeyboardInterrupt:
            logger.info("Interrupted. Exiting.")
            return
        except Exception:
            logger.exception("Unhandled error")
            return


if __name__ == "__main__":
    run()
