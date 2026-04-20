# First-Time Setup Guide

Walk the user through initial configuration. Follow these phases in order. Use `AskUserQuestion` to batch related questions when possible. Keep tone friendly and jargon-light — the user is learning a language, not a programming language.

**Before this guide runs**, [preflight.md](preflight.md) must have passed. Don't repeat those checks here.

---

## Resuming from partial setup

Before Phase 1, check whether the user previously got partway through. Read `USER.md` and compare:

| Signal | Interpretation | What to do |
| --- | --- | --- |
| Target language is still `(not configured - run /setup)` | Totally fresh | Start at Phase 1. |
| Target language is set, but deck name is `(not configured)` | Partial — stopped in Phase 2 | Ask: "Looks like we got as far as your language ([target language]). Want to pick up from the deck setup, or start over?" |
| Deck + model are set, but no card-creation preferences | Partial — stopped in Phase 3 | Ask: "Looks like we got as far as the deck. Want to finish setting preferences, or start over?" |
| Everything set except Audio | Partial — stopped in Phase 4 | Skip to Phase 4 (integrations). |

If the user wants to resume, jump directly to the next incomplete phase and keep the values already in `USER.md`. If they want to start over, reset `USER.md` to the default template (or overwrite field-by-field as you go).

**Checkpoint rule:** After each phase below succeeds, immediately update `USER.md` with whatever's been confirmed so far. This way, if the user quits or Claude crashes mid-wizard, re-entering `/setup` can resume cleanly.

---

## Phase 1: Language

Ask the user these questions (use `AskUserQuestion` to batch the first three):

1. **What language are you learning?** (e.g., Vietnamese, Spanish, Japanese, Korean)
2. **Any specific dialect or variant?** (e.g., Northern Vietnamese, Latin American Spanish, Kansai Japanese) — optional, default "none"
3. **What is your native language?** (e.g., English)

### Checkpoint after Phase 1

Write these three values into `USER.md` under `## Language` before continuing. If they quit here, resuming is safe.

---

## Phase 2: Deck & Card Model

### 2a. Name the deck

Ask: **What would you like to name your Anki deck?** Suggest the target language as the default (e.g., "Spanish").

### 2b. Create new or connect to existing?

Use `AskUserQuestion`:

- **Create the default "Language Learning" setup (recommended)** — we create the deck + a 6-field card model automatically. Best for new users.
- **Use a deck/model I already have in Anki** — for users who already have their own setup.

### If creating default setup:

Create the deck:

```bash
curl -s --max-time 5 localhost:8765 -X POST -d '{"action": "createDeck", "version": 6, "params": {"deck": "DECK_NAME"}}'
```

Create the "Language Learning" model with 6 fields and a basic card template:

```bash
curl -s --max-time 5 localhost:8765 -X POST -d '{
  "action": "createModel",
  "version": 6,
  "params": {
    "modelName": "Language Learning",
    "inOrderFields": ["Learning Language", "Native language", "Example (Learning)", "Example (native)", "Audio Word", "Audio Sentence"],
    "css": ".card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; } .word { font-size: 32px; font-weight: bold; margin-bottom: 10px; } .example { font-size: 16px; color: #555; margin-top: 15px; font-style: italic; }",
    "cardTemplates": [
      {
        "Name": "Word → Translation",
        "Front": "<div class=\"word\">{{Learning Language}}</div><div>{{Audio Word}}</div><div class=\"example\">{{Example (Learning)}}</div><div>{{Audio Sentence}}</div>",
        "Back": "{{FrontSide}}<hr id=answer><div class=\"word\">{{Native language}}</div><div class=\"example\">{{Example (native)}}</div>"
      }
    ]
  }
}'
```

If either call returns an error (e.g., model already exists), report it in plain language and ask the user whether to use the existing one or pick a different name.

Record the field mappings:
- Word field: `Learning Language`
- Translation field: `Native language`
- Example (target) field: `Example (Learning)`
- Example (native) field: `Example (native)`
- Audio word field: `Audio Word`
- Audio sentence field: `Audio Sentence`

### If using existing setup:

Show available decks:

```bash
curl -s --max-time 5 localhost:8765 -X POST -d '{"action": "deckNames", "version": 6}'
```

Ask which deck to use (use `AskUserQuestion` with the actual deck names as options if the list is reasonably short).

Show available models:

```bash
curl -s --max-time 5 localhost:8765 -X POST -d '{"action": "modelNames", "version": 6}'
```

Get the chosen model's fields:

```bash
curl -s --max-time 5 localhost:8765 -X POST -d '{"action": "modelFieldNames", "version": 6, "params": {"modelName": "MODEL_NAME"}}'
```

Then ask the user to map their fields to the standard roles. Show them the actual field list for reference:

- Which field holds the **word/phrase in the target language**?
- Which field holds the **translation in the native language**?
- Which field holds the **example sentence in the target language**? (optional — say "none" to skip)
- Which field holds the **example sentence in the native language**? (optional)
- Which field holds the **word audio**? (optional)
- Which field holds the **sentence audio**? (optional)

After mapping, **confirm back to the user**: "Got it — when I make cards, I'll put the word in *[Word field name]*, the translation in *[Translation field name]*, examples in *[…]*. Ready to go?" This is the safety net against silent mis-mapping.

### Checkpoint after Phase 2

Write the deck name, model name, and all field mappings into `USER.md` before continuing.

---

## Phase 3: Card Creation Preferences

Ask the user:

1. **Do you have any default tags you'd like applied to all new cards?** (e.g., "vocabulary", a topic tag, etc.) — optional
2. **Any card creation best practices you'd like Claude to follow?** For example:
   - "Generalize related concepts into single cards using placeholders"
   - "Always include example sentences"
   - "Keep translations concise"
   - Or they can say "none for now" and add these later

Mention: "I'll also pick up on your preferences as we go and update `USER.md` automatically."

### Checkpoint after Phase 3

Write tags and best practices into `USER.md`.

---

## Phase 4: Optional Integrations

Present the available integrations from the table in [SKILL.md](SKILL.md) and ask which (if any) the user wants to set up now. They can always add these later by running `/setup` again.

For each integration the user opts into, follow the corresponding guide in `integrations/`.

---

## Phase 5: Confirm

All checkpointed writes above mean `USER.md` is already up to date. The only thing left is to confirm with the user.

1. Show a short summary: language, deck name, model name, audio on/off.
2. Suggest a test: "Try asking me to create a flashcard for a word in [target language]!"
3. Remind them they can run `/setup` again any time to add integrations, reconfigure, or diagnose issues.

---

## Reference: USER.md format

Fill in the existing template at `USER.md` (at the repo root). For reference, the expected shape is:

```markdown
# User Preferences

## Language

- **Target language:** [language]
- **Native language:** [language]
- **Dialect/variant:** [dialect or "none"]

## Anki Configuration

- **Main deck name:** [deck name]
- **Card model name:** [model name]
- **Model fields:**
  - Word field: [field name]
  - Translation field: [field name]
  - Example (target) field: [field name or "none"]
  - Example (native) field: [field name or "none"]
  - Audio word field: [field name or "none"]
  - Audio sentence field: [field name or "none"]

## Audio Configuration

- **Audio enabled:** [true/false]
- **Audio provider:** [provider or "none"]
- **Provider settings:** [see integration guide or "none"]

## Card Creation Preferences

- **Default tags:** [comma-separated tags or "none"]
- **Best practices:**
  - [practice 1]
  - [practice 2]
```

Use `Edit` to update fields incrementally (checkpointing). If an integration was configured, follow its guide's USER.md template snippet for the Audio Configuration section.
