import pygame

BUTTONS = [
    "Start Game",
    "High Scores",
    "Instructions",
    "Exit Game",
]

def make_rects(width: int, height: int) -> dict[str, pygame.Rect]:
    """Build one centered rectangle per button for a window size.

    Args:
        width: window width in pixels.
        height: window height in pixels.
    """
    rects = {}
    button_w = width // 2
    button_h = height // 12
    gap = button_h // 4
    for i, name in enumerate(BUTTONS):
        x = (width - button_w) // 2
        y = height // 3 + i * (button_h + gap)
        rects[name] = pygame.Rect(x, y, button_w, button_h)
    return rects

def get_clicked_button(
        rects: dict[str, pygame.Rect],
        pos: tuple[int, int]
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

