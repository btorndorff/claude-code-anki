---
name: anki-connect
description: Manage Anki flashcards via AnkiConnect API. Use when user wants to create cards, query decks, manage tags, update notes, or work with their Anki collection. Requires Anki to be running with AnkiConnect plugin installed.
allowed-tools: Bash, Read, Write
argument-hint: [action] [content]
---

# AnkiConnect Skill

Interact with Anki flashcard application via the AnkiConnect REST API.

## Current Anki State

Available decks: !`curl -s localhost:8765 -X POST -d '{"action": "deckNames", "version": 6}' 2>/dev/null | grep -o '"result":\[[^]]*\]' || echo "Anki not running"`

Available models: !`curl -s localhost:8765 -X POST -d '{"action": "modelNames", "version": 6}' 2>/dev/null | grep -o '"result":\[[^]]*\]' || echo "Anki not running"`

## Prerequisites

- Anki must be running
- AnkiConnect plugin installed (addon code: 2055492159)
- API available at `http://localhost:8765`

If connection fails, user needs to start Anki application.

## Workflows

- [Card Creation Workflow](card-creation-workflow.md) — Step-by-step process for creating new flashcards (duplicate check, audio, create, sync, cleanup)

## API Request Format

All requests are HTTP POST with JSON body:

```bash
curl localhost:8765 -X POST -d '{
  "action": "actionName",
  "version": 6,
  "params": { ... }
}'
```

Response format:

```json
{
  "result": <return value or null>,
  "error": <error message or null>
}
```

Always check `error` field - if non-null, the operation failed.

---

## Core Operations

### List Decks

```bash
curl localhost:8765 -X POST -d '{"action": "deckNames", "version": 6}'
```

### List Models (Note Types)

```bash
curl localhost:8765 -X POST -d '{"action": "modelNames", "version": 6}'
```

### Get Model Fields

```bash
curl localhost:8765 -X POST -d '{
  "action": "modelFieldNames",
  "version": 6,
  "params": {"modelName": "Basic"}
}'
```

---

## Note Operations

### Create Single Note

```bash
curl localhost:8765 -X POST -d '{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "Default",
      "modelName": "Basic",
      "fields": {
        "Front": "Question",
        "Back": "Answer"
      },
      "tags": ["tag1", "tag2"]
    }
  }
}'
```

Returns note ID on success, null on failure.

### Create Multiple Notes

```bash
curl localhost:8765 -X POST -d '{
  "action": "addNotes",
  "version": 6,
  "params": {
    "notes": [
      {
        "deckName": "Default",
        "modelName": "Basic",
        "fields": {"Front": "Q1", "Back": "A1"},
        "tags": ["batch"]
      },
      {
        "deckName": "Default",
        "modelName": "Basic",
        "fields": {"Front": "Q2", "Back": "A2"},
        "tags": ["batch"]
      }
    ]
  }
}'
```

Returns array of note IDs (null for failed notes).

### Validate Before Creating

```bash
curl localhost:8765 -X POST -d '{
  "action": "canAddNotes",
  "version": 6,
  "params": {
    "notes": [
      {"deckName": "Default", "modelName": "Basic", "fields": {"Front": "Q", "Back": "A"}}
    ]
  }
}'
```

Returns array of booleans.

### Find Notes

```bash
curl localhost:8765 -X POST -d '{
  "action": "findNotes",
  "version": 6,
  "params": {"query": "deck:Default tag:verb"}
}'
```

Returns array of note IDs.

### Get Note Details

```bash
curl localhost:8765 -X POST -d '{
  "action": "notesInfo",
  "version": 6,
  "params": {"notes": [1234567890]}
}'
```

### Update Note Fields

```bash
curl localhost:8765 -X POST -d '{
  "action": "updateNoteFields",
  "version": 6,
  "params": {
    "note": {
      "id": 1234567890,
      "fields": {
        "Front": "Updated question",
        "Back": "Updated answer"
      }
    }
  }
}'
```

### Delete Notes

```bash
curl localhost:8765 -X POST -d '{
  "action": "deleteNotes",
  "version": 6,
  "params": {"notes": [1234567890, 1234567891]}
}'
```

---

## Card Operations

### Find Cards

```bash
curl localhost:8765 -X POST -d '{
  "action": "findCards",
  "version": 6,
  "params": {"query": "deck:Default is:due"}
}'
```

### Suspend/Unsuspend Cards

```bash
curl localhost:8765 -X POST -d '{
  "action": "suspend",
  "version": 6,
  "params": {"cards": [1234567890]}
}'
```

```bash
curl localhost:8765 -X POST -d '{
  "action": "unsuspend",
  "version": 6,
  "params": {"cards": [1234567890]}
}'
```

### Set Due Date

