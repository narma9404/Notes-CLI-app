"""
Workspace menu CLI for Notes Application.
"""
import logging

from src.notes.utils.helpers import safe_input
from src.notes.cli.note_menu import note_menu
from src.notes.cli.task_menu import task_menu

logger = logging.getLogger("notes.app")


def _notebook_menu() -> int:
    logger.info("\n--- NOTEBOOK ---")
    logger.info("1. Create notebook")
    logger.info("2. List notebooks")
    logger.info("3. Delete notebook")
    logger.info("4. Open notebook")
    logger.info("5. Back")
    try:
        return int(safe_input("Enter choice: "))
    except ValueError:
        return 0


def notebook_menu(notebook_svc):
    """Notebook menu loop."""
    while True:
        choice = _notebook_menu()

        # CREATE
        if choice == 1:
            name = safe_input("Notebook name: ").strip()
            try:
                notebook_svc.create_notebook(name)
                logger.info("Notebook created: %s", name)
            except Exception as exc:
                logger.error("Failed to create notebook: %s", exc)

        # LIST
        elif choice == 2:
            notebooks = notebook_svc.list_notebooks()
            if not notebooks:
                logger.info("No notebooks found")
            else:
                for nb in notebooks:
                    logger.info(nb)

        # DELETE
        elif choice == 3:
            notebooks = notebook_svc.list_notebooks()
            if not notebooks:
                logger.info("No notebooks found. Create one first.")
                continue

            logger.info("Available notebooks:")
            for nb in notebooks:
                logger.info(nb)

            name = safe_input("Notebook to delete: ").strip()
            if name not in notebooks:
                logger.error("Notebook not found")
                continue

            # Warn if notebook has content
            note_svc = notebook_svc.note_service_for(name)
            task_svc = notebook_svc.task_service_for(name)

            if note_svc.list_notes() or task_svc.list_task_files():
                confirm = safe_input(
                    "Are you sure to delete? (y/n): "
                ).lower()
                if confirm != "y":
                    logger.info("Delete cancelled")
                    continue

            try:
                notebook_svc.delete_notebook(name)
                logger.info("Notebook deleted: %s", name)
            except Exception as exc:
                logger.error("Failed to delete notebook: %s", exc)

        # OPEN
        elif choice == 4:
            notebooks = notebook_svc.list_notebooks()
            if not notebooks:
                logger.info("No notebooks found. Create one first.")
                continue

            logger.info("Available notebooks:")
            for nb in notebooks:
                logger.info(nb)

            nb_name = safe_input("Open notebook: ").strip()
            if nb_name not in notebooks:
                logger.error("Notebook not found")
                continue

            note_svc_nb = notebook_svc.note_service_for(nb_name)
            task_svc_nb = notebook_svc.task_service_for(nb_name)

            while True:
                logger.info("\n--- NOTEBOOK CONTENT ---")
                logger.info("1. Notes")
                logger.info("2. Tasks")
                logger.info("3. Back")
                try:
                    nb_choice = int(safe_input("Enter choice: "))
                except ValueError:
                    nb_choice = 0

                if nb_choice == 1:
                    note_menu(note_svc_nb)
                elif nb_choice == 2:
                    task_menu(task_svc_nb)
                elif nb_choice == 3:
                    break
                else:
                    logger.error("Invalid choice")

        elif choice == 5:
            break

        else:
            logger.error("Invalid choice")
