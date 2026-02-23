---
name: setup
description: First-time setup wizard and integration manager. Run /setup after cloning to configure your language, deck, and card model. Run /setup again later to add optional integrations.
allowed-tools: Bash, Read, Write, Edit
---

# Setup

This skill handles both first-time setup and adding optional integrations later.

## Determine What To Do

1. Read `USER.md` and check if the target language is still `(not configured - run /setup)`
2. **If not configured** → This is a first-time setup. Follow [first-time-setup.md](first-time-setup.md)
3. **If already configured** → The user wants to add or reconfigure an integration. Present the available integrations below and ask which one they'd like to set up. Also offer to re-run the full first-time setup if they want to reconfigure from scratch.

## Available Integrations

Each integration has its own guide in the `integrations/` directory:

| Integration      | File                                                     | Description                                                |
| ---------------- | -------------------------------------------------------- | ---------------------------------------------------------- |
| ElevenLabs Audio | [integrations/elevenlabs.md](integrations/elevenlabs.md) | Generate native-speaker audio pronunciation for flashcards |

<!-- To add a new integration: create a new .md file in integrations/ following the same pattern as elevenlabs.md, then add a row to this table. -->
