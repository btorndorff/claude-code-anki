# Claude Code Anki

**Talk to Claude. Get flashcards.** A conversational companion for Anki, built for language learners.

<!-- TODO: record a 20–30s screen capture of adding cards by conversation and drop it here as demo.gif -->
<!-- ![Demo: adding five Spanish words by chat](docs/demo.gif) -->

## See it work

```
You:    Add hola, gracias, and buenos días with example sentences.

Claude: Creating three cards in your Spanish deck…
         • hola — "Hola, ¿cómo estás?" / "Hello, how are you?"
         • gracias — "Muchas gracias por tu ayuda." / "Thanks a lot for your help."
         • buenos días — "Buenos días, señora." / "Good morning, ma'am."
        Audio generated for all three. Added to Anki. ✓

You:    Tag those as "greetings" and add a couple more: de nada, por favor.

Claude: Done. Five cards tagged "greetings".
```

That's the whole loop. No forms, no field-by-field entry. You talk, Claude handles Anki.

## Install — one paste

Have [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [Anki](https://apps.ankiweb.net/) installed? Open Claude Code and paste this:

> Clone `https://github.com/btorndorff/anki-language-learning-claude.git` into `~/anki-learning`, open it, and run `/setup`.

Claude will do the rest — including walking you through installing the AnkiConnect add-on if you don't have it yet.

**Prefer to run it yourself?**

```bash
git clone https://github.com/btorndorff/anki-language-learning-claude.git ~/anki-learning
cd ~/anki-learning
claude "/setup"
```

`claude "/setup"` opens Claude Code and runs the setup wizard in one step.

## What you can say to Claude

Once setup is done, talk to Claude in plain English. A few examples:

- "Add these words: *hola, gracias, de nada*."
- "Create cards from this list I pasted from my textbook."
- "Make a card for *levantarse* with example sentences about a morning routine."
- "Tag all cards I added today as `lesson-5`."
- "Suspend my cards about weather vocabulary."
- "How many cards are in my Spanish deck? What's my review load this week?"
- "Fix the translation on the card that's currently open in Anki — it should be 'to get up,' not 'to raise.'"

Claude can see the card you're reviewing in Anki and edit it in place. No copy-paste required.

## Prerequisites (if you don't have them yet)

1. **Anki Desktop** — https://apps.ankiweb.net/#downloads
2. **AnkiConnect add-on** — in Anki: *Tools → Add-ons → Get Add-ons → paste code `2055492159` → Restart Anki*
3. **Claude Code** — https://docs.anthropic.com/en/docs/claude-code

Don't worry about getting AnkiConnect right now — `/setup` will check for it and walk you through if it's missing.

## Making it yours

This is a **template**, not a black box. Everything Claude knows about your setup lives in plain Markdown files you can read and edit:

- **`USER.md`** — your target language, deck name, field mappings, and card-creation preferences. Claude updates this automatically as you mention new preferences, but you can also edit it directly.
- **`CLAUDE.md`** — how Claude approaches Anki. Add your own rules here (e.g., "always include IPA pronunciation," "prefer shorter example sentences").
- **`.claude/settings.json`** — which shell commands Claude is allowed to run without asking. For personal tweaks that shouldn't be shared, use `.claude/settings.local.json` — it's gitignored.

Re-run `/setup` any time to reconfigure, add an integration, or run a health check if something seems off.

## Optional: audio pronunciation

If you'd like native-speaker audio on every card, `/setup` can configure [ElevenLabs](https://elevenlabs.io) (free tier works). You can skip this during setup and add it later — just run `/setup` again.

## What's included

```
├── README.md                         # You are here
├── CLAUDE.md                         # How Claude approaches Anki
├── USER.md                           # Your language + deck preferences
├── .claude/
│   ├── settings.json                 # Permissions + hooks
│   ├── hooks/current-card.sh         # Lets Claude see the card you're reviewing
│   └── skills/
│       ├── setup/                    # The /setup wizard (and its diagnostics)
│       └── anki-connect/             # How Claude talks to AnkiConnect
└── .gitignore
```

## Available commands

| Command         | What it does                                                                  |
| --------------- | ----------------------------------------------------------------------------- |
| `/setup`        | First-time setup. Run again later to add integrations, reconfigure, or diagnose issues. |
| `/anki-connect` | Open Claude's reference for the AnkiConnect API (usually invoked automatically). |

## Troubleshooting

- **"Claude can't connect to Anki."** Make sure Anki Desktop is actually running and AnkiConnect is installed. Run `/setup` and pick **Diagnose** — it will tell you exactly what's wrong.
- **Cards aren't landing in the right deck.** Your deck or card-model name in `USER.md` may have drifted from Anki. Re-run `/setup` → **Diagnose**, or edit `USER.md` directly.
- **Audio isn't working.** Re-run `/setup` and pick ElevenLabs. Make sure you restarted Claude Code after adding the MCP server.

## Contributing

Issues and PRs welcome. This is designed to be forked — if you build a nicer version for your own language or study style, share it.

## License

MIT
