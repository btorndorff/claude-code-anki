#!/usr/bin/env python3
"""
Create flashcards in Anki using AnkiConnect.

Usage:
    python3 scripts/create_cards.py --file cards.json
    python3 scripts/create_cards.py --help
"""

import argparse
import base64
import json
import sys
import requests
import re
from pathlib import Path


ANKI_URL = "http://localhost:8765"
API_VERSION = 6


def store_audio_file(filename):
    """
    Store an audio file in Anki's media collection.

    Args:
        filename: Path to audio file

    Returns:
        True if successful, False otherwise
    """
    audio_path = Path(filename)

    if not audio_path.exists():
        print(f"  ⚠ Audio file not found: {filename}")
        return False

    try:
        with open(audio_path, "rb") as f:
            audio_data = base64.b64encode(f.read()).decode()

        payload = {
            "action": "storeMediaFile",
            "version": API_VERSION,
            "params": {
                "filename": audio_path.name,
                "data": audio_data
            }
        }

        response = requests.post(ANKI_URL, json=payload, timeout=10)
        result = response.json()

        if result.get("error"):
            print(f"  ✗ Error storing {audio_path.name}: {result['error']}")
            return False

        return True
    except Exception as e:
        print(f"  ✗ Error storing {audio_path.name}: {e}")
        return False


def extract_audio_filenames(cards_data):
    """
    Extract all audio filenames from card fields.

    Returns:
        Set of unique audio filenames referenced in [sound:...] syntax
    """
    audio_files = set()
    sound_pattern = r'\[sound:([^\]]+)\]'

    for card in cards_data:
        fields = card.get("fields", {})
        for field_value in fields.values():
            if isinstance(field_value, str):
                matches = re.findall(sound_pattern, field_value)
                audio_files.update(matches)

    return audio_files


def create_cards(cards_data):
    """
    Create flashcards in Anki via AnkiConnect.

    Args:
        cards_data: List of card dictionaries with fields

    Returns:
        Tuple of (created_count, failed_count)
    """
    created_count = 0
    failed_count = 0

    for card in cards_data:
        payload = {
            "action": "addNote",
            "version": API_VERSION,
            "params": {
                "note": {
                    "deckName": card.get("deckName", "Vietnamese"),
                    "modelName": card.get("modelName", "Language Learning"),
                    "fields": card.get("fields", {}),
                    "tags": card.get("tags", [])
                }
            }
        }

        try:
            response = requests.post(ANKI_URL, json=payload, timeout=10)
            result = response.json()

            learning_lang = card.get("fields", {}).get("Learning Language", "Unknown")

            if result.get("error"):
                print(f"✗ {learning_lang}: {result['error']}")
                failed_count += 1
            else:
                print(f"✓ {learning_lang}")
                created_count += 1
        except Exception as e:
            learning_lang = card.get("fields", {}).get("Learning Language", "Unknown")
            print(f"✗ {learning_lang}: {e}")
            failed_count += 1

    return created_count, failed_count


def main():
    parser = argparse.ArgumentParser(
        description="Create flashcards in Anki deck",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example cards.json format:
[
  {
    "deckName": "Vietnamese",
    "modelName": "Language Learning",
    "fields": {
      "Learning Language": "lắm",
      "Native language": "very, extremely",
      "Example (Learning)": "Cái này khó lắm.",
      "Example (native)": "This is very difficult.",
      "Audio Word": "[sound:lam.mp3]",
      "Audio Sentence": "[sound:cai_nay_kho_lam.mp3]"
    },
    "tags": ["vocabulary", "modifiers"]
  }
]
        """
    )

    parser.add_argument(
        "-f", "--file",
        required=True,
        help="JSON file containing card data"
    )

    args = parser.parse_args()

    # Load cards from file
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            cards_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)

    # Ensure cards_data is a list
    if not isinstance(cards_data, list):
        cards_data = [cards_data]

    print(f"Creating {len(cards_data)} card(s)...")
    print()

    # Extract and store audio files first
    audio_files = extract_audio_filenames(cards_data)
    if audio_files:
        print("Storing audio files...")
        stored_count = 0
        for audio_file in sorted(audio_files):
            audio_path = Path("audio") / audio_file
            if store_audio_file(audio_path):
                stored_count += 1
        print(f"✓ {stored_count}/{len(audio_files)} audio files stored")
        print()

    created, failed = create_cards(cards_data)

    print()
    print(f"Summary: {created} created, {failed} failed")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
