---
name: setup
description: First-time setup wizard, health check, and integration manager. Run /setup after cloning to configure your language, deck, and card model. Run /setup again later to diagnose problems, add integrations, or reconfigure.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# Setup

This skill handles first-time setup, diagnosing problems, and adding optional integrations. It always begins with a **preflight** check so the user never hits Anki errors mid-wizard.

## Step 1 — Always run preflight first

Before doing anything else, run the preflight sequence from [preflight.md](preflight.md). This confirms Anki is running, AnkiConnect is installed, and the API responds with version ≥ 6. Each check has a copy-pasteable fix and a retry affordance.

**Do not proceed past preflight until every check passes.** If the user needs time to install something, wait for them to say they're ready, then re-run preflight.

## Step 2 — Determine which path to take

After preflight passes, read `USER.md` and look at the **Target language** line:

| State of USER.md | Path |
| --- | --- |
| `Target language: (not configured - run /setup)` | **Fresh setup** — run [first-time-setup.md](first-time-setup.md) from Phase 1. |
| Partially configured (language set, but deck or fields still `(not configured)`) | **Resume** — detect the latest completed phase and continue from the next one. See [first-time-setup.md](first-time-setup.md) § Resuming. |
| Fully configured | **Ask the user what they want** — use the menu below. |

### Menu for already-configured users

Use `AskUserQuestion` with these three options:

1. **Diagnose** (recommended if something is broken) — run the diagnostic flow in [diagnostic.md](diagnostic.md). Confirms Anki/AnkiConnect still work and verifies the deck, card model, and fields in `USER.md` still exist in Anki.
2. **Add or reconfigure an integration** — show the Available Integrations table and ask which one.
3. **Reconfigure from scratch** — re-run the full first-time setup. Offer to preserve current `USER.md` values as defaults (don't silently overwrite).

## Available Integrations

Each integration has its own guide in the `integrations/` directory:

| Integration      | File                                                     | Description                                                |
| ---------------- | -------------------------------------------------------- | ---------------------------------------------------------- |
| ElevenLabs Audio | [integrations/elevenlabs.md](integrations/elevenlabs.md) | Generate native-speaker audio pronunciation for flashcards |

<!-- To add a new integration: create a new .md file in integrations/ following the same pattern as elevenlabs.md, then add a row to this table. -->

## Tone

The user is a language learner, not a developer. Keep prompts short, skip jargon, and when something fails give a copy-pasteable fix (not a link to a docs page). Always offer a "try again" after fixes — never force them to restart the whole wizard.
