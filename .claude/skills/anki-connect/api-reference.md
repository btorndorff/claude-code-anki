# AnkiConnect API Reference

Complete reference for all AnkiConnect API actions.

**Endpoint:** `http://localhost:8765`
**Method:** POST
**Version:** 6

---

## Note Actions

### addNote
Create a single note.
- **Params:** `note` (object with deckName, modelName, fields, tags, options, audio/video/picture)
- **Returns:** Note ID or null

### addNotes
Create multiple notes.
- **Params:** `notes` (array of note objects)
- **Returns:** Array of note IDs (null for failures)

### canAddNotes
Check if notes can be added (validates duplicates, fields).
- **Params:** `notes` (array)
- **Returns:** Array of booleans

### canAddNotesWithErrorDetail
Validate with detailed error messages.
- **Params:** `notes` (array)
- **Returns:** Array of `{canAdd, error}` objects

### updateNoteFields
Update specific fields of a note.
- **Params:** `note` (object with id, fields)
- **Returns:** null

### updateNote
Update fields and tags of a note.
- **Params:** `note` (object with id, fields, tags)
- **Returns:** null

### updateNoteModel
Change a note's model and fields.
- **Params:** `note` (object with id, modelName, fields, tags)
- **Returns:** null

### updateNoteTags
Replace all tags on a note.
- **Params:** `note` (ID), `tags` (array)
- **Returns:** null

### getNoteTags
Get tags for a note.
- **Params:** `note` (ID)
- **Returns:** Array of tags

### addTags
Add tags to notes.
- **Params:** `notes` (array of IDs), `tags` (space-separated string)
- **Returns:** null

### removeTags
Remove tags from notes.
- **Params:** `notes` (array of IDs), `tags` (space-separated string)
- **Returns:** null

### getTags
Get all tags in collection.
- **Params:** none
- **Returns:** Array of tag strings

### clearUnusedTags
Remove tags not used by any notes.
- **Params:** none
- **Returns:** null

### replaceTags
Replace a tag on specific notes.
- **Params:** `notes` (array), `tag_to_replace`, `replace_with_tag`
- **Returns:** null

### replaceTagsInAllNotes
Replace a tag across all notes.
- **Params:** `tag_to_replace`, `replace_with_tag`
- **Returns:** null

### findNotes
Find notes matching query.
- **Params:** `query` (string)
- **Returns:** Array of note IDs

### notesInfo
Get detailed info about notes.
- **Params:** `notes` (array of IDs) OR `query` (string)
- **Returns:** Array of note detail objects

### notesModTime
Get modification times.
- **Params:** `notes` (array of IDs)
- **Returns:** Array of `{noteId, mod}` objects

### deleteNotes
Delete notes.
- **Params:** `notes` (array of IDs)
- **Returns:** null

### removeEmptyNotes
Remove notes with no cards.
- **Params:** none
- **Returns:** null

---

## Card Actions

### findCards
Find cards matching query.
- **Params:** `query` (string)
- **Returns:** Array of card IDs

### cardsToNotes
Convert card IDs to note IDs.
- **Params:** `cards` (array)
- **Returns:** Array of note IDs

### cardsInfo
Get detailed card info.
- **Params:** `cards` (array of IDs)
- **Returns:** Array of card detail objects

### cardsModTime
Get card modification times.
- **Params:** `cards` (array)
- **Returns:** Array of `{cardId, mod}` objects

### suspend
Suspend cards.
- **Params:** `cards` (array of IDs)
- **Returns:** boolean

### unsuspend
Unsuspend cards.
- **Params:** `cards` (array of IDs)
- **Returns:** boolean

### suspended
Check if card is suspended.
- **Params:** `card` (ID)
- **Returns:** boolean

### areSuspended
Check suspension status of multiple cards.
- **Params:** `cards` (array)
- **Returns:** Array of booleans/null

### areDue
Check if cards are due.
- **Params:** `cards` (array)
- **Returns:** Array of booleans

### getIntervals
Get card intervals.
- **Params:** `cards` (array), `complete` (optional boolean)
- **Returns:** Array of intervals

### getEaseFactors
Get ease factors.
- **Params:** `cards` (array)
- **Returns:** Array of ease factors

### setEaseFactors
Set ease factors.
- **Params:** `cards` (array), `easeFactors` (array)
- **Returns:** Array of booleans

### setSpecificValueOfCard
Set specific card values.
- **Params:** `card` (ID), `keys` (array), `newValues` (array)
- **Returns:** Array of booleans

### setDueDate
Set card due date.
- **Params:** `cards` (array), `days` (string like "0", "1", "-1", "0!")
- **Returns:** boolean

### forgetCards
Reset cards to new state.
- **Params:** `cards` (array)
- **Returns:** null

