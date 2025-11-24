# Claude Anki Scripts

This directory contains all scripts for managing Vietnamese Anki decks through the AnkiConnect API.

## Directory Structure

```
scripts/
├── README.md                          # This file
├── Permanent Scripts (for regular use)
├── tmp/                               # Temporary scripts and data files
└── (see below for specific scripts)
```

## Permanent Scripts

These scripts are production-ready and used regularly for deck management.

### tts scripts

These scripts handle generating audio files for flashcards

## Temporary Scripts & Data (scripts/tmp/)

This subdirectory contains:

- Experimental translation generators (generate\_\*.py)
- Temporary card querying scripts (query\_\*.py)
- Audit reports and data files (AUDIT\*_._, TRANSLATION\*_._, etc.)
- Temporary data exports (_.json, _.csv, \*.txt)

These files are safe to delete after project work is complete. They are kept for reference and debugging purposes.

## AnkiConnect Requirements

All scripts require:

- Anki running in the background
- AnkiConnect plugin installed
- API accessible at `http://localhost:8765`
- API version 6 compatibility

## Related Files

- `../CLAUDE.md` - Project configuration and user preferences
- `../audio/` - Audio files directory

## Notes

- Scripts maintain detailed error handling and reporting
- All API calls check for errors before processing
- Scripts are designed to be safe and non-destructive
- Temporary files are preserved for audit and debugging
