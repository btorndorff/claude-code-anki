#!/usr/bin/env python3
"""
Fix audio references in flashcards by adding .mp3 extension
"""
import json
import urllib.request

def anki_request(action, params):
    """Send a request to AnkiConnect API"""
    request = json.dumps({
        "action": action,
        "version": 6,
        "params": params
    }).encode('utf-8')

    try:
        response = urllib.request.urlopen(
            urllib.request.Request("http://localhost:8765", request)
        )
        result = json.loads(response.read().decode('utf-8'))

        if result.get('error'):
            print(f"❌ Error: {result['error']}")
            return None
        return result.get('result')
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def fix_note_audio(note_id, note):
    """Fix audio references in a note by adding .mp3 if missing"""
    audio_word = note['fields']['Audio Word']['value']
    audio_sentence = note['fields']['Audio Sentence']['value']

    needs_fix = False

    # Fix Audio Word field
    if audio_word and '[sound:' in audio_word and not audio_word.endswith('.mp3]'):
        audio_word = audio_word.replace('[sound:', '[sound:').replace(']', '.mp3]')
        needs_fix = True

    # Fix Audio Sentence field
    if audio_sentence and '[sound:' in audio_sentence and not audio_sentence.endswith('.mp3]'):
        audio_sentence = audio_sentence.replace('[sound:', '[sound:').replace(']', '.mp3]')
        needs_fix = True

    if needs_fix:
        # Update the note
        updated_note = {
            "id": note_id,
            "fields": {
                "Learning Language": note['fields']['Learning Language']['value'],
                "Native Language": note['fields']['Native language']['value'],
                "Example (Learning)": note['fields']['Example (Learning)']['value'],
                "Example (native)": note['fields']['Example (native)']['value'],
                "Audio Word": audio_word,
                "Audio Sentence": audio_sentence
            },
            "tags": note['tags']
        }

        result = anki_request("updateNote", {"note": updated_note})
        if result:
            print(f"✓ Fixed: {note['fields']['Learning Language']['value']}")
            return True

    return False

print("Finding all notes in Vietnamese deck...")
result = anki_request("findNotes", {"query": "deck:Vietnamese"})
note_ids = result

print(f"Found {len(note_ids)} notes. Checking audio references...\n")

note_info = anki_request("notesInfo", {"notes": note_ids})
fixed_count = 0

for note in note_info:
    if fix_note_audio(note['noteId'], note):
        fixed_count += 1

print(f"\n✓ Fixed {fixed_count} cards with missing .mp3 extensions")
