## Overview

AnkiConnect is a plugin that enables external applications to communicate with Anki over a RESTful HTTP API. It runs on `http://localhost:8765` when Anki is open.

### Installation (Should already be completed)

The user has should have already installed AnkiConnect. For reference, installation involves:

1. Open Anki → Tools → Add-ons → Browse & Install
2. Enter code: **2055492159**
3. Restart Anki

### Verification

Visit `http://localhost:8765` in your browser. You should see: `AnkiConnect v.5`

## API Basics

### Request Format

All requests are HTTP POST with JSON body:

```json
{
  "action": "actionName",
  "version": 5,
  "params": {
    /* action-specific parameters */
  }
}
```

### Response Format

```json
{
  "result": /* return value or null */,
  "error": /* error message or null */
}
```

### Example with curl

```bash
curl localhost:8765 -X POST -d '{"action": "deckNames", "version": 5}'
```

## Common Operations for Language Learning

### 1. Deck Management

#### Get all decks

```json
{
  "action": "deckNames",
  "version": 5
}
```

Returns: `["Default", "Spanish", "Japanese::Vocabulary"]`

#### Get decks with IDs

```json
{
  "action": "deckNamesAndIds",
  "version": 5
}
```

Returns: `{"Default": 1, "Spanish": 1502972374573}`

#### Create/move cards to deck

```json
{
  "action": "changeDeck",
  "version": 5,
  "params": {
    "cards": [1502098034045, 1502098034048],
    "deck": "Japanese::JLPT N3"
  }
}
```

Note: This creates the deck if it doesn't exist.

#### Delete decks

```json
{
  "action": "deleteDecks",
  "version": 5,
  "params": {
    "decks": ["Japanese::JLPT N5"],
    "cardsToo": true
  }
}
```

### 2. Models (Card Types)

#### Get available models

```json
{
  "action": "modelNames",
  "version": 5
}
```

Returns: `["Basic", "Basic (and reversed card)", "Cloze"]`

#### Get model field names

```json
{
  "action": "modelFieldNames",
  "version": 5,
  "params": {
    "modelName": "Basic"
  }
}
```

Returns: `["Front", "Back"]`

### 3. Creating Notes/Cards

#### Add a single note

```json
{
  "action": "addNote",
  "version": 5,
  "params": {
    "note": {
      "deckName": "Spanish::Vocabulary",
      "modelName": "Basic",
      "fields": {
        "Front": "hola",
        "Back": "hello"
      },
      "tags": ["greetings", "common"]
    }
  }
}
```

Returns: note ID on success, `null` on failure

#### Add note with audio

```json
{
  "action": "addNote",
  "version": 5,
  "params": {
    "note": {
      "deckName": "Japanese::Vocabulary",
      "modelName": "Basic",
      "fields": {
        "Front": "猫 (ねこ)",
        "Back": "cat"
      },
      "tags": ["animals", "jlpt-n5"],
      "audio": {
        "url": "https://example.com/neko.mp3",
        "filename": "neko_猫.mp3",
        "skipHash": "7e2c2f954ef6051373ba916f000168dc",
        "fields": "Front"
      }
    }
  }
}
```

#### Add multiple notes at once

```json
{
  "action": "addNotes",
  "version": 5,
  "params": {
    "notes": [
      {
        "deckName": "Spanish::Vocabulary",
        "modelName": "Basic",
        "fields": {
          "Front": "gracias",
          "Back": "thank you"
        },
        "tags": ["common"]
      },
      {
        "deckName": "Spanish::Vocabulary",
        "modelName": "Basic",
        "fields": {
          "Front": "adiós",
          "Back": "goodbye"
        },
        "tags": ["common", "greetings"]
      }
    ]
  }
}
```

Returns: array of note IDs (null for failed notes)

#### Check if notes can be added (validate before creating)

```json
{
  "action": "canAddNotes",
  "version": 5,
  "params": {
    "notes": [
      {
        "deckName": "Spanish",
        "modelName": "Basic",
        "fields": {
          "Front": "hola",
          "Back": "hello"
        }
      }
    ]
  }
}
```

Returns: `[true]` or `[false]` for each note

### 4. Querying and Finding Notes

#### Find notes by query

```json
{
  "action": "findNotes",
  "version": 5,
  "params": {
    "query": "deck:Spanish tag:verbs"
  }
}
```

Returns: array of note IDs

Common query syntax:

- `deck:Spanish` - notes in Spanish deck
- `tag:verbs` - notes tagged with "verbs"
- `deck:Japanese::JLPT tag:n5` - combine conditions
- `deck:current` - current deck

#### Get note information

```json
{
  "action": "notesInfo",
  "version": 5,
  "params": {
    "notes": [1502298033753, 1502298033754]
  }
}
```

Returns:

```json
[
  {
    "noteId": 1502298033753,
    "modelName": "Basic",
    "tags": ["verbs", "common"],
    "fields": {
      "Front": { "value": "hablar", "order": 0 },
      "Back": { "value": "to speak", "order": 1 }
    }
  }
]
```

