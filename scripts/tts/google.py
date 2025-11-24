#!/usr/bin/env python3
"""
Google Cloud Text-to-Speech Generator for Anki
Generates audio files for Vietnamese language learning flashcards.
"""

import argparse
import base64
import json
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
from lib import store_in_anki, sanitize_filename

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Google TTS API configuration
API_KEY = os.getenv("GOOGLE_TTS_API_KEY")
if not API_KEY:
    print("Error: GOOGLE_TTS_API_KEY not found in .env file")
    sys.exit(1)

# Voice configuration for Vietnamese
VOICE = {"languageCode": "vi-VN", "name": "vi-VN-Neural2-A"}
AUDIO_ENCODING = "MP3"
SPEAKING_RATE = 1.0


def generate_audio(text: str, output_file: str = None):
    """
    Generate audio from text using Google Cloud Text-to-Speech.

    Args:
        text: Text to convert to speech
        output_file: Output file path (optional, auto-generated if not provided)

    Returns:
        Path to generated audio file
    """
    # Generate filename if not provided
    if not output_file:
        safe_text = sanitize_filename(text)
        output_file = f"audio/{safe_text}.mp3"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating audio: {text[:50]}...")
    print(f"Voice: vi-VN-Neural2-A")

    try:
        url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}"

        data = {
            "audioConfig": {
                "audioEncoding": AUDIO_ENCODING,
                "pitch": 0,
                "speakingRate": SPEAKING_RATE,
            },
            "input": {"text": text},
            "voice": VOICE,
        }

        response = requests.post(
            url, headers={"Content-Type": "application/json"}, data=json.dumps(data)
        )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}, {response.text}")

        audio_content = response.json()["audioContent"]

        # Decode base64 audio content
        audio_bytes = base64.b64decode(audio_content)

        with open(output_path, "wb") as f:
            f.write(audio_bytes)

        print(f"✓ Saved: {output_path}")
        return str(output_path)

    except Exception as e:
        print(f"Error generating audio: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Vietnamese text-to-speech audio using Google Cloud TTS for Anki flashcards"
    )

    parser.add_argument(
        "text",
        nargs="?",
        help="Text to convert to speech"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output audio file path (default: audio/[text_snippet].mp3)"
    )

    parser.add_argument(
        "-a", "--anki",
        action="store_true",
        help="Store audio in Anki's media collection after generation"
    )

    args = parser.parse_args()

    # Require text argument
    if not args.text:
        parser.print_help()
        sys.exit(1)

    # Generate audio
    audio_file = generate_audio(args.text, output_file=args.output)

    # Store in Anki if requested
    if args.anki:
        store_in_anki(audio_file)


if __name__ == "__main__":
    main()
