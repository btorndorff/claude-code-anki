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

### Creating New Cards

**Step 1: Generate audio**

use the audio scripts in `scripts/tts` to generate audio for the cards

**Step 2: Create card via script**

use the `scripts/create_card.ts` to create cards

## Important Notes

- Audio filenames should be descriptive (e.g., `word.mp3`, `sentence.mp3`)