### 5. Updating Notes

#### Update note fields

```json
{
  "action": "updateNoteFields",
  "version": 5,
  "params": {
    "note": {
      "id": 1514547547030,
      "fields": {
        "Front": "新しい内容",
        "Back": "new content"
      }
    }
  }
}
```

#### Add tags to existing notes

```json
{
  "action": "addTags",
  "version": 5,
  "params": {
    "notes": [1483959289817, 1483959291695],
    "tags": "reviewed needs-practice"
  }
}
```

#### Remove tags from notes

```json
{
  "action": "removeTags",
  "version": 5,
  "params": {
    "notes": [1483959289817],
    "tags": "needs-practice"
  }
}
```

### 6. Tag Management

#### Get all tags

```json
{
  "action": "getTags",
  "version": 5
}
```

Returns: `["verbs", "nouns", "jlpt-n5", "common"]`

### 7. Card Operations

#### Find cards

```json
{
  "action": "findCards",
  "version": 5,
  "params": {
    "query": "deck:Spanish is:due"
  }
}
```

#### Get card information

```json
{
  "action": "cardsInfo",
  "version": 5,
  "params": {
    "cards": [1498938915662]
  }
}
```

#### Suspend/Unsuspend cards

```json
{
  "action": "suspend",
  "version": 5,
  "params": {
    "cards": [1483959291685, 1483959293217]
  }
}
```

```json
{
  "action": "unsuspend",
  "version": 5,
  "params": {
    "cards": [1483959291685]
  }
}
```

### 8. Media Files

#### Store audio/image file

```json
{
  "action": "storeMediaFile",
  "version": 5,
  "params": {
    "filename": "spanish_hola.mp3",
    "data": "SGVsbG8sIHdvcmxkIQ==" // base64 encoded
  }
}
```

Note: Prefix filename with underscore (e.g., `_config.json`) to prevent Anki from removing unused files.

#### Retrieve media file

```json
{
  "action": "retrieveMediaFile",
  "version": 5,
  "params": {
    "filename": "spanish_hola.mp3"
  }
}
```

Returns: base64-encoded file content

### Adding Audio to Flashcards: Complete Workflow

**Important:** Audio files must be stored in Anki's media collection before they can be referenced in cards. Simply having audio files in a local folder won't work.

#### Step 1: Generate audio files

**Option A: Using the eleven-labs.py script (Recommended)**

The easiest way to generate Vietnamese audio and optionally import it directly to Anki:

```bash
# Generate audio only
python3 audio/tts/eleven-labs.py "Gia đình" -o audio/gia_dinh.mp3

# Generate AND store in Anki in one command
python3 audio/tts/eleven-labs.py "Gia đình" -o audio/gia_dinh.mp3 -a
```

**Option B: Generate audio files manually**

Generate audio files using ElevenLabs API, text-to-speech service, or any other tool and save them locally.

#### Step 2: Store audio files in Anki's media collection

Convert audio file to base64 and store using `storeMediaFile`:

```python
import base64
import json
import requests

# Read audio file
with open("path/to/audio.mp3", "rb") as f:
    audio_data = base64.b64encode(f.read()).decode()

# Store in Anki
response = requests.post("http://localhost:8765", json={
    "action": "storeMediaFile",
    "version": 6,
    "params": {
        "filename": "audio.mp3",
        "data": audio_data
    }
})

print(response.json())  # Should return {"result": "audio.mp3", "error": null}
```

Or using curl:

```bash
# 1. Convert file to base64
BASE64_DATA=$(base64 < audio.mp3)

# 2. Store in Anki
curl -X POST http://localhost:8765 \
  -H "Content-Type: application/json" \
  -d "{
    \"action\": \"storeMediaFile\",
    \"version\": 6,
    \"params\": {
      \"filename\": \"audio.mp3\",
      \"data\": \"$BASE64_DATA\"
    }
  }"
```

#### Step 3: Reference audio in card fields

Use the `[sound:filename.mp3]` syntax in your note fields:

```json
{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "Vietnamese",
      "modelName": "Basic",
      "fields": {
        "Front": "gia đình [sound:gia_dinh.mp3]",
        "Back": "family\n\nExample: Gia đình tôi rất yêu thương. [sound:gia_dinh_sentence.mp3]"
      },
      "tags": ["vocabulary", "vietnamese"]
    }
  }
}
```

Or update existing notes with audio:

```json
{
  "action": "updateNoteFields",
  "version": 6,
  "params": {
    "note": {
      "id": 1763281937583,
      "fields": {
        "Front": "word [sound:word.mp3]",
        "Back": "definition [sound:example.mp3]"
      }
    }
  }
}
```

#### Quick Start Example: Vietnamese Flashcard with Audio

Here's a practical example using the `eleven-labs.py` script:

