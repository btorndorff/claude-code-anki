# ElevenLabs Audio Integration

Generate native-speaker audio pronunciation for every flashcard using ElevenLabs MCP.

## What It Does

When enabled, the card creation workflow will:

1. Generate an audio file for each word/phrase using ElevenLabs TTS
2. Generate an audio file for each example sentence
3. Store the audio files in Anki and link them to the card's audio fields

## Prerequisites

- An [ElevenLabs](https://elevenlabs.io) account (free tier works for limited usage)
- The ElevenLabs MCP server added to Claude Code

## Setup Steps

### 1. Check if ElevenLabs MCP is already configured

Check if the ElevenLabs MCP server has already been set up in Claude Code.

**If not configured**, guide them:

- Offical ElevenLabs MCP Read Me: https://github.com/elevenlabs/elevenlabs-mcp/blob/main/README.md
- Get your API key from https://elevenlabs.io/app/settings/api-keys. There is a free tier with 10k credits per month.
- Let them know they can finish this setup later and re-run `/setup` to configure audio

**If already configured**, proceed to voice selection.

### 2. Voice Selection

Ask the user:

- **What voice would you like to use?** — They can browse voices at https://elevenlabs.io/app/voice-library
- They should provide the voice url
- If they're unsure, suggest they pick a native speaker voice for their target language

### 3. TTS Preferences

Ask for (with suggested defaults):

- **Language code** — e.g., `vi` for Vietnamese, `es` for Spanish, `ja` for Japanese, `ko` for Korean (should be derived from there target language in USER.md)
- **Speed** — suggest `0.9` (slightly slower is helpful for language learning)
- **Stability** — suggest `0.75` (consistent pronunciation)

## USER.md Template

When this integration is configured, update the Audio Configuration section of USER.md with:

```markdown
## Audio Configuration

- **Audio enabled:** true
- **Audio provider:** ElevenLabs
- **Provider settings:**
  - Voice: [voice name] (ID: [voice_id])
  - Language code: [code]
  - Speed: [value]
  - Stability: [value]
  - Output directory: ./audio
```

## How Audio Works in the Card Creation Workflow

When CLAUDE.md's card creation workflow reaches the audio step and audio is enabled:

1. Use the ElevenLabs MCP `text_to_speech` tool with:
   - `voice_id`: from USER.md provider settings
   - `text`: the word or sentence to generate audio for
   - `language`: from USER.md provider settings
   - `stability`: from USER.md provider settings
   - `speed`: from USER.md provider settings
   - `output_directory`: `./audio`

2. Rename the generated files to descriptive names:
   - Word audio: `word_name.mp3`
   - Sentence audio: `word_name_sentence.mp3`

3. Store in Anki via `storeMediaFile` and reference as `[sound:filename.mp3]` in the audio fields
