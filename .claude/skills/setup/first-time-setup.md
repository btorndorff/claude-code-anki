# First-Time Setup Guide

Walk the user through initial configuration. Follow these phases in order. Use `AskUserQuestion` to batch related questions together when possible.

## Phase 1: Prerequisites Check

Check if Anki and AnkiConnect are running:

```bash
curl -s localhost:8765 -X POST -d '{"action": "version", "version": 6}' 2>/dev/null
```

**If the connection fails**, tell the user:

1. **Install Anki Desktop** (if not installed): https://apps.ankiweb.net/#downloads
2. **Install AnkiConnect plugin**: Open Anki → Tools → Add-ons → Get Add-ons → Enter code: `2055492159`
3. **Restart Anki** after installing AnkiConnect
4. AnkiConnect docs: https://ankiweb.net/shared/info/2055492159

Ask the user to complete these steps, then re-check the connection. Do not proceed until the connection succeeds.

**If the connection succeeds**, confirm it and show the AnkiConnect version. Then proceed.

## Phase 2: Language & Deck Configuration

Ask the user these questions:

1. **What language are you learning?** (e.g., Vietnamese, Spanish, Japanese, Korean)
2. **Any specific dialect or variant?** (e.g., Northern Vietnamese, Latin American Spanish, Kansai Japanese) — optional, can be "none"
3. **What is your native language?** (e.g., English)
4. **What would you like to name your Anki deck?** — suggest using the target language name (e.g., "Vietnamese", "Spanish")

Then ask:

5. **Do you already have a deck and card model set up in Anki, or should we create the default "Language Learning" setup?**
   - Option A: **Create default setup** — We'll create the deck and the 6-field "Language Learning" card model automatically
   - Option B: **Use existing** — They already have a deck and model they want to use

### If creating default setup (Option A):

Create the deck:

```bash
curl -s localhost:8765 -X POST -d '{"action": "createDeck", "version": 6, "params": {"deck": "DECK_NAME"}}'
```

Create the "Language Learning" model with 6 fields and a basic card template:

```bash
curl -s localhost:8765 -X POST -d '{
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

Record the field mappings:
- Word field: `Learning Language`
- Translation field: `Native language`
- Example (target) field: `Example (Learning)`
- Example (native) field: `Example (native)`
- Audio word field: `Audio Word`
- Audio sentence field: `Audio Sentence`

### If using existing setup (Option B):

Ask which deck to use. Show available decks:

```bash
curl -s localhost:8765 -X POST -d '{"action": "deckNames", "version": 6}'
```

Ask which model to use. Show available models:

```bash
curl -s localhost:8765 -X POST -d '{"action": "modelNames", "version": 6}'
```

Get the model's fields:

```bash
curl -s localhost:8765 -X POST -d '{"action": "modelFieldNames", "version": 6, "params": {"modelName": "MODEL_NAME"}}'
```

Then ask the user to map their fields to the standard roles:
- Which field holds the **word/phrase in the target language**?
- Which field holds the **translation in the native language**?
- Which field holds the **example sentence in the target language**? (optional)
- Which field holds the **example sentence in the native language**? (optional)
- Which field holds the **word audio**? (optional)
- Which field holds the **sentence audio**? (optional)

## Phase 3: Preferences

Ask the user:

1. **Do you have any default tags you'd like applied to all new cards?** (e.g., "vocabulary", a topic tag, etc.) — optional
2. **Any card creation best practices you'd like Claude to follow?** For example:
   - "Generalize related concepts into single cards using placeholders"
   - "Always include example sentences"
   - "Keep translations concise"
   - Or they can say "none for now" and add these later

Let them know Claude will also learn their preferences over time and update USER.md as they mention new ones.

## Phase 4: Optional Integrations

Present the available integrations from the [integrations table in SKILL.md](SKILL.md) and ask which (if any) the user wants to set up now. They can always add these later by running `/setup` again.

For each integration the user opts into, follow the corresponding guide in `integrations/`.

## Phase 5: Write Configuration

Using all the information gathered, write the completed `USER.md` file. Use this format:

```markdown
# User Preferences

<!-- Configured by /setup. Claude will update this as you mention preferences. -->

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

If the user set up an integration (e.g., ElevenLabs), use the USER.md template snippet from that integration's guide for the relevant section.

After writing USER.md, confirm to the user:

1. Show a summary of their configuration
2. Suggest they try creating a test card: "Try asking me to create a flashcard for a word in [target language]!"
3. Remind them they can re-run `/setup` anytime to add integrations or reconfigure