```bash
# 1. Generate audio for the word
python3 audio/tts/eleven-labs.py "gia đình" -o audio/gia_dinh.mp3 -a

# 2. Generate audio for example sentence
python3 audio/tts/eleven-labs.py "Gia đình tôi rất yêu thương." -o audio/gia_dinh_example.mp3 -a

# 3. Create flashcard with audio references
curl -X POST http://localhost:8765 \
  -H "Content-Type: application/json" \
  -d '{
    "action": "addNote",
    "version": 6,
    "params": {
      "note": {
        "deckName": "Vietnamese",
        "modelName": "Basic",
        "fields": {
          "Front": "gia đình [sound:gia_dinh.mp3]",
          "Back": "family\n\nExample: Gia đình tôi rất yêu thương. [sound:gia_dinh_example.mp3]\n(My family is very loving.)"
        },
        "tags": ["vocabulary", "vietnamese"]
      }
    }
  }'
```

#### Troubleshooting

**Audio not playing:**
- Verify files were stored using `storeMediaFile` (should return filename, not null)
- **CRITICAL:** Check that `[sound:filename.mp3]` syntax includes the `.mp3` extension
  - ❌ Wrong: `[sound:filename]`
  - ✓ Correct: `[sound:filename.mp3]`
  - This is a common mistake when programmatically building audio references
- Ensure Anki is running and the media folder is accessible
- Try restarting Anki to reload the media collection

**Files not found after storing:**
- Audio files must be stored BEFORE cards reference them
- The filename in `storeMediaFile` must exactly match the filename in `[sound:...]`

**Script errors:**
- Ensure `.env` file exists with valid `ELEVENLABS_API_KEY`
- Verify Anki is running if using `-a` flag
- Check that `elevenlabs` Python package is installed: `pip3 install elevenlabs`

**Audio file organization:**
- It's helpful to save generated audio files locally (e.g., `./audio/` folder) before importing
- After confirming audio plays in Anki, local copies can be archived or deleted

### 9. Batch Operations

#### Execute multiple actions in one request

```json
{
  "action": "multi",
  "version": 5,
  "params": {
    "actions": [
      { "action": "deckNames" },
      {
        "action": "findNotes",
        "params": { "query": "deck:current" }
      }
    ]
  }
}
```

Returns: array of results for each action

## Typical Workflows

### Workflow 1: Add a batch of vocabulary words

1. Get available decks: `deckNames`
2. Validate notes can be added: `canAddNotes`
3. Add notes: `addNotes`
4. Verify creation: `findNotes` with appropriate query

### Workflow 2: Review and update existing cards

1. Find notes by tag/deck: `findNotes`
2. Get note details: `notesInfo`
3. Update fields if needed: `updateNoteFields`
4. Update tags: `addTags` or `removeTags`

### Workflow 3: Import cards with audio (Recommended for Language Learning)

1. Generate audio files using TTS script with `-a` flag to auto-store in Anki
2. Create notes with audio references: `addNote` with `[sound:filename.mp3]` syntax
3. **Important:** Audio files must be stored BEFORE cards are created
4. Verify audio plays in Anki before moving to next batch

### Best Practices for Large Batches

**Organizing Audio Generation:**
- Group audio generation by category to track progress
- Use descriptive filenames with underscores: `word_type_word.mp3` (e.g., `dialog_vocab_thoi_gian_ranh.mp3`)
- Generate all word audio first, then all sentence audio (easier to parallelize)

**Creating Cards Efficiently:**
- Build a mapping dictionary of words to audio filenames before creating cards
- Create cards in batches by category (questions, vocabulary, etc.) for better organization
- Include appropriate tags during card creation for later filtering

**Testing:**
- Create a test card first to verify the audio workflow
- Check that audio plays and fields display correctly before bulk operations
- Use query filters to verify cards were created with correct tags/content

## Important Notes

- **Authentication**: None required (localhost only by default)
- **Network Access**: Set env var `ANKICONNECT_BIND_ADDRESS=0.0.0.0` for remote access
- **Anki Must Be Running**: The API only works when Anki is open
- **API Version**: Always use version 5 in requests
- **Duplicate Detection**: By default, AnkiConnect checks for duplicates. Use `"options": {"allowDuplicate": true}` to override
- **Deck Creation**: Using `changeDeck` or `addNote` with a non-existent deck name will create the deck automatically

## Error Handling

Always check the `error` field in responses:

```javascript
if (response.error) {
  console.error("AnkiConnect error:", response.error);
} else {
  console.log("Success:", response.result);
}
```

Common errors:

- `"unsupported action"` - Invalid action name
- `"cannot create note because it is a duplicate"` - Duplicate detection triggered
- `"model was not found: ModelName"` - Invalid model name
- Connection refused - Anki is not running or AnkiConnect not installed

## Reference Links

- Full API documentation: See `/anki-connect/README.md`
- Anki search syntax: https://docs.ankiweb.net/searching.html
