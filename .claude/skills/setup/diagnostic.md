# Diagnostic Mode

Run this when the user picks **Diagnose** from the `/setup` menu (i.e., `USER.md` is already configured and something may be wrong). Goal: a single, friendly report the user can scan to understand what's working and what's broken — with copy-pasteable fixes for anything that's off.

The heavy lifting for Anki/AnkiConnect health already lives in [preflight.md](preflight.md). This guide adds a layer on top: verifying `USER.md` still matches reality.

---

## How to run

Run each step in order. Collect results (pass / warn / fail) and present them as a single summary at the end — don't drip them out one at a time. A scannable checklist is easier for the user than a narrative.

Use ✅ / ⚠️ / ❌ markers so the user can see at a glance.

---

## Step 1 — Preflight

Run the full preflight sequence from [preflight.md](preflight.md). If any preflight check fails, **stop and show the fix** — no point checking USER.md↔Anki alignment if Anki itself isn't reachable.

If preflight passes, record: "✅ Anki connected (AnkiConnect v[N])".

## Step 2 — Does the configured deck still exist?

Read `Main deck name` from `USER.md`. Then:

```bash
curl -s --max-time 5 localhost:8765 -X POST -d '{"action": "deckNames", "version": 6}'
```

If the name is present in the returned list: **✅ Deck "[name]" found.**

If not: **❌ Deck "[name]" from USER.md is not in Anki.** Possible causes and fixes:

- Deck was renamed in Anki → offer to update `USER.md` to match one of the existing decks (show the list).
- Deck was deleted → offer to create it: "Want me to recreate the deck '[name]' now?"
- Anki profile is different than when you set up → ask the user to switch profiles and re-run.

## Step 3 — Does the configured card model still exist?

Read `Card model name` from `USER.md`. Then:

```bash
curl -s --max-time 5 localhost:8765 -X POST -d '{"action": "modelNames", "version": 6}'
```

If present: **✅ Card model "[name]" found.**

If not: **❌ Card model "[name]" from USER.md is not in Anki.** Offer:

- Pick a different model from the list (re-map fields) → hand off to the "using existing setup" path in [first-time-setup.md](first-time-setup.md) Phase 2b.
- Recreate the default "Language Learning" model (if that's what they had).

## Step 4 — Do the configured fields still exist in that model?

Only run this if Step 3 passed. Read all field names from `USER.md` (Word, Translation, Example target, Example native, Audio word, Audio sentence — skip any that are "none"). Then:

```bash
curl -s --max-time 5 localhost:8765 -X POST -d '{"action": "modelFieldNames", "version": 6, "params": {"modelName": "MODEL_NAME"}}'
```

For each configured field, check it exists in the returned list:
- Match: **✅ Field "[role]" → "[name]".**
- Missing: **❌ Field "[role]" → "[name]" is not in the model anymore.** Offer to re-map it (show the actual field names from Anki) and save the update to `USER.md`.

## Step 5 — Audio integration (if enabled)

If `Audio enabled: true` in `USER.md`:

- Check if the configured MCP server's tools are available via `ToolSearch`. If yes: **✅ Audio provider ([name]) is connected.**
- If not: **⚠️ Audio is enabled in USER.md but the [provider] MCP doesn't appear to be loaded. You may need to restart Claude Code. If that doesn't work, re-run `/setup` → Add or reconfigure an integration.**

---

## Report format

Present findings as one compact summary, then ask what to fix. Example:

> **Diagnostic results**
>
> ✅ Anki connected (AnkiConnect v6)
> ✅ Deck "Spanish" found
> ❌ Card model "Language Learning" is no longer in Anki
> ⚠️ Audio enabled but ElevenLabs MCP not loaded (try restarting Claude Code)
>
> Two things to fix. Want me to:
> 1. Help you pick a new card model from the ones you have? (or recreate the default)
> 2. Walk you through reconnecting ElevenLabs?

Let the user pick what to tackle first. Never auto-fix anything that changes their Anki collection without asking.