### relearnCards
Put cards in relearning queue.
- **Params:** `cards` (array)
- **Returns:** null

### answerCards
Answer cards programmatically.
- **Params:** `answers` (array of `{cardId, ease}` objects)
- **Returns:** Array of booleans

---

## Deck Actions

### deckNames
Get all deck names.
- **Params:** none
- **Returns:** Array of deck names

### deckNamesAndIds
Get deck names with IDs.
- **Params:** none
- **Returns:** Object mapping names to IDs

### getDecks
Get decks containing specified cards.
- **Params:** `cards` (array)
- **Returns:** Object mapping deck names to card arrays

### createDeck
Create a new deck.
- **Params:** `deck` (string name, use `::` for subdecks)
- **Returns:** Deck ID

### changeDeck
Move cards to deck (creates if needed).
- **Params:** `cards` (array), `deck` (string)
- **Returns:** null

### deleteDecks
Delete decks.
- **Params:** `decks` (array of names), `cardsToo` (boolean, required)
- **Returns:** null

### getDeckConfig
Get deck configuration.
- **Params:** `deck` (string)
- **Returns:** Configuration object

### saveDeckConfig
Save deck configuration.
- **Params:** `config` (object)
- **Returns:** boolean

### setDeckConfigId
Assign config to decks.
- **Params:** `decks` (array), `configId` (number)
- **Returns:** boolean

### cloneDeckConfigId
Clone deck configuration.
- **Params:** `name` (string), `cloneFrom` (optional ID)
- **Returns:** New config ID or false

### removeDeckConfigId
Remove deck configuration.
- **Params:** `configId` (number)
- **Returns:** boolean

### getDeckStats
Get deck statistics.
- **Params:** `decks` (array of names)
- **Returns:** Statistics object

---

## Model Actions

### modelNames
Get all model names.
- **Params:** none
- **Returns:** Array of model names

### modelNamesAndIds
Get model names with IDs.
- **Params:** none
- **Returns:** Object mapping names to IDs

### findModelsById
Find models by ID.
- **Params:** `modelIds` (array)
- **Returns:** Array of model objects

### findModelsByName
Find models by name.
- **Params:** `modelNames` (array)
- **Returns:** Array of model objects

### modelFieldNames
Get field names for model.
- **Params:** `modelName` (string)
- **Returns:** Array of field names

### modelFieldDescriptions
Get field descriptions.
- **Params:** `modelName` (string)
- **Returns:** Array of descriptions

### modelFieldFonts
Get field font settings.
- **Params:** `modelName` (string)
- **Returns:** Object mapping fields to font objects

### modelFieldsOnTemplates
Get fields used in templates.
- **Params:** `modelName` (string)
- **Returns:** Object mapping templates to field arrays

### createModel
Create new model.
- **Params:** `modelName`, `inOrderFields`, `cardTemplates`, `css` (optional), `isCloze` (optional)
- **Returns:** Model object

### modelTemplates
Get model templates.
- **Params:** `modelName` (string)
- **Returns:** Object mapping template names to template objects

### modelStyling
Get model CSS.
- **Params:** `modelName` (string)
- **Returns:** Object with css property

### updateModelTemplates
Update model templates.
- **Params:** `model` (object with name and templates)
- **Returns:** null

### updateModelStyling
Update model CSS.
- **Params:** `model` (object with name and css)
- **Returns:** null

### findAndReplaceInModels
Find and replace text in models.
- **Params:** `model` (object with modelName, findText, replaceText, front, back, css booleans)
- **Returns:** Count of replacements

### modelTemplateRename
Rename template.
- **Params:** `modelName`, `oldTemplateName`, `newTemplateName`
- **Returns:** null

### modelTemplateReposition
Reposition template.
- **Params:** `modelName`, `templateName`, `index`
- **Returns:** null

### modelTemplateAdd
Add template.
- **Params:** `modelName`, `template` (object)
- **Returns:** null

### modelTemplateRemove
Remove template.
- **Params:** `modelName`, `templateName`
- **Returns:** null

### modelFieldRename
Rename field.
- **Params:** `modelName`, `oldFieldName`, `newFieldName`
- **Returns:** null

### modelFieldReposition
Reposition field.
- **Params:** `modelName`, `fieldName`, `index`
- **Returns:** null

### modelFieldAdd
Add field.
- **Params:** `modelName`, `fieldName`, `index` (optional)
- **Returns:** null

### modelFieldRemove
Remove field.
- **Params:** `modelName`, `fieldName`
- **Returns:** null

### modelFieldSetFont
Set field font.
- **Params:** `modelName`, `fieldName`, `font`
- **Returns:** null

