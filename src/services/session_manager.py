from dataclasses import dataclass
from pathlib import Path
from typing import List
import logging

from src.services.workspace_service import WorkspaceService
from src.services.notebook_service import NotebookService
from src.services.note_service import NoteService
from src.services.task_service import TaskService

from configs.paths import DATA_DIR  

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SessionContext:
    """Immutable context for a logged-in user."""

    username: str
    base_dir: Path = Path(DATA_DIR)

    @property
    def user_dir(self) -> Path:
        """Return the user's root directory (under DATA_DIR)."""
        return self.base_dir / self.username


class UserSession:
    """Session bound to an authenticated user."""
    @property
    def username(self) -> str:
        return self.context.username

    def __init__(self, username: str):
        if not username.strip():
            raise ValueError("Username must not be empty")

        self.context = SessionContext(username=username)
        self.workspace_svc = WorkspaceService(self.context.user_dir)  
        logger.info("Session started for user: %s", username)

    # Workspace operations 
    def create_workspace(self, name: str) -> Path:
        """Create a workspace for the current user."""
        return self.workspace_svc.create_workspace(name)

    def list_workspaces(self) -> List[str]:
        """List all workspaces for the current user."""
        return self.workspace_svc.list_workspaces()

    def delete_workspace(self, name: str) -> None:
        """Delete a workspace for the current user."""
        return self.workspace_svc.delete_workspace(name)

    # Services
    def notebook_service_for(self, workspace_name: str) -> NotebookService:
        workspace_path = self.context.user_dir / workspace_name
        return NotebookService(workspace_path)

    def note_service_for(self, workspace_name: str) -> NoteService:
        workspace_path = self.context.user_dir / workspace_name
        return NoteService(workspace_path)

    def task_service_for(self, workspace_name: str) -> TaskService:
        workspace_path = self.context.user_dir / workspace_name
        return TaskService(workspace_path)  

