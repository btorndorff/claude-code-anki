#!/usr/bin/env python3
"""
ElevenLabs Text-to-Speech Generator for Anki
Generates audio files for Vietnamese language learning flashcards.
"""

import argparse
import base64
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# ElevenLabs API configuration
API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    print("Error: ELEVENLABS_API_KEY not found in .env file")
    sys.exit(1)

MODEL_ID = "eleven_turbo_v2_5"

# Available  voices
VOICES = {
    "mai-thao": "558B1EcdabtcSdleer40",
}

# Default voice
DEFAULT_VOICE = "mai-thao"


def list_voices():
    """List all available Vietnamese voices."""
    print("Available Vietnamese voices:")
    for name, voice_id in VOICES.items():
        print(f"  {name:<25} (ID: {voice_id})")


def generate_audio(text: str, voice: str = DEFAULT_VOICE, language_code: str = "vi", output_file: str = None):
    """
    Generate audio from text using ElevenLabs.

    Args:
        text: Text to convert to speech
        voice: Voice name (see VOICES dict)
        output_file: Output file path (optional, auto-generated if not provided)

    Returns:
        Path to generated audio file
    """
    if voice not in VOICES:
        print(f"Error: Voice '{voice}' not found. Available voices:")
        list_voices()
        sys.exit(1)

    client = ElevenLabs(api_key=API_KEY)
    voice_id = VOICES[voice]

    # Generate filename if not provided
    if not output_file:
        # Use sanitized text as filename
        safe_text = "".join(c if c.isalnum() or c in (" ", "-") else "" for c in text[:30])
        safe_text = safe_text.strip().replace(" ", "_")
        output_file = f"output_{safe_text}_{voice}.mp3"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating audio: {text[:50]}...")
    print(f"Voice: {voice} ({voice_id})")

    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=MODEL_ID,
            language_code=language_code
        )

        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        print(f"✓ Saved: {output_path}")
        return str(output_path)

    except Exception as e:
        print(f"Error generating audio: {e}")
        sys.exit(1)


def store_in_anki(audio_file: str):
    """
    Store audio file in Anki's media collection.

    Args:
        audio_file: Path to audio file to store
    """
    import json
    import subprocess

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


def main():
    parser = argparse.ArgumentParser(
        description="Generate Vietnamese text-to-speech audio for Anki flashcards"
    )

    parser.add_argument(
        "text",
        nargs="?",
        help="Text to convert to speech"
    )

    parser.add_argument(
        "-v", "--voice",
        default=DEFAULT_VOICE,
        help=f"Voice to use (default: {DEFAULT_VOICE}). Use --list-voices to see all options."
    )

    parser.add_argument(
        "-o", "--output",
        help="Output audio file path"
    )

    parser.add_argument(
        "-a", "--anki",
        action="store_true",
        help="Store audio in Anki's media collection after generation"
    )

    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List all available voices and exit"
    )

    args = parser.parse_args()

    # Handle list-voices flag
    if args.list_voices:
        list_voices()
        return

    # Require text argument if not listing voices
    if not args.text:
        parser.print_help()
        sys.exit(1)

    # Generate audio
    audio_file = generate_audio(args.text, args.voice, output_file=args.output)

    # Store in Anki if requested
    if args.anki:
        store_in_anki(audio_file)


if __name__ == "__main__":
    main()
