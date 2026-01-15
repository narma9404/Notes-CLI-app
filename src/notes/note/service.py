"""
Note management service.
"""

from pathlib import Path
from typing import List
import logging

from src.notes.utils.helpers import open_file_cross_platform

logger = logging.getLogger(__name__)

class NoteService:
    """Manage text notes in a directory (workspace or notebook)."""

    def __init__(self, directory: Path):
        self.directory = Path(directory)

    def _note_filename(self, title: str) -> str:
        """Generate filename from note title."""
        return f"{title.strip().replace(' ', '_')}.txt"

    def create_note(self, title: str) -> Path:
        """Create a note file open it."""
        if not title.strip():
            raise ValueError("Title must not be empty")
        path = self.directory / self._note_filename(title)
        if path.exists():
            raise FileExistsError("Note already exists")
        path.touch()
        logger.info("Note created: %s", path)
        try:
            open_file_cross_platform(str(path))
        except Exception:
            logger.exception("Failed to open note: %s", path)
        return path

    def list_notes(self) -> List[str]:
        """List note filenames in the directory."""
        return [p.name for p in self.directory.glob("*.txt")]

    def open_note(self, filename: str) -> Path:
        """Open a note file."""
        path = self.directory / filename
        if not path.exists():
            raise FileNotFoundError("Note not found")
        try:
            open_file_cross_platform(str(path))
        except Exception:
            logger.exception("Failed to open note: %s", path)
            raise
        return path

    def delete_note(self, filename: str) -> None:
        """Delete a note file."""
        path = self.directory / filename
        if not path.exists():
            raise FileNotFoundError("Note not found")
        path.unlink()
        logger.info("Note deleted: %s", path)

    def rename_note(self, old_name: str, new_title: str) -> Path:
        """Rename a note file."""
        old_path = self.directory / old_name
        if not old_path.exists():
            raise FileNotFoundError("Note not found")
        new_path = self.directory / self._note_filename(new_title)
        if new_path.exists():
            raise FileExistsError("Target note exists")
        old_path.rename(new_path)
        logger.info("Note renamed: %s -> %s", old_path, new_path)
        return new_path

    def search_notes(self, keyword: str) -> List[Path]:
        """Search notes by filename or content."""
        kw = keyword.lower().strip()
        matches = []
        for p in self.directory.rglob("*.txt"):
            try:
                if kw in p.name.lower():
                    matches.append(p)
                    continue
                content = p.read_text(encoding="utf-8", errors="ignore").lower()
                if kw in content:
                    matches.append(p)
            except Exception:
                logger.exception("Failed to read note: %s", p)
        return matches
