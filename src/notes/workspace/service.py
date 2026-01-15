from pathlib import Path
import shutil
from typing import List
import logging

logger = logging.getLogger(__name__)


class WorkspaceService:
    """Manage user workspaces."""

    def __init__(self, user_dir: Path):
        self.user_dir = user_dir
        self.user_dir.mkdir(parents=True, exist_ok=True)  # ensure user folder exists

    def create_workspace(self, name: str) -> Path:
        if not name.strip():
            raise ValueError("Workspace name must not be empty")
        ws_path = self.user_dir / name.strip()
        if ws_path.exists():
            raise FileExistsError("Workspace exists")
        ws_path.mkdir(parents=True)
        logger.info("Workspace created: %s", ws_path)
        return ws_path

    def list_workspaces(self) -> List[str]:
        return [p.name for p in self.user_dir.iterdir() if p.is_dir()]

    def delete_workspace(self, name: str) -> None:
        ws_path = self.user_dir / name
        if not ws_path.exists():
            raise FileNotFoundError("Workspace not found")
        shutil.rmtree(ws_path)
        logger.info("Workspace deleted: %s", ws_path)
