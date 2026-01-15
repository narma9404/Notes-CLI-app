"""
Notebook management service.
"""

from pathlib import Path
import shutil
from typing import List
import logging

from src.notes.note.service import NoteService
from src.notes.task.service import TaskService
from src.notes.utils.helpers import safe_input  

logger = logging.getLogger(__name__)


class NotebookService:
    """
    Manage notebooks within a workspace path.
    """

    def __init__(self, workspace_path: Path):
        self.workspace_path = Path(workspace_path)

    def create_notebook(self, name: str) -> Path:
        """Create a notebook directory."""
        if not name.strip():
            raise ValueError("Notebook name must not be empty")

        nb_path = self.workspace_path / name.strip()
        if nb_path.exists():
            raise FileExistsError("Notebook already exists")

        nb_path.mkdir(parents=True)
        logger.info("Notebook created: %s", nb_path)
        return nb_path

    def list_notebooks(self) -> List[str]:
        """List notebook directories in workspace."""
        if not self.workspace_path.exists():
            return []

        return [p.name for p in self.workspace_path.iterdir() if p.is_dir()]

    def delete_notebook(self, name: str, force: bool = False) -> None:
        """
        Delete a notebook directory.
        """
        nb_path = self.workspace_path / name

        if not nb_path.exists() or not nb_path.is_dir():
            raise FileNotFoundError("Notebook not found")

        if any(nb_path.iterdir()) and not force:
            raise ValueError("Notebook is not empty. Use force=True to delete.")

        shutil.rmtree(nb_path)
        logger.info("Notebook deleted: %s", nb_path)


    def select_notebook(self, name: str) -> Path:
        """Return notebook Path if exists."""
        nb_path = self.workspace_path / name

        if not nb_path.exists() or not nb_path.is_dir():
            raise FileNotFoundError("Notebook not found")

        return nb_path

    def note_service_for(self, notebook_name: str) -> NoteService:
        """
        Return a NoteService scoped to a notebook.
        """
        nb_path = self.select_notebook(notebook_name)
        return NoteService(nb_path)

    def task_service_for(self, notebook_name: str) -> TaskService:
        """
        Return a TaskService scoped to a notebook.
        """
        nb_path = self.select_notebook(notebook_name)
        return TaskService(nb_path)
