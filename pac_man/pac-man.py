import sys
from pm_game.config import Config


def main() -> None:
    """main entry point to pac-man game"""
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config_file.json>")
        sys.exit(1)
    config_path = sys.argv[1]
    print(f"Loading game with config : {config_path}")
    config = Config(config_path)
    file_name = config.get("highscore_filename")
    pacgum = config.get("pacgum")
    points_gum = config.get("points_per_pacgum")
    points_sgum = config.get("points_per_super_pacgum")
    points_ghost = config.get("points_per_ghost")
    time = config.get("level_max_time")
    levels = config.get("level")
    lives = config.get("lives")
    seed = config.get("seed")

    print("Game Settings Loaded Successfully:")
    print(f"{file_name} , {pacgum} , {points_gum}, {points_sgum}"
          f", {points_ghost}, {time}, {levels}")
    print(f" - Initial Lives: {lives}")
    print(f" - Maze Seed: {seed}")


if __name__ == "__main__":
    main()
