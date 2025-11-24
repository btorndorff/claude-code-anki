#!/usr/bin/env python3
"""
Delete notes from Anki by note ID.

Since AnkiConnect doesn't support note deletion, this script directly modifies
the Anki collection database. Anki must be closed before running this script.

Usage:
    python3 scripts/delete_notes.py 1234567890 9876543210 ...
    python3 scripts/delete_notes.py --file notes_to_delete.txt
    python3 scripts/delete_notes.py --help
"""

import argparse
import sqlite3
import subprocess
import sys
import time
from pathlib import Path


def find_collection_path():
    """Find the Anki collection.anki2 file."""
    anki_profiles = Path.home() / "Library/Application Support/Anki2"

    if not anki_profiles.exists():
        print("Error: Anki profile directory not found at:")
        print(f"  {anki_profiles}")
        sys.exit(1)

    # Find the most recently modified collection.anki2 (active profile)
    collection_files = list(anki_profiles.glob("*/collection.anki2"))
    if not collection_files:
        print("Error: No collection.anki2 found in Anki profiles")
        sys.exit(1)

    collection_path = max(collection_files, key=lambda p: p.stat().st_mtime)
    return collection_path


def check_anki_running(collection_path):
    """Check if Anki is currently running."""
    # Check if Anki process is running
    try:
        result = subprocess.run(["pgrep", "-f", "aqt.run"], capture_output=True, timeout=2)
        if result.returncode == 0:
            return True
    except Exception:
        pass

    # Also check for old-style lock file (older Anki versions)
    lock_file = collection_path.parent / "collection.anki2.lock"
    if lock_file.exists():
        return True

    return False


def delete_notes(note_ids):
    """
    Delete notes from Anki collection.

    Args:
        note_ids: List of note IDs to delete

    Returns:
        Number of notes deleted
    """
    collection_path = find_collection_path()

    # Check if Anki is running
    if check_anki_running(collection_path):
        print("⚠️  ERROR: Anki is currently running!")
        print("❌ Cannot delete notes while Anki is open (database would be corrupted)")
        print("\nPlease close Anki and try again")
        sys.exit(1)

    print(f"Using collection: {collection_path}")
    print(f"Deleting {len(note_ids)} note(s)...")

    try:
        conn = sqlite3.connect(collection_path)
        cursor = conn.cursor()

        # Delete notes by ID
        placeholders = ",".join("?" * len(note_ids))
        cursor.execute(f"DELETE FROM notes WHERE id IN ({placeholders})", note_ids)

        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()

        if deleted_count == 0:
            print("⚠ No notes were deleted (note IDs not found)")
        else:
            print(f"✓ Successfully deleted {deleted_count} note(s)")
            print("\nNote: Restart Anki to see the changes in your deck")

        return deleted_count

    except sqlite3.Error as e:
        print(f"Error: Database error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Delete notes from Anki by note ID. Anki must be closed.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/delete_notes.py 1763955179629 1763955180900
  python3 scripts/delete_notes.py --file notes_to_delete.txt
        """
    )

    parser.add_argument(
        "note_ids",
        nargs="*",
        type=int,
        help="Note IDs to delete"
    )

    parser.add_argument(
        "-f", "--file",
        help="Read note IDs from file (one ID per line)"
    )

    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Skip confirmation prompt"
    )

    args = parser.parse_args()

    # Collect note IDs from arguments and/or file
    note_ids = list(args.note_ids)

    if args.file:
        try:
            with open(args.file, "r") as f:
                file_ids = [int(line.strip()) for line in f if line.strip()]
                note_ids.extend(file_ids)
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        except ValueError as e:
            print(f"Error: Invalid note ID in file: {e}")
            sys.exit(1)

    # Require at least one note ID
    if not note_ids:
        parser.print_help()
        sys.exit(1)

    # Remove duplicates and sort
    note_ids = sorted(set(note_ids))

    # Confirmation prompt
    if not args.yes:
        print(f"About to delete {len(note_ids)} note(s):")
        for note_id in note_ids:
            print(f"  - {note_id}")
        print("\nWarning: This action cannot be undone!")
        response = input("Continue? (y/N): ")
        if response.lower() != "y":
            print("Cancelled")
            sys.exit(0)

    # Delete notes
    delete_notes(note_ids)


if __name__ == "__main__":
    main()
