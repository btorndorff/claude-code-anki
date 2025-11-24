# CLAUDE.md

# Your Role

You (Claude Code) are responsible for helping manage Anki language learning decks through the AnkiConnect API. The user has already installed AnkiConnect on their machine, and Anki must be running for you to interact with it.

**Your responsibilities include:**

- Creating new flashcards from vocabulary lists, translations, or learning materials
- Organizing cards into appropriate decks and subdeck hierarchies
- Adding relevant tags for categorization (e.g., difficulty level, topic, source)
- Updating existing cards with corrections, additional context, or improved translations
- Querying and analyzing deck contents to help the user review their progress
- Managing audio files for pronunciation (especially for language learning)
- Bulk operations for efficient deck management

# Interacting with

- All API calls are HTTP POST requests to `http://localhost:8765`
- Always use version 5 in your requests
- Check the `error` field in responses to handle failures gracefully
- Anki must be running in the background for the API to work (if it is not you should ask the user to open it for you)
- Read `docs/ANKI_CONNECT.md` for full documentation on how to use ankiconnect

# Flashcard Format: Language Learning Model

The standard card format for all language learning is the **Language Learning** model with 6 fields:

1. **Learning Language** - Word/phrase in target language
2. **Native Language** - Translation in native language
3. **Example (Learning)** - Example sentence in target language
4. **Example (Native)** - Example sentence in native language
5. **Audio Word** - Audio file for the word (e.g., `[sound:filename.mp3]`)
6. **Audio Sentence** - Audio file for the example sentence (e.g., `[sound:filename.mp3]`)

### Creating New Cards

**Step 1: Generate audio**

```bash
# Generate word audio and store in Anki
python3 scripts/tts/eleven-labs.py "word" -o audio/word.mp3 -a

# Generate example sentence audio and store in Anki
python3 scripts/tts/eleven-labs.py "Example sentence here." -o audio/sentence.mp3 -a
```

**Step 2: Create card via AnkiConnect**
Use the `addNote` action with the Language Learning model:

```json
{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "Vietnamese",
      "modelName": "Language Learning",
      "fields": {
        "Learning Language": "word",
        "Native Language": "translation",
        "Example (Learning)": "Example sentence",
        "Example (Native)": "Example translation",
        "Audio Word": "[sound:word.mp3]",
        "Audio Sentence": "[sound:sentence.mp3]"
      },
      "tags": ["vocabulary"]
    }
  }
}
```

### Card Templates

Currently configured with 1 main template. Additional templates can be added for:

- Audio-only practice (audio → translation)
- Sentence practice (sentence → translation)
- Reverse practice (native → learning language)

# Generating Audio with ElevenLabs

Audio generation uses the ElevenLabs Python SDK with a dedicated script.

## Setup

ElevenLabs API key is stored in `.env`:

```bash
ELEVENLABS_API_KEY=your-api-key-here
```

## Using the Script

**File:** `scripts/tts/eleven-labs.py`

```bash
# Generate audio only
python3 scripts/tts/eleven-labs.py "Text to convert" -o audio/filename.mp3

# Generate AND automatically store in Anki (recommended)
python3 scripts/tts/eleven-labs.py "Text to convert" -o audio/filename.mp3 -a

# List available voices
python3 scripts/tts/eleven-labs.py --list-voices
```

## Script Configuration

- **Model:** `eleven_turbo_v2_5` (fast, low latency, multilingual)
- **Language Code:** Vietnamese (`vi`)
- **Default Voice:** Mai Thao (ID: `558B1EcdabtcSdleer40`)

## Important Notes

- Always use the `-a` flag to automatically store audio in Anki's media collection
- Audio filenames should be descriptive (e.g., `word.mp3`, `sentence.mp3`)
- Ensure `.env` file exists with valid `ELEVENLABS_API_KEY`
- Anki must be running when using `-a` flag

# User Preferences & Information

This is a list of what this specific user is working on and cares about in relation to anki and your work managing.

IMPORTANT: You should not expect the user to keep this up to date, you should activley add to this in CLAUDE.md as the user mention preferences

- The user is learning Vietnamese
- Uses ElevenLabs API for text-to-speech generation with Mai Thao voice
- Prefers audio files saved to `./audio` folder before importing to Anki
- Uses custom "Language Learning" model with 6 fields for all vocabulary cards
- Audio is stored in dedicated fields (`Audio Word` and `Audio Sentence`), NOT embedded in text fields
- Currently has 1 main card template; may expand to 4 templates (word, audio, sentence, reverse) in future
- Uses flexible tagging system for card organization (categories, topics, difficulty, source, etc.)
- Example tags used: `questions`, `grammar`, `dialog-vocab`, `listening-vocab`, `pronouns`, `vocabulary`

## Card Creation Best Practices

- **Generalize related concepts into single cards**: Instead of creating separate cards for variations of the same concept (e.g., anh ấy, ông ấy, cô ấy, bà ấy, em ấy), create a single card using a placeholder like `<Pronoun>` with all variations listed in the translation field. This reduces deck clutter and helps users understand relationships between similar forms.
- Example: Use `<Pronoun> ấy` with explanation "anh ấy = he | ông ấy = he (elder) | cô ấy = she..." instead of 5 separate cards
