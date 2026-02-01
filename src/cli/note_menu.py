"""
Note menu CLI for Notes Application.
"""
import logging

from src.utils.helpers import safe_input

logger = logging.getLogger("notes.app")


def _note_menu() -> int:
    """Display notes menu."""
    logger.info("\n--- NOTES ---")
    logger.info("1. Create note")
    logger.info("2. List notes")
    logger.info("3. Open note")
    logger.info("4. Delete note")
    logger.info("5. Rename note")
    logger.info("6. Search notes")
    logger.info("7. Back")
    try:
        return int(safe_input("Enter choice: "))
    except ValueError:
        return 0


def _ensure_notes_exist(note_service) -> bool:
    """Check whether notes exist."""
    notes = note_service.list_notes()
    if not notes:
        logger.info("No notes found. Create a note first.")
        return False
    return True


def note_menu(note_service):
    """Notes menu loop."""
    while True:
        choice = _note_menu()

        # Create note
        if choice == 1:
            title = safe_input("Note title: ")
            try:
                note_service.create_note(title)
                logger.info("Note created: %s", title)
            except Exception as exc:
                logger.error("Failed to create note: %s", exc)

        # List notes
        elif choice == 2:
            notes = note_service.list_notes()
            if not notes:
                logger.info("No notes found")
            else:
                for n in notes:
                    logger.info(n)

        # Open note
        elif choice == 3:
            if not _ensure_notes_exist(note_service):
                continue
            filename = safe_input("Open note: ")
            try:
                note_service.open_note(filename)
            except Exception as exc:
                logger.error("Failed to open note: %s", exc)

        # Delete note
        elif choice == 4:
            if not _ensure_notes_exist(note_service):
                continue
            filename = safe_input("Delete note: ")
            try:
                note_service.delete_note(filename)
                logger.info("Note deleted: %s", filename)
            except Exception as exc:
                logger.error("Failed to delete note: %s", exc)

        # Rename note
        elif choice == 5:
            if not _ensure_notes_exist(note_service):
                continue
            old_name = safe_input("Old note name: ")
            new_name = safe_input("New note title: ")
            try:
                note_service.rename_note(old_name, new_name)
                logger.info("Note renamed to: %s", new_name)
            except Exception as exc:
                logger.error("Failed to rename note: %s", exc)

        # Search notes
        elif choice == 6:
            if not _ensure_notes_exist(note_service):
                continue
            keyword = safe_input("Search keyword: ")
            results = note_service.search_notes(keyword)
            if not results:
                logger.info("No matching notes found")
            else:
                for r in results:
                    logger.info(r.name)

        elif choice == 7:
            break

        else:
            logger.error("Invalid choice")
