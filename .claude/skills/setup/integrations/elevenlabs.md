# ElevenLabs Audio Integration

Generate native-speaker audio pronunciation for every flashcard using ElevenLabs MCP.

## What It Does

When enabled, the card creation workflow will:

1. Generate an audio file for each word/phrase using ElevenLabs TTS
2. Generate an audio file for each example sentence
3. Store the audio files in Anki and link them to the card's audio fields

## Prerequisites

- An [ElevenLabs](https://elevenlabs.io) account (free tier gives 10k credits/month)
- `uv` installed (provides `uvx` for running the MCP server)

## Setup Steps

### 1. Check if ElevenLabs MCP is already configured

Use `ToolSearch` to check if any `elevenlabs` tools are available. If tools are found, the MCP server is already configured — skip to **Voice Selection**.

**If not configured**, walk the user through these steps:

#### a. Install uv (if not already installed)

Check if `uvx` is available:

```bash
which uvx
```

If not found, install it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> **Note:** `uv` is a fast Python package runner. `uvx` (included with `uv`) lets Claude Code run the ElevenLabs MCP server without any global pip installs. This is NOT the same as installing the ElevenLabs MCP in Claude Desktop — that config is separate and not needed here.

#### b. Get an ElevenLabs API key

Direct the user to https://elevenlabs.io/app/settings/api-keys (free tier works).

#### c. Add the MCP server to Claude Code

Run this command (replacing the API key):

```bash
claude mcp add elevenlabs-mcp -s user -e ELEVENLABS_API_KEY=YOUR_API_KEY -- uvx elevenlabs-mcp
```

- `-s user` makes it available across all projects
- `-e` passes the API key as an environment variable (not a CLI flag)
- The `-- uvx elevenlabs-mcp` part tells Claude Code how to launch the server

#### d. Restart Claude Code

The user must exit and relaunch Claude Code for the new MCP server to connect. Then re-run `/setup` to continue configuration.

Let the user know they can finish this later and re-run `/setup` at any point.

### 2. Voice Selection

Ask the user:

- **What voice would you like to use?** — They can browse voices at https://elevenlabs.io/app/voice-library
- They should provide the voice URL or name
- If they're unsure, suggest they pick a native speaker voice for their target language

### 3. TTS Preferences

Ask for (with suggested defaults):

- **Language code** — e.g., `vi` for Vietnamese, `es` for Spanish, `ja` for Japanese, `ko` for Korean (should be derived from their target language in USER.md)
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
  - Output directory: ./audio (within repo)
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
