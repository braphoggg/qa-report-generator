"""Persist take history to a local JSON file for timeline rendering."""

import json
import os

from app.models.report import TakeHistoryEntry

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "history.json")


def load_history() -> list:
    """Load take history entries from the JSON file."""
    path = os.path.normpath(HISTORY_FILE)
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [
            TakeHistoryEntry(
                branch=entry.get("branch", ""),
                take=entry.get("take", 0),
                verdict=entry.get("verdict", "na"),
                date=entry.get("date", ""),
            )
            for entry in data
        ]
    except (json.JSONDecodeError, KeyError):
        return []


def save_history_entry(branch: str, take: int, verdict: str, date: str):
    """Save a history entry, overriding any existing entry for the same branch+take."""
    path = os.path.normpath(HISTORY_FILE)

    # Load existing
    entries = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except (json.JSONDecodeError, KeyError):
            entries = []

    # Check if entry for this branch+take already exists — override it
    new_entry = {
        "branch": branch,
        "take": take,
        "verdict": verdict,
        "date": date,
    }

    found = False
    for i, entry in enumerate(entries):
        if entry.get("branch") == branch and entry.get("take") == take:
            entries[i] = new_entry
            found = True
            break

    if not found:
        entries.append(new_entry)

    # Save
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
