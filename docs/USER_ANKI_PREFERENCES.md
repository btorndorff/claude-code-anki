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

# Flashcard Format: Language Learning Model

The standard card format for all language learning is the **Language Learning** model with 6 fields:

1. **Learning Language** - Word/phrase in target language
2. **Native Language** - Translation in native language
3. **Example (Learning)** - Example sentence in target language
4. **Example (Native)** - Example sentence in native language
5. **Audio Word** - Audio file for the word (e.g., `[sound:filename.mp3]`)
6. **Audio Sentence** - Audio file for the example sentence (e.g., `[sound:filename.mp3]`)

# Card Templates

Currently configured with 1 main template. Additional templates can be added for:

- Audio-only practice (audio → translation)
- Sentence practice (sentence → translation)
- Reverse practice (native → learning language)
