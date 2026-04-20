# Preflight Check

Run this sequence before any wizard work or diagnostic. It confirms the user's Anki + AnkiConnect environment is healthy. Every check either passes silently or gives the user a **specific, copy-pasteable fix** and a way to retry.

**Audience reminder:** The user is a language learner, not a developer. Never paste a raw curl command or link to docs without context. Show the fix, wait for them to do it, then re-run the check.

## How to run

Run each check in order. On failure, show the user the fix message for that check, then ask them to reply when they've done it (or say "skip" / "I can't do this right now"). Re-run the failing check, then continue down the list.

If a check fails 3 times in a row with the same error, offer to pause setup — don't trap the user in a loop.

---

## Check 1: Is Anki Desktop installed?

**How to detect:** Try the connection in Check 3. If `curl` reports `Connection refused`, there's a decent chance Anki isn't installed at all. Ask the user directly: "Do you have Anki Desktop installed and open right now?" If no, show the fix.

**Fix:**

> You'll need Anki Desktop first (it's free).
>
> - **macOS:** `brew install --cask anki` — or download from https://apps.ankiweb.net/#downloads
> - **Windows:** https://apps.ankiweb.net/#downloads — download the installer and run it.
> - **Linux:** https://apps.ankiweb.net/#downloads — or your package manager if it has a recent version.
>
> Reply when you've installed and opened it.

---

## Check 2: Is Anki currently running?

**How to detect:** The connection attempt in Check 3 returns `Connection refused` but Anki *is* installed.

**Fix:**

> Open Anki Desktop now — I'll wait. It needs to be running in the background for the rest of this to work. Reply "ready" when it's open.

---

## Check 3: Is AnkiConnect responding on port 8765?

**Command:**

```bash
curl -s --max-time 3 localhost:8765 -X POST -d '{"action": "version", "version": 6}' 2>/dev/null
```

**Note the `--max-time 3`** — never let this hang. If curl returns nothing within 3 seconds, treat it as a failure.

**If the response is empty or a connection error:**

The AnkiConnect add-on probably isn't installed. Fix:

> AnkiConnect is the add-on that lets me talk to Anki. To install it:
>
> 1. In Anki, open **Tools → Add-ons**
> 2. Click **Get Add-ons…**
> 3. Paste this code: **`2055492159`**
> 4. Click OK, then **fully restart Anki** (quit and reopen)
>
> Reply when Anki is back open.

**If the response is a valid JSON object with an `error` field:**

Pass it through — most AnkiConnect errors are specific enough to show to the user directly.

---

## Check 4: Is AnkiConnect version ≥ 6?

**Extract the version from the Check 3 response.** Expected shape: `{"result": 6, "error": null}` or higher.

**If result is missing, not a number, or < 6:**

> Your AnkiConnect add-on is outdated (version `[N]`, this template needs at least 6). In Anki, go to **Tools → Add-ons**, select AnkiConnect, click **Check for Updates**, then restart Anki.
>
> Reply when you've updated it.

---

## Done

When all four checks pass, tell the user briefly: "Anki is connected (AnkiConnect v[N]). Let's keep going." Then return control to the caller (either `first-time-setup.md`, `diagnostic.md`, or an integration guide).

Do **not** dump technical details (like the full JSON response) unless the user asks.
