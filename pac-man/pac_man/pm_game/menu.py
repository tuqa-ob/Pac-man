import pygame

from .config import Config

BUTTONS = [
    "Start Game",
    "High Scores",
    "Instructions",
    "Exit Game",
]

PAUSE_BUTTONS = [
    "Resume",
    "Exit",
]


def make_rects(width: int, height: int) -> dict[str, pygame.Rect]:
    """Build one centered rectangle per button for a window size.

    Args:
        width: window width in pixels.
        height: window height in pixels.
    """
    rects = {}
    button_h = int(height * 0.082)
    button_w = int(button_h * 6.3)
    gap = max(4, button_h // 10)
    start_y = int(height * 0.30)
    for i, name in enumerate(BUTTONS):
        x = (width - button_w) // 2
        y = start_y + i * (button_h + gap)
        rects[name] = pygame.Rect(x, y, button_w, button_h)
    return rects


def make_pause_rects(width: int, height: int) -> dict[str, pygame.Rect]:
    """Build one centered rectangle per pause-menu button.

    Args:
        width: window width in pixels.
        height: window height in pixels.
    """
    rects = {}
    button_h = int(height * 0.095)
    button_w = int(button_h * 4.4)
    gap = int(button_h * 0.3)
    start_y = int(height * 0.42)
    for i, name in enumerate(PAUSE_BUTTONS):
        x = (width - button_w) // 2
        y = start_y + i * (button_h + gap)
        rects[name] = pygame.Rect(x, y, button_w, button_h)
    return rects


def get_clicked_button(
    rects: dict[str, pygame.Rect],
    pos: tuple[int, int],
) -> str | None:
    """Return the name of the button at pos, or None if no button is there.

    Args:
        rects: one rectangle per button name.
        pos: the mouse position (x, y).
    """
    for name, rect in rects.items():
        if rect.collidepoint(pos):
            return name
    return None


def get_instructions(config: Config) -> list[tuple[str, list[str]]]:
    """Return the instruction screen text, using the values of the config.

    Args:
        config: the game configuration.

    Returns:
        A list of (heading, lines) pairs.
    """
    pacgum = config.get("points_per_pacgum")
    super_pacgum = config.get("points_per_super_pacgum")
    ghost = config.get("points_per_ghost")
    lives = config.get("lives")
    seconds = config.get("level_max_time")
    return [
        ("CONTROLS", [
            "ARROW KEYS or W A S D: move Pac-Man one step.",
            "PAUSE button under the maze: pause and resume the game.",
        ]),
        ("RULES", [
            "Eat every pacgum to clear the level.",
            f"A pacgum gives {pacgum} points, "
            f"a super pacgum gives {super_pacgum} points.",
            "A super pacgum makes the ghosts edible for a short time. "
            f"Eating an edible ghost gives {ghost} points.",
            "If a ghost that is not edible touches you, you lose a life. "
            f"You start with {lives} lives.",
            f"Each level has {seconds} seconds. "
            "When the time is over, the game is over.",
            "Clear all the levels to win. "
            "Your score goes to the high scores.",
        ]),
    ]
