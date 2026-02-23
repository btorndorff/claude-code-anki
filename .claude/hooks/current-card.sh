#!/bin/bash
# Inject current Anki card into Claude's context on every prompt

CARD_INFO=$(curl -s localhost:8765 -X POST -d '{"action": "guiCurrentCard", "version": 6}' 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    r = d.get('result')
    if r:
        fields = r.get('fields', {})
        parts = [f'{k}: {v[\"value\"]}' for k, v in fields.items() if v.get('value')]
        print('Current Anki card: ' + ' | '.join(parts) if parts else 'Card has no content')
    else:
        print('No Anki card open')
except:
    print('Anki not running')
" 2>/dev/null)

# Output JSON with additionalContext for Claude
echo "{\"hookSpecificOutput\": {\"hookEventName\": \"UserPromptSubmit\", \"additionalContext\": \"$CARD_INFO\"}}"
exit 0
