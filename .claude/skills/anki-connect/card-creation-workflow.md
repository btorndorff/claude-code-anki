# Card Creation Workflow

Step-by-step process for creating new flashcards. Always read `USER.md` first to get the user's deck name, model name, field mappings, and audio configuration.

## Step 0: Check for duplicates

Before creating cards, check if any words already exist in the user's deck:

```bash
for word in "word1" "word2" "word3"; do
  result=$(curl -s localhost:8765 -X POST -d "{\"action\": \"findNotes\", \"version\": 6, \"params\": {\"query\": \"deck:\\\"DECK_NAME\\\" \\\"WORD_FIELD:$word\\\"\"}}")
  count=$(echo "$result" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['result']))")
  echo "$word: $count"
done
```

Replace `DECK_NAME` and `WORD_FIELD` with the values from USER.md. If the count is non-zero, the card already exists. Skip duplicates and inform the user which words were skipped.

## Step 1: Generate audio (if configured)

**Skip this step if USER.md has `Audio enabled: false` or audio is not configured.**

Use the audio provider and settings specified in USER.md to generate two audio files per card:

- Word audio: `word_name.mp3`
- Sentence audio: `word_name_sentence.mp3`

Refer to the user's audio provider integration guide (in `.claude/skills/setup/integrations/`) for provider-specific instructions.

## Step 2: Store audio in Anki (if audio was generated)

```bash
cd audio
for file in *.mp3; do
  base64_data=$(base64 -i "$file")
  curl -s localhost:8765 -X POST -d "{\"action\": \"storeMediaFile\", \"version\": 6, \"params\": {\"filename\": \"$file\", \"data\": \"$base64_data\"}}"
done
```

## Step 3: Create cards via AnkiConnect (batch)

Use `addNotes` (plural) to create all cards in a single request. Use the deck name, model name, and field names from USER.md:

```bash
curl localhost:8765 -X POST -d '{
  "action": "addNotes",
  "version": 6,
  "params": {
    "notes": [
      {
        "deckName": "DECK_NAME",
        "modelName": "MODEL_NAME",
        "fields": {
          "WORD_FIELD": "word1",
          "TRANSLATION_FIELD": "translation1",
          "EXAMPLE_TARGET_FIELD": "example sentence in target language",
          "EXAMPLE_NATIVE_FIELD": "example sentence in native language",
          "AUDIO_WORD_FIELD": "[sound:word1.mp3]",
          "AUDIO_SENTENCE_FIELD": "[sound:word1_sentence.mp3]"
        },
        "tags": ["vocabulary"]
      }
    ]
  }
}'
```

Returns an array of note IDs (or `null` for failures). If audio is not configured, omit the audio fields. Include any default tags from USER.md.

## Step 4: Sync to AnkiWeb

```bash
curl localhost:8765 -X POST -d '{"action": "sync", "version": 6}'
```

## Step 5: Clean up

After syncing, delete any generated audio files:

```bash
rm audio/*.mp3
```