### modelFieldSetFontSize
Set field font size.
- **Params:** `modelName`, `fieldName`, `fontSize`
- **Returns:** null

### modelFieldSetDescription
Set field description.
- **Params:** `modelName`, `fieldName`, `description`
- **Returns:** boolean

---

## Media Actions

### storeMediaFile
Store media file in Anki.
- **Params:** `filename` (string), one of: `data` (base64), `path`, or `url`; `deleteExisting` (optional)
- **Returns:** Filename string

### retrieveMediaFile
Get media file content.
- **Params:** `filename` (string)
- **Returns:** Base64 string or false

### getMediaFilesNames
List media files.
- **Params:** `pattern` (string, optional glob pattern)
- **Returns:** Array of filenames

### getMediaDirPath
Get media directory path.
- **Params:** none
- **Returns:** Path string

### deleteMediaFile
Delete media file.
- **Params:** `filename` (string)
- **Returns:** null

---

## Graphical Actions

### guiBrowse
Open browser with query.
- **Params:** `query` (string), `reorderCards` (optional object)
- **Returns:** Array of card IDs

### guiSelectCard
Select card in browser.
- **Params:** `card` (ID)
- **Returns:** boolean

### guiSelectedNotes
Get selected notes in browser.
- **Params:** none
- **Returns:** Array of note IDs

### guiAddCards
Open Add Cards dialog.
- **Params:** `note` (object with deckName, modelName, fields, tags)
- **Returns:** Note ID

### guiEditNote
Open note editor.
- **Params:** `note` (ID)
- **Returns:** null

### guiCurrentCard
Get current review card.
- **Params:** none
- **Returns:** Card object or null

### guiStartCardTimer
Start card timer.
- **Params:** none
- **Returns:** boolean

### guiShowQuestion
Show question side.
- **Params:** none
- **Returns:** boolean

### guiShowAnswer
Show answer side.
- **Params:** none
- **Returns:** boolean

### guiAnswerCard
Answer current card.
- **Params:** `ease` (number 1-4)
- **Returns:** boolean

### guiUndo
Undo last action.
- **Params:** none
- **Returns:** boolean

### guiDeckOverview
Show deck overview.
- **Params:** `name` (string)
- **Returns:** boolean

### guiDeckBrowser
Show deck browser.
- **Params:** none
- **Returns:** null

### guiDeckReview
Start deck review.
- **Params:** `name` (string)
- **Returns:** boolean

### guiImportFile
Import file dialog.
- **Params:** `path` (optional string)
- **Returns:** null

### guiExitAnki
Exit Anki.
- **Params:** none
- **Returns:** null

### guiCheckDatabase
Check database integrity.
- **Params:** none
- **Returns:** boolean

---

## Statistic Actions

### getNumCardsReviewedToday
Get today's review count.
- **Params:** none
- **Returns:** Number

### getNumCardsReviewedByDay
Get review counts by day.
- **Params:** none
- **Returns:** Array of [dateString, number] pairs

### getCollectionStatsHTML
Get collection statistics.
- **Params:** `wholeCollection` (boolean)
- **Returns:** HTML string

### cardReviews
Get review history for deck.
- **Params:** `deck` (string), `startID` (unix timestamp)
- **Returns:** Array of review data tuples

### getReviewsOfCards
Get reviews for specific cards.
- **Params:** `cards` (array of IDs)
- **Returns:** Object mapping card IDs to review arrays

### getLatestReviewID
Get latest review timestamp.
- **Params:** `deck` (string)
- **Returns:** Unix timestamp

### insertReviews
Insert review records.
- **Params:** `reviews` (array of tuples)
- **Returns:** null

---

## Miscellaneous Actions

### requestPermission
Request API permission.
- **Params:** none
- **Returns:** Object with permission, requireApiKey, version

### version
Get API version.
- **Params:** none
- **Returns:** Version number

### apiReflect
Get API reflection info.
- **Params:** `scopes` (array), `actions` (array or null)
- **Returns:** Object with scopes and actions

### sync
Sync with AnkiWeb.
- **Params:** none
- **Returns:** null

### getProfiles
Get user profiles.
- **Params:** none
- **Returns:** Array of profile names

### getActiveProfile
Get active profile name.
- **Params:** none
- **Returns:** Profile name string

### loadProfile
Load user profile.
- **Params:** `name` (string)
- **Returns:** boolean

### multi
Execute multiple actions.
- **Params:** `actions` (array of action objects)
- **Returns:** Array of results

### exportPackage
Export deck package.
- **Params:** `deck` (string), `path` (string), `includeSched` (optional boolean)
- **Returns:** boolean

### importPackage
Import deck package.
- **Params:** `path` (string)
- **Returns:** boolean

### reloadCollection
Reload collection.
- **Params:** none
- **Returns:** null
