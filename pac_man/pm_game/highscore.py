import json
from pathlib import Path


class Highscore:
    """Load, validate, and persist the top 10 Pac-Man highscores."""

    MAX_ENTRIES = 10
    MAX_NAME_LENGTH = 10

    def __init__(self, file_path: str) -> None:
        """Load existing highscores from disk, if any.
        Args:
            file_path: path to the JSON file storing highscores.
        """

        self.file_path = Path(file_path)
        self.entries: list[dict[str, str | int]] = []
        self.load()

    def load(self) -> None:
        """Read scores from disk. On any problem, start with an empty list."""

        self.entries = []

        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        except OSError as e:
            print(f"[Warning] Could not read highscores file: {e}. "
                  "Starting with an empty list.")
            return
        except json.JSONDecodeError as e:
            print(f"[Warning] Invalid JSON in highscores file: {e}. "
                  "Starting with an empty list.")
            return

        if not isinstance(data, list):
            print("[Warning] Highscores file must contain a JSON list. "
                  "Starting with an empty list.")
            return

        valid_entries = []
        for entry in data:
            if (
                isinstance(entry, dict)
                and isinstance(entry.get("name"), str)
                and isinstance(entry.get("score"), int)
                and not isinstance(entry.get("score"), bool)
                and entry["score"] >= 0
            ):

                valid_entries.append({
                    "name": entry["name"][:self.MAX_NAME_LENGTH],
                    "score": entry["score"]
                    })
            else:
                print(f"[Warning] Ignoring invalid highscore entry: {entry}")

        self.entries = valid_entries

    def save(self) -> None:
        """Write the current entries back to disk."""

        try:
            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with open(self.file_path, "w") as f:
                json.dump(self.entries, f, indent=2)
        except OSError as e:
            print(f"[Warning] Could not save highscores file: {e}")

    def _clean_name(self, name: str) -> str:
        """Keep only letters, digits and spaces, max MAX_NAME_LENGTH chars."""

        cleaned = "".join(c for c in name if c.isalnum() or c == " ")
        cleaned = cleaned.strip()
        return cleaned[:self.MAX_NAME_LENGTH] or "Player"

    def add_score(self, name: str, score: int) -> None:
        """Add a new entry, keeping only the top MAX_ENTRIES scores.

        Args:
            name: the player's name (will be cleaned and truncated).
            score: a non-negative integer score.
        """

        if not isinstance(score, int) or isinstance(score, bool) or score < 0:
            print(f"[Warning] Ignoring invalid score: {score}")
            return

        clean = self._clean_name(name)
        self.entries.append({"name": clean, "score": score})
        self.entries.sort(key=lambda e: e["score"], reverse=True)
        self.entries = self.entries[:self.MAX_ENTRIES]
        self.save()

    def top(self) -> list[dict[str, str | int]]:
        """Return all highscore entries, already sorted, highest first."""
        return [entry.copy() for entry in self.entries]