```bash
curl localhost:8765 -X POST -d '{
  "action": "setDueDate",
  "version": 6,
  "params": {"cards": [1234567890], "days": "0"}
}'
```

Days can be: "0" (today), "1" (tomorrow), "-1" (yesterday), "0!" (force today ignoring review limits).

---

## Deck Operations

### Create Deck

```bash
curl localhost:8765 -X POST -d '{
  "action": "createDeck",
  "version": 6,
  "params": {"deck": "NewDeck"}
}'
```

Use `::` for subdecks: `"Parent::Child"`.

### Move Cards to Deck

```bash
curl localhost:8765 -X POST -d '{
  "action": "changeDeck",
  "version": 6,
  "params": {"cards": [1234567890], "deck": "TargetDeck"}
}'
```

Creates deck if it doesn't exist.

### Delete Decks

```bash
curl localhost:8765 -X POST -d '{
  "action": "deleteDecks",
  "version": 6,
  "params": {"decks": ["DeckToDelete"], "cardsToo": true}
}'
```

### Get Deck Statistics

```bash
curl localhost:8765 -X POST -d '{
  "action": "getDeckStats",
  "version": 6,
  "params": {"decks": ["Default"]}
}'
```

---

## Tag Operations

### Get All Tags

```bash
curl localhost:8765 -X POST -d '{"action": "getTags", "version": 6}'
```

### Add Tags to Notes

```bash
curl localhost:8765 -X POST -d '{
  "action": "addTags",
  "version": 6,
  "params": {"notes": [1234567890], "tags": "newtag1 newtag2"}
}'
```

Tags are space-separated string.

### Remove Tags

```bash
curl localhost:8765 -X POST -d '{
  "action": "removeTags",
  "version": 6,
  "params": {"notes": [1234567890], "tags": "oldtag"}
}'
```

### Replace Tags

```bash
curl localhost:8765 -X POST -d '{
  "action": "replaceTags",
  "version": 6,
  "params": {"notes": [1234567890], "tag_to_replace": "old", "replace_with_tag": "new"}
}'
```

---

## Media Operations

### Store Media File (from base64)

```bash
curl localhost:8765 -X POST -d '{
  "action": "storeMediaFile",
  "version": 6,
  "params": {
    "filename": "audio.mp3",
    "data": "<base64-encoded-content>"
  }
}'
```

### Store Media File (from local path)

```bash
curl localhost:8765 -X POST -d '{
  "action": "storeMediaFile",
  "version": 6,
  "params": {
    "filename": "audio.mp3",
    "path": "/absolute/path/to/audio.mp3"
  }
}'
```

### Store Media File (from URL)

```bash
curl localhost:8765 -X POST -d '{
  "action": "storeMediaFile",
  "version": 6,
  "params": {
    "filename": "audio.mp3",
    "url": "https://example.com/audio.mp3"
  }
}'
```

### Reference Audio in Cards

Use `[sound:filename.mp3]` syntax in note fields:

```json
{
  "fields": {
    "Front": "Word [sound:pronunciation.mp3]",
    "Back": "Definition"
  }
}
```

---

## Batch Operations

Execute multiple actions in one request:

```bash
curl localhost:8765 -X POST -d '{
  "action": "multi",
  "version": 6,
  "params": {
    "actions": [
      {"action": "deckNames"},
      {"action": "getTags"},
      {"action": "findNotes", "params": {"query": "deck:Default"}}
    ]
  }
}'
```

---

## Search Query Syntax

Common query patterns for `findNotes` and `findCards`:

| Query                | Meaning                |
| -------------------- | ---------------------- |
| `deck:DeckName`      | Cards in specific deck |
| `deck:Parent::Child` | Cards in subdeck       |
| `tag:tagname`        | Cards with tag         |
| `-tag:tagname`       | Cards without tag      |
| `is:due`             | Due cards              |
| `is:new`             | New cards              |
| `is:suspended`       | Suspended cards        |
| `"exact phrase"`     | Exact text match       |
| `front:word`         | Field contains word    |
| `added:7`            | Added in last 7 days   |
| `rated:1`            | Reviewed today         |

Combine with spaces: `deck:Default tag:verb is:due`

---

## Error Handling

Common errors:

| Error                                          | Cause               | Solution                                  |
| ---------------------------------------------- | ------------------- | ----------------------------------------- |
| Connection refused                             | Anki not running    | Start Anki                                |
| `unsupported action`                           | Invalid action name | Check action spelling                     |
| `cannot create note because it is a duplicate` | Duplicate detection | Add `"options": {"allowDuplicate": true}` |
| `model was not found`                          | Invalid model name  | Use `modelNames` to list available models |
| `deck was not found`                           | Invalid deck name   | Use `deckNames` to list available decks   |

---

## API Reference

For complete API documentation with all 80+ actions, see [api-reference.md](api-reference.md).
