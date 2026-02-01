from pathlib import Path
import shutil
from typing import List
import logging

logger = logging.getLogger(__name__)


class WorkspaceService:
    """Manage user workspaces."""

    def __init__(self, user_dir: Path):
        self.user_dir = user_dir
        self.user_dir.mkdir(parents=True, exist_ok=True)  

    def create_workspace(self, name: str) -> Path:
        if not name.strip():
            raise ValueError("Workspace name must not be empty")
        workspace_path = self.user_dir / name.strip()
        if workspace_path.exists():
            raise FileExistsError("Workspace exists")
        workspace_path.mkdir(parents=True)
        logger.info("Workspace created: %s", workspace_path)
        return workspace_path
    
    def list_workspaces(self) -> List[str]:
        return [p.name for p in self.user_dir.iterdir() if p.is_dir()]

    def delete_workspace(self, name: str) -> None:
        workspace_path = self.user_dir / name
        if not workspace_path.exists():
            raise FileNotFoundError("Workspace not found")
        shutil.rmtree(workspace_path)
        logger.info("Workspace deleted: %s", workspace_path)    