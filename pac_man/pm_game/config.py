import json
from typing import Any, Dict
from copy import deepcopy


class Config:
    """Game settings read from a JSON file, with safe defaults."""

    def __init__(self, file_path: str = "") -> None:
        """Create the settings and load a file if a path is given.

        Args:
            file_path: path of the JSON config file (optional).
        """
        self.default_values: Dict[str, Any] = {
            "highscore_filename": "highscores.json",
            "lives": 3,
            "pacgum": 42,
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "seed": 42,
            "level_max_time": 90,
            "level": [
                {"width": 10, "height": 10},
                {"width": 15, "height": 10},
                {"width": 20, "height": 10},
                {"width": 20, "height": 15},
                {"width": 25, "height": 15},
                {"width": 25, "height": 20},
                {"width": 30, "height": 20},
                {"width": 30, "height": 25},
                {"width": 35, "height": 25},
                {"width": 40, "height": 30}
                ]
        }

        self.data: Dict[str, Any] = deepcopy(self.default_values)

        if file_path:
            self.load(file_path)

    def load(self, file_path: str) -> None:
        """Read a config file and keep its valid values.

        Problems never stop the game: the defaults are used and a
        warning is printed.

        Args:
            file_path: path of the JSON config file.
        """
        try:
            text = self._read_file(file_path)
            new_values = json.loads(text)

        except FileNotFoundError:
            print(
                f"[Warning] Config file '{file_path}' not found. "
                "Using defaults."
            )
            return

        except OSError as e:
            print(
                f"[Warning] Could not read config file: {e}. "
                "Using defaults."
            )
            return

        except json.JSONDecodeError as e:
            print(
                f"[Warning] Invalid JSON in config file: {e}. "
                "Using defaults."
            )
            return

        if not isinstance(new_values, dict):
            print(
                "[Warning] Config must contain a JSON object. "
                "Using defaults."
            )
            return

        self._validate(new_values)

    def _read_file(self, file_path: str) -> str:
        """Read a config file without its comment lines.

        Lines starting with # or // are ignored.

        Args:
            file_path: path of the config file.

        Returns:
            The text of the file, ready for the JSON parser.
        """
        text = ""

        with open(file_path, "r") as file:
            for line in file:
                stripped = line.strip()

                if not stripped or stripped.startswith(("#", "//")):
                    continue

                text += stripped

        return text

    def _validate(self, new_values: Dict[str, Any]) -> None:
        """Keep the valid values of the file and ignore the others.

        Unknown keys are ignored, and invalid values are replaced by the
        defaults, with a warning.

        Args:
            new_values: the content of the config file.
        """
        for key, value in new_values.items():

            if key not in self.default_values:
                print(
                    f"[Warning] Unknown config key '{key}'. "
                    "Ignoring it."
                )
                continue

            if key == "level":
                if self._validate_levels(value):
                    self.data["level"] = value
                else:
                    self.data["level"] = self.default_values["level"]
                continue

            if self._is_valid(key, value):
                self.data[key] = value
            else:
                print(
                    f"[Warning] Invalid value for '{key}'. "
                    f"Using default: {self.default_values[key]}"
                )
        for key in self.default_values:
            if key not in new_values:
                print(
                    f"[Warning] Missing key '{key}'. "
                    f"Using default: {self.default_values[key]}"
                )

    def _is_valid(self, key: str, value: Any) -> bool:
        """Tell if a value is acceptable for a config key.

        Args:
            key: name of the setting.
            value: the value found in the file.

        Returns:
            True if the value can be used, otherwise False.
        """
        if key == "highscore_filename":
            return isinstance(value, str) and bool(value.strip())

        if key in {
            "lives",
            "pacgum",
            "points_per_pacgum",
            "points_per_super_pacgum",
            "points_per_ghost",
            "seed",
            "level_max_time"
        }:
            return (
                    isinstance(value, int)
                    and not isinstance(value, bool)
                    and value > 0)
        return False

    def _validate_levels(self, levels: Any) -> bool:
        """Tell if the list of levels can be used.

        Args:
            levels: the value of the 'level' key.

        Returns:
            True if there are at least 10 levels with usable sizes.
        """
        if not isinstance(levels, list) or len(levels) < 10:
            print("[Warning] Invalid 'level'."
                  "At least 10 levels are required. Using default levels."
                  )
            return False

        for i, level in enumerate(levels):
            level_number = i + 1

            if i < len(self.default_values["level"]):
                default_level = self.default_values["level"][i]
            else:
                default_level = self.default_values["level"][-1]

            if not isinstance(level, dict):
                print(
                    f"[Warning] Invalid level {level_number}. "
                    f"Using default."
                )
                levels[i] = default_level.copy()
                continue

            if "width" not in level:
                level["width"] = default_level["width"]
                print(
                    f"[Warning] Missing 'width' in level {level_number}. "
                    f"Using default: {level['width']}"
                )

            elif (
                    type(level["width"]) is not int
                    or level["width"] < 5):
                level["width"] = default_level["width"]
                print(
                    f"[Warning] Invalid 'width' in level {level_number}. "
                    f"Using default: {level['width']}"
                )

            if "height" not in level:
                level["height"] = default_level["height"]
                print(
                    f"[Warning] Missing 'height' in level {level_number}. "
                    f"Using default: {level['height']}"
                )

            elif (
                    type(level["height"]) is not int
                    or level["height"] < 5):
                level["height"] = default_level["height"]
                print(
                    f"[Warning] Invalid 'height' in level {level_number}. "
                    f"Using default: {level['height']}"
                )

        return True

    def get(self, key: str) -> Any:
        """Return the value of a setting, or its default value.

        Args:
            key: name of the setting.

        Returns:
            The value of the setting.
        """
        return self.data.get(key, self.default_values.get(key))
