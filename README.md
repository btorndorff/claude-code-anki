# Claude Code Anki

A Claude Code project template for managing Anki language learning decks.

## Prerequisites

1. [Anki Desktop](https://apps.ankiweb.net/#downloads)
2. [AnkiConnect](https://ankiweb.net/shared/info/2055492159) plugin (addon code: `2055492159`)
3. [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI

## Quick Start

```bash
git clone https://github.com/btorndorff/anki-language-learning-claude.git
cd anki-language-learning-claude
claude
```

Then run `/setup` inside Claude Code. The wizard will:

1. Verify Anki and AnkiConnect are running
2. Ask about your target language and preferences
3. Create your deck and card model (or connect to an existing one)
4. Optionally configure audio pronunciation (ElevenLabs)
5. Save everything to `USER.md`

After setup, just start talking to Claude:

- "Add these words: hello, goodbye, thank you"
- "Create cards from this vocabulary list"
- "Show me my deck stats"
- "Tag all cards added today as 'lesson-5'"
- "Suspend all my cards about weather"

## What's Included

```
├── CLAUDE.md                          # Framework instructions for Claude
├── USER.md                            # Your preferences
├── README.md                          # This file
├── .claude/
│   ├── settings.json                  # Permissions & hooks
│   ├── hooks/
│   │   └── current-card.sh            # Injects current card into context
│   └── skills/
│       ├── anki-connect/              # How to interact with anki via anki connect
│       └── setup/                     # first time setup and integration setup
└── .gitignore
```

## Available Commands

| Command         | Description                                                       |
| --------------- | ----------------------------------------------------------------- |
| `/setup`        | First-time configuration and integration setup                    |
| `/anki-connect` | Interact with Anki (create cards, query decks, manage tags, etc.) |

## Customization

Your preferences live in `USER.md`. Claude updates this file automatically as you mention preferences. You can also edit it directly or re-run `/setup` to reconfigure.

For personal Claude Code settings that shouldn't be shared (API keys, local overrides), create `.claude/settings.local.json` — it's gitignored.

## Contributing

Contributions welcome! Feel free to open issues or PRs to improve the template.

## License

MIT
