#!/bin/bash
# Inject current Anki card into Claude's context on every prompt

CARD_INFO=$(curl -s localhost:8765 -X POST -d '{"action": "guiCurrentCard", "version": 6}' 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    r = d.get('result')
    if r:
        word = r['fields']['Learning Language']['value']
        meaning = r['fields']['Native language']['value']
        print(f'Current Anki card: {word} = {meaning}')
    else:
        print('No Anki card open')
except:
    print('Anki not running')
" 2>/dev/null)

# Output JSON with additionalContext for Claude
echo "{\"hookSpecificOutput\": {\"hookEventName\": \"UserPromptSubmit\", \"additionalContext\": \"$CARD_INFO\"}}"
exit 0
