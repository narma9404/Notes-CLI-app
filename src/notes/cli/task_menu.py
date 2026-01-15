"""
Task menu CLI for Notes Application.
"""

import logging

from src.notes.utils.helpers import safe_input

logger = logging.getLogger("notes.app")


def _task_menu() -> int:
    logger.info("\n--- TASKS ---")
    logger.info("1. Create task")
    logger.info("2. List tasks")
    logger.info("3. Open task file")
    logger.info("4. Toggle task checkbox")
    logger.info("5. Delete task")
    logger.info("6. Back")
    try:
        return int(safe_input("Enter choice: "))
    except ValueError:
        return 0


def _ensure_tasks_exist(task_service) -> bool:
    tasks = task_service.list_tasks()
    if not tasks:
        logger.info("No tasks found. Create a task first.")
        return False
    return True


def task_menu(task_service):
    while True:
        choice = _task_menu()

        # Create task
        if choice == 1:
            task = safe_input("Task description: ")
            try:
                task_service.create_task(task)
            except Exception as exc:
                logger.error("Failed to create task: %s", exc)

        # List tasks
        elif choice == 2:
            tasks = task_service.list_tasks()
            if not tasks:
                logger.info("No tasks found")
            else:
                for i, t in enumerate(tasks, start=1):
                    logger.info("%d. %s", i, t)

        # Open task file
        elif choice == 3:
            try:
                task_service.open_task_file()
            except Exception as exc:
                logger.error("Failed to open task file: %s", exc)

        # Toggle task
        elif choice == 4:
            if not _ensure_tasks_exist(task_service):
                continue
            try:
                index = int(safe_input("Task number to toggle: "))
                task_service.toggle_task(index)
                logger.info("Task updated")
            except Exception as exc:
                logger.error("Failed to toggle task: %s", exc)

        # Delete task
        elif choice == 5:
            if not _ensure_tasks_exist(task_service):
                continue
            try:
                index = int(safe_input("Task number to delete: "))
                task_service.delete_task(index)
                logger.info("Task deleted")
            except Exception as exc:
                logger.error("Failed to delete task: %s", exc)

        elif choice == 6:
            break

        else:
            logger.error("Invalid choice")
