"""
Task management service.
"""

from pathlib import Path
from typing import List
import logging

from src.notes.utils.helpers import open_file_cross_platform

logger = logging.getLogger(__name__)


class TaskService:
    """Manage tasks stored in a single tasks.txt file inside a directory."""

    TASK_FILE_NAME = "tasks.txt"

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.task_file = self.base_dir / self.TASK_FILE_NAME
        if not self.task_file.exists():
            self.task_file.touch()

    def create_task(self, task: str) -> None:
        """Add a new unchecked task."""
        if not task.strip():
            raise ValueError("Task cannot be empty")

        with self.task_file.open("a", encoding="utf-8") as f:
            f.write(f"[ ] {task.strip()}\n")

        logger.info("Task added")

    def list_tasks(self) -> List[str]:
        """List all tasks."""
        return self.task_file.read_text(encoding="utf-8").splitlines()

    def toggle_task(self, index: int) -> None:
        """Toggle task checkbox."""
        tasks = self.list_tasks()

        if not tasks:
            raise ValueError("No tasks found")

        if index < 1 or index > len(tasks):
            raise IndexError("Invalid task number")

        line = tasks[index - 1]

        if line.startswith("[ ]"):
            tasks[index - 1] = line.replace("[ ]", "[x]", 1)
        elif line.startswith("[x]"):
            tasks[index - 1] = line.replace("[x]", "[ ]", 1)

        self.task_file.write_text("\n".join(tasks) + "\n", encoding="utf-8")

    def delete_task(self, index: int) -> None:
        """Delete a task by index."""
        tasks = self.list_tasks()

        if not tasks:
            raise ValueError("No tasks found")

        if index < 1 or index > len(tasks):
            raise IndexError("Invalid task number")

        tasks.pop(index - 1)
        self.task_file.write_text("\n".join(tasks) + "\n", encoding="utf-8")

    def open_task_file(self) -> None:
        """Open the task file in editor."""
        open_file_cross_platform(str(self.task_file))
