"""
Workspace menu for Notes Application.
"""

import logging
from pathlib import Path

from src.notes.session.manager import UserSession

from src.notes.cli.notebook_menu import notebook_menu
from src.notes.cli.note_menu import note_menu
from src.notes.cli.task_menu import task_menu
from src.notes.utils.helpers import safe_input

logger = logging.getLogger("notes.app")


def workspace_menu(username: str) -> None:
    """Main workspace menu loop."""
    session = UserSession(username)

    while True:
        logger.info("\n--- WORKSPACES ---")
        logger.info("1. Create workspace")
        logger.info("2. List workspaces")
        logger.info("3. Select workspace")
        logger.info("4. Delete workspace")
        logger.info("5. Logout")

        try:
            choice = int(safe_input("\nEnter choice: "))
        except ValueError:
            logger.error("Invalid input. Please enter a number.")
            continue

        # CREATE WORKSPACE
        if choice == 1:
            name = safe_input("Workspace name: ").strip()
            try:
                session.create_workspace(name)
                logger.info("Workspace created: %s", name)
            except Exception as exc:
                logger.error("Failed to create workspace: %s", exc)

        # LIST WORKSPACES
        elif choice == 2:
            workspaces = session.list_workspaces()
            if not workspaces:
                logger.info("No workspaces found")
            else:
                logger.info("Available workspaces:")
                for i, ws in enumerate(workspaces, 1):
                    logger.info("%d. %s", i, ws)

        # SELECT WORKSPACE
        elif choice == 3:
            workspaces = session.list_workspaces()
            if not workspaces:
                logger.info("No workspaces found. Create one first.")
                continue

            logger.info("Available workspaces:")
            for i, ws in enumerate(workspaces, 1):
                logger.info("%d. %s", i, ws)

            workspace_name = safe_input("Enter workspace name to select: ").strip()
            ws_path = Path(session.context.user_dir) / workspace_name
            if not ws_path.exists():
                logger.error("Workspace not found")
                continue

            # Initialize services for this workspace
            notebook_svc = session.notebook_service_for(workspace_name)
            note_svc_ws = session.note_service_for(workspace_name)
            task_svc_ws = session.task_service_for(workspace_name)

            # Workspace content menu
            while True:
                logger.info("\n--- WORKSPACE CONTENT ---")
                logger.info("1. Manage Notebooks")
                logger.info("2. Manage Notes")
                logger.info("3. Manage Tasks")
                logger.info("4. Back")

                try:
                    content_choice = int(safe_input("Enter choice: "))
                except ValueError:
                    logger.error("Invalid input. Enter a number.")
                    continue

                if content_choice == 1:
                    notebook_menu(notebook_svc)
                elif content_choice == 2:
                    note_menu(note_svc_ws)
                elif content_choice == 3:
                    task_menu(task_svc_ws)
                elif content_choice == 4:
                    break
                else:
                    logger.error("Invalid choice")

        # DELETE WORKSPACE
        elif choice == 4:
            workspaces = session.list_workspaces()
            if not workspaces:
                logger.info("No workspaces found to delete")
                continue

            logger.info("Available workspaces:")
            for i, ws in enumerate(workspaces, 1):
                logger.info("%d. %s", i, ws)

            name = safe_input("Workspace to delete: ").strip()
            try:
                session.delete_workspace(name)
                logger.info("Workspace deleted: %s", name)
            except Exception as exc:
                logger.error("Failed to delete workspace: %s", exc)

        # LOGOUT
        elif choice == 5:
            logger.info("Logged out")
            break

        else:
            logger.error("Invalid choice")
