"""
Shared utilities for Text-to-Speech generation scripts.
Handles Anki integration and common TTS operations.
"""

import base64
import json
import subprocess
import sys
from pathlib import Path


def store_in_anki(audio_file: str) -> str:
    """
    Store audio file in Anki's media collection.

    Args:
        audio_file: Path to audio file to store

    Returns:
        Filename as stored in Anki

    Raises:
        SystemExit: If file not found, Anki not running, or storage fails
    """
    audio_path = Path(audio_file)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_file}")
        sys.exit(1)

    # Read file and convert to base64
    with open(audio_path, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode()

    print(f"Storing {audio_path.name} in Anki...")

    try:
        response = subprocess.run(
            [
                "curl", "-X", "POST", "http://localhost:8765",
                "-H", "Content-Type: application/json",
                "-d", json.dumps({
                    "action": "storeMediaFile",
                    "version": 6,
                    "params": {
                        "filename": audio_path.name,
                        "data": audio_data
                    }
                })
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        result = json.loads(response.stdout)
        if result.get("error"):
            print(f"Error: {result['error']}")
            sys.exit(1)

        print(f"✓ Stored in Anki: {result['result']}")
        return result['result']

    except json.JSONDecodeError:
        print(f"Error: Invalid response from Anki. Is Anki running?")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: Anki connection timeout. Is Anki running?")
        sys.exit(1)


def sanitize_filename(text: str, max_length: int = 30) -> str:
    """
    Sanitize text to create a valid filename.

    Args:
        text: Text to sanitize
        max_length: Maximum length of filename (before extension)

    Returns:
        Sanitized filename-safe string
    """
    safe_text = "".join(c if c.isalnum() or c in (" ", "-") else "" for c in text[:max_length])
    return safe_text.strip().replace(" ", "_")
