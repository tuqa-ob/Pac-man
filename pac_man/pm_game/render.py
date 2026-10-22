import pygame
from .ghost import Ghost, GhostState
from pm_game.adapter import MazeAdapter
from pm_game.player import Player
from pathlib import Path
import math


class Renderer:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    
    def __init__(self, screen: pygame.Surface, maze: MazeAdapter) -> None:
        self._screen = screen
        self._maze = maze
        self.fit_maze()
        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        self.ghost_images = {
                "blue": pygame.image.load(
                    str(assets_dir / "blue.png")
                    ).convert_alpha(),
                "orange": pygame.image.load(
                    str(assets_dir / "orange.png")
                    ).convert_alpha(),
                "pink": pygame.image.load(
                    str(assets_dir / "pink.png")
                    ).convert_alpha(),
                "red": pygame.image.load(
                    str(assets_dir / "red.png")
                    ).convert_alpha(),
                "eaten": pygame.image.load(
                    str(assets_dir / "eaten.png")
                    ).convert_alpha()
                }
        self.all_bg = pygame.image.load(
                    str(assets_dir / "bg.png")
                    ).convert_alpha()

        self.font_path = str(assets_dir / "BebasNeue-Regular.ttf")
        self.pacman_image = pygame.image.load(
                str(assets_dir /"pac-man.png")
                ).convert_alpha()


        try:
            self.menu_bg = pygame.image.load(
                str(assets_dir / "menu.png")
            ).convert()
        except (pygame.error, FileNotFoundError):
            self.menu_bg = None

        try:
            self.hs_bg = pygame.image.load(
                str(assets_dir / "HS.png")
            ).convert()
        except (pygame.error, FileNotFoundError):
            self.hs_bg = None

        try:
            self.maze_bg = pygame.image.load(
                str(assets_dir / "maze.png")
            ).convert()
        except (pygame.error, FileNotFoundError):
            self.maze_bg = None
        
        try:
            self.gameOver = pygame.image.load(
                str(assets_dir / "gameover.png")
            ).convert()
        except (pygame.error, FileNotFoundError):
            self.gameOver = None
        
        try:
            self.won = pygame.image.load(
                str(assets_dir / "won.png")
            ).convert()
        except (pygame.error, FileNotFoundError):
            self.won = None

        try:
            self.instr = pygame.image.load(
                str(assets_dir / "instr.png")
            ).convert()
        except (pygame.error, FileNotFoundError):
            self.instr = None



    def calculate_pos(self) -> tuple[int, int]:
        cell = self.cell_size
        maze_width = self._maze.width * cell
        maze_height = self._maze.height * cell
        offset_x = (self._screen.get_width() - maze_width) // 2
        offset_y = (self._screen.get_height() - maze_height) // 2
        return (offset_x, offset_y)

    def make_font(self, size: int) -> pygame.font.Font:
        """Return the Bebas Neue font, or the default font if it is missing."""
        try:
            return pygame.font.Font(self.font_path, size)
        except (pygame.error, FileNotFoundError):
            return pygame.font.Font(None, size)

    def fit_maze(self) -> None:
        """Choose the cell size so the maze fits between the side panels."""
        avail_w = int(self._screen.get_width() * 0.65)
        avail_h = int(self._screen.get_height() * 0.85)
        self.cell_size = min(
            avail_w // self._maze.width,
            avail_h // self._maze.height,
        )
        self.build_maze_surface()


    def maze_segments(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """List every wall as two points, relative to the maze corner."""
        cell = self.cell_size
        segments = []
        for r in range(self._maze.height):
            for c in range(self._maze.width):
                x = c * cell
                y = r * cell
                if self._maze.has_wall(r, c, self.NORTH):
                    segments.append(((x, y), (x + cell, y)))
                if self._maze.has_wall(r, c, self.WEST):
                    segments.append(((x, y), (x, y + cell)))
                if self._maze.has_wall(r, c, self.EAST):
                    segments.append(((x + cell, y), (x + cell, y + cell)))
                if self._maze.has_wall(r, c, self.SOUTH):
                    segments.append(((x, y + cell), (x + cell, y + cell)))
        return segments

    def build_maze_surface(self) -> None:
        """Draw the glowing neon maze once and keep it for every frame."""
        cell = self.cell_size
        self.maze_pad = max(8, cell // 2)
        pad = self.maze_pad
        size = (
            self._maze.width * cell + 2 * pad,
            self._maze.height * cell + 2 * pad,
        )
        thick = max(2, cell // 10)
        segments = [
            ((x1 + pad, y1 + pad), (x2 + pad, y2 + pad))
            for (x1, y1), (x2, y2) in self.maze_segments()
        ]

        lines = pygame.Surface(size, pygame.SRCALPHA)
        for start, end in segments:
            pygame.draw.line(lines, (20, 110, 255), start, end, thick + 2)

        # blur: shrink the lines, then enlarge them again
        small = pygame.transform.smoothscale(
            lines, (size[0] // 5, size[1] // 5)
        )
        glow = pygame.transform.smoothscale(small, size)

        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.blit(glow, (0, 0))
        surface.blit(glow, (0, 0))
        surface.blit(lines, (0, 0))
        for start, end in segments:
            pygame.draw.line(surface, (140, 210, 255), start, end, 1)
        self.maze_surface = surface

    def draw_maze(self) -> None:
        """Draw the cached neon maze in the middle of the window."""
        offset_x, offset_y = self.calculate_pos()
        background = pygame.transform.scale(
            self.maze_bg,
            self._screen.get_size(),
        )
        self._screen.blit(background, (0, 0))

        self._screen.blit(
            self.maze_surface,
            (offset_x - self.maze_pad, offset_y - self.maze_pad),
        )


    def draw_player(self, player: Player) -> None:
        cell = self.cell_size
        offset_x, offset_y = self.calculate_pos()
        x = offset_x + (player.curr_col + 0.5) * cell
        y = offset_y + (player.curr_row + 0.5) * cell

        image_size = int(cell * 0.7)
        image = pygame.transform.smoothscale(
            self.pacman_image,
            (image_size, image_size),
            )
        image_rect = image.get_rect(
                center=(round(x), round(y)))
        self._screen.blit(image, image_rect)

    def update_screen(self, screen: pygame.Surface) -> None:
        self._screen = screen
        self.fit_maze()


    def draw_pac_gum(self, pacgums: set[tuple[int, int]]) -> None:
        """Draw the small yellow dots."""
        offset_x, offset_y = self.calculate_pos()
        cell = self.cell_size
        for r, c in pacgums:
            x = offset_x + (c + 0.5) * cell
            y = offset_y + (r + 0.5) * cell
            pygame.draw.circle(
                self._screen,
                (255, 215, 0),
                (x, y),
                max(2, cell // 9),
            )

    def draw_super_pacgum(
        self,
        pacgums: set[tuple[int, int]],
    ) -> None:
        """Draw the big pink pellets with a soft glow."""
        offset_x, offset_y = self.calculate_pos()
        cell = self.cell_size
        radius = cell // 4
        size = radius * 6
        glow = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)
        pygame.draw.circle(glow, (255, 60, 255, 40), center, radius * 3)
        pygame.draw.circle(glow, (255, 60, 255, 80), center, radius * 2)
        pygame.draw.circle(
            glow, (255, 60, 255, 140), center, int(radius * 1.4)
        )
        for r, c in pacgums:
            x = offset_x + (c + 0.5) * cell
            y = offset_y + (r + 0.5) * cell
            self._screen.blit(glow, (x - size // 2, y - size // 2))
            pygame.draw.circle(
                self._screen,
                (255, 120, 255),
                (x, y),
                radius,
            )

    def draw_panel(self, rect: pygame.Rect, label: str, value: str) -> None:
        """Draw one HUD panel: a small label and a big value."""
        glass = pygame.Surface(rect.size, pygame.SRCALPHA)
        area = glass.get_rect()
        pygame.draw.rect(glass, (4, 10, 35, 200), area, border_radius=12)
        pygame.draw.rect(glass, (0, 110, 255, 90), area, 8, border_radius=12)
        pygame.draw.rect(glass, (60, 190, 255), area, 2, border_radius=12)
        self._screen.blit(glass, rect.topleft)
        label_font = self.make_font(rect.height // 4)
        value_font = self.make_font(rect.height // 2)
        label_text = label_font.render(label, True, (190, 190, 210))
        value_text = value_font.render(value, True, (255, 255, 255))
        x = rect.x + rect.width // 12
        self._screen.blit(label_text, (x, rect.y + rect.height // 8))
        self._screen.blit(value_text, (x, rect.y + rect.height // 2 - 6))

    def draw_hud(self, score: int, lives: int, level: int, time_left: float) -> None:
        """Draw the side panels: score and lives left, level right."""
        width = self._screen.get_width()
        height = self._screen.get_height()
        offset_x, offset_y = self.calculate_pos()
        maze_w = self._maze.width * self.cell_size
        panel_w = int(width * 0.12)
        panel_h = int(height * 0.10)
        gap = int(height * 0.03)
        margin = int(width * 0.03)
        left_x = offset_x - panel_w - margin
        right_x = offset_x + maze_w + margin
        top_y = offset_y + int(height * 0.04)
        
        total = math.ceil(time_left)
        minutes = total // 60
        seconds = total % 60
        time_text = f"{minutes:02d}:{seconds:02d}"

        self.draw_panel(
            pygame.Rect(left_x, top_y, panel_w, panel_h),
            "SCORE",
            str(score),
        )
        self.draw_panel(
            pygame.Rect(left_x, top_y + panel_h + gap, panel_w, panel_h),
            "LIVES",
            str(lives),
        )
        self.draw_panel(
            pygame.Rect(right_x, top_y + panel_h + gap, panel_w, panel_h),
            "TIME",
            str(time_text)
        )
        self.draw_panel(
            pygame.Rect(right_x, top_y, panel_w, panel_h),
            "LEVEL",
            str(level),
        )



    def draw_ghost(self, ghost: Ghost) -> None:
        cell = self.cell_size
        offset_x, offset_y = self.calculate_pos()
        x = offset_x + ghost.current_col * cell
        y = offset_y + ghost.current_row * cell
        if ghost.state == GhostState.EATEN:
            image = self.ghost_images["eaten"]
        else:
            image = self.ghost_images[ghost.color]
        image = pygame.transform.scale(image, (cell, cell))
        self._screen.blit(image, (x, y))

    def update_maze(self, maze: MazeAdapter) -> None:
        """Update the maze used by the renderer."""
        self._maze = maze
        self.fit_maze()

    def draw_input_box(self, rect: pygame.Rect) -> None:
        """Draw a neon glass box for typing text."""
        glass = pygame.Surface(rect.size, pygame.SRCALPHA)
        area = glass.get_rect()
        pygame.draw.rect(glass, (4, 10, 35, 210), area, border_radius=10)
        pygame.draw.rect(glass, (0, 110, 255, 90), area, 8, border_radius=10)
        pygame.draw.rect(glass, (60, 190, 255), area, 2, border_radius=10)
        self._screen.blit(glass, rect.topleft)
 


    def draw_game_over(self, score: int, player_name: str = "") -> None:
        """Draw the Game Over screen."""
        background = pygame.transform.scale(
            self.gameOver,
            self._screen.get_size(),
        )
        self._screen.blit(background, (0, 0))

        font = pygame.font.Font(None, 64)
        score_font = pygame.font.Font(None, 36)
        input_font = pygame.font.Font(None, 32)
        instruction_font = pygame.font.Font(None, 26)


        score_text = score_font.render(
            f"Final Score: {score}", True, (255, 255, 255)
        )

        name_label = input_font.render(
                "Enter your name:", True, (255, 255, 255)
                )

        name_text = input_font.render(
                player_name + "_", True, (255, 255, 0)
                )

        instruction = instruction_font.render(
            "Press ENTER to submit", True, (200, 200, 200)
            )

        screen_width, screen_height = self._screen.get_size()

        center_x = screen_width // 2
        center_y = screen_height // 2


        self._screen.blit(
            score_text,
            score_text.get_rect(center=(center_x, center_y - 45)),
        )
        self._screen.blit(
            name_label,
            name_label.get_rect(center=(center_x, center_y + 10)),
        )

        input_rect = pygame.Rect(
            center_x - 150, center_y + 35, 300, 45
        )
        self.draw_input_box(input_rect)
        self._screen.blit(
            name_text,
            name_text.get_rect(
                midleft=(input_rect.left + 10, input_rect.centery)
            ),
        )
        self._screen.blit(
            instruction,
            instruction.get_rect(center=(center_x, center_y + 110)),
        )


    def draw_victory(self, score: int, player_name: str = "") -> None:
        """Draw the victory screen."""
        background = pygame.transform.scale(
            self.won,
            self._screen.get_size(),
        )
        self._screen.blit(background, (0, 0))


        font = pygame.font.Font(None, 64)
        score_font = pygame.font.Font(None, 36)
        input_font = pygame.font.Font(None, 32)
        instruction_font = pygame.font.Font(None, 26)

        score_text = score_font.render(
            f"Final Score: {score}", True, (255, 255, 255)
        )

        name_label = input_font.render(
            "Enter your name:", True, (255, 255, 255)
        )
        name_text = input_font.render(
            player_name + "_", True, (255, 255, 0)
        )
        instruction = instruction_font.render(
            "Press ENTER to submit", True, (200, 200, 200)
        )

        screen_width, screen_height = self._screen.get_size()
        center_x = screen_width // 2
        center_y = screen_height // 2

        self._screen.blit(
            score_text,
            score_text.get_rect(center=(center_x, center_y - 45)),
        )
        self._screen.blit(
            name_label,
            name_label.get_rect(center=(center_x, center_y + 10)),
        )

        input_rect = pygame.Rect(
            center_x - 150, center_y + 35, 300, 45
        )
        self.draw_input_box(input_rect)
        self._screen.blit(
            name_text,
            name_text.get_rect(
                midleft=(input_rect.left + 10, input_rect.centery)
            ),
        )
        self._screen.blit(
            instruction,
            instruction.get_rect(center=(center_x, center_y + 110)),
        )

    def draw_neon_button(self, screen: pygame.Surface,
                         rect: pygame.Rect, text: str,
                         font: pygame.font.Font, is_hovered: bool = False) -> None:
        """Draws a futuristic neon button with dual cyan/yellow borders."""
        button_surface = pygame.Surface(
            rect.size, pygame.SRCALPHA
        )
        button_rect = button_surface.get_rect()

        if is_hovered:
            glow_color = (0, 220, 255, 70)
            pygame.draw.rect(
                button_surface,
                glow_color,
                button_rect.inflate(-2, -2),
                border_radius=10,
            )
            outer_color = (0, 255, 255)
            inner_color = (255, 255, 0)
            text_color = (255, 255, 0)
            border_width = 4
        else:
            outer_color = (0, 160, 180)
            inner_color = (200, 150, 0)
            text_color = (255, 255, 255)
            border_width = 2

        pygame.draw.rect(
            button_surface,
            outer_color,
            button_rect,
            width=2,
            border_radius=8,
        )

        pygame.draw.rect(
            button_surface,
            inner_color,
            button_rect.inflate(-6, -6),
            width=1,
            border_radius=6,
        )

        text_surface = font.render(
            text, True, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(
            center=button_rect.center
        )
        button_surface.blit(text_surface, text_rect)

        screen.blit(button_surface, rect.topleft)


    def draw_main_menu(self, rects: dict[str, pygame.Rect], mouse_pos: tuple[int, int]) -> None:
 
        width = self._screen.get_width()
        height = self._screen.get_height()
        if self.menu_bg is not None:
             background = pygame.transform.smoothscale(
                 self.menu_bg, (width, height)
             )
             self._screen.blit(background, (0, 0))



        font = pygame.font.SysFont("Arial", 22, bold=True)

        for name, rect in rects.items():
            is_hovered = rect.collidepoint(mouse_pos)
            self.draw_neon_button(self._screen, rect, name, font, is_hovered)


    def draw_highscores(self, entries: list[dict[str, str | int]]) -> None:
        """Draw the top 10 highscores screen."""
        width = self._screen.get_width()
        height = self._screen.get_height()

        if self.hs_bg is not None:
            background = pygame.transform.smoothscale(
                self.hs_bg, (width, height)
            )
            self._screen.blit(background, (0, 0))

        #title_font = self.make_font(height // 10)
        line_font = self.make_font(height // 20)
        hint_font = self.make_font(height // 36)

        #title = title_font.render("HIGH SCORES", True, (255, 255, 0))
        #self._screen.blit(
        #    title,
        #    title.get_rect(center=(width // 2, height // 8)),
        #)


        panel = pygame.Rect(0, 0, width // 2, int(height * 0.62))
        panel.center = (width // 2, int(height * 0.44))
        shade = pygame.Surface(panel.size, pygame.SRCALPHA)
        shade.fill((0, 0, 0, 140))
        self._screen.blit(shade, panel.topleft)

        if not entries:
            empty = line_font.render("NO SCORES YET", True, (255, 255, 255))
            self._screen.blit(empty, empty.get_rect(center=panel.center))

        row_h = panel.height / 10
        for i, entry in enumerate(entries[:10]):
            y = int(panel.top + (i + 0.5) * row_h)
            rank = line_font.render(f"{i + 1}.", True, (255, 255, 255))
            name = line_font.render(
                str(entry["name"]).upper(), True, (255, 255, 255)
            )
            score = line_font.render(str(entry["score"]), True, (255, 255, 0))
            self._screen.blit(
                rank, rank.get_rect(midleft=(panel.left + 20, y))
            )
            self._screen.blit(
                name, name.get_rect(midleft=(panel.left + 90, y))
            )
            self._screen.blit(
                score, score.get_rect(midright=(panel.right - 20, y))
            )

        hint = hint_font.render(
            "PRESS ESC OR CLICK TO GO BACK", True, (255, 255, 0)
        )
        self._screen.blit(
            hint,
            hint.get_rect(center=(width // 2, height - height // 14)),
        )

    def pause_button_rect(self) -> pygame.Rect:
        """Return the rectangle of the Pause button under the maze."""

        offset_x, offset_y = self.calculate_pos()
        maze_w = self._maze.width * self.cell_size
        maze_h = self._maze.height * self.cell_size
        room = self._screen.get_height() - (offset_y + maze_h)
        button_h = int(room * 0.4)
        rect = pygame.Rect(0, 0, int(button_h * 3.5), button_h)
        rect.midtop = (
            offset_x + maze_w // 2,
            offset_y + maze_h + int(room * 0.2),
        )
        return rect

    def draw_pause_button(self, mouse_pos: tuple[int, int]) -> None:
        """Draw the Pause button under the maze."""
        rect = self.pause_button_rect()
        font = self.make_font(int(rect.height * 0.7))
        self.draw_neon_button(
            self._screen, rect, "PAUSE", font, rect.collidepoint(mouse_pos)
        )

    def draw_pause_menu(
        self,
        rects: dict[str, pygame.Rect],
        mouse_pos: tuple[int, int],
    ) -> None:
        """Dim the game and draw the pause title and its two buttons."""
        width = self._screen.get_width()
        height = self._screen.get_height()
        shade = pygame.Surface((width, height), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 170))
        self._screen.blit(shade, (0, 0))

        title_font = self.make_font(height // 8)
        title = title_font.render("PAUSED", True, (255, 255, 255))
        self._screen.blit(
            title,
            title.get_rect(center=(width // 2, int(height * 0.30))),
        )

        first = next(iter(rects.values()))
        font = self.make_font(int(first.height * 0.6))
        for name, rect in rects.items():
            self.draw_neon_button(
                self._screen,
                rect,
                name.upper(),
                font,
                rect.collidepoint(mouse_pos),
            )
    def wrap_text(
        self,
        font: pygame.font.Font,
        text: str,
        max_width: int,
    ) -> list[str]:
        """Cut a text into lines that are not wider than max_width."""
        lines: list[str] = []
        current = ""
        for word in text.split():
            trial = f"{current} {word}".strip()
            if not current or font.size(trial)[0] <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def draw_instructions(
        self,
        sections: list[tuple[str, list[str]]],
    ) -> None:
        """Draw the instructions screen: controls and rules."""
        width = self._screen.get_width()
        height = self._screen.get_height()

        background = pygame.transform.scale(
            self.instr,
            (width, height),
        )
        self._screen.blit(background, (0, 0))

        dim = pygame.Surface((width, height), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 90))
        self._screen.blit(dim, (0, 0))

        title_font = self.make_font(height // 10)
        head_font = self.make_font(height // 22)
        text_font = self.make_font(height // 30)
        hint_font = self.make_font(height // 36)

        title = title_font.render("INSTRUCTIONS", True, (255, 255, 0))
        self._screen.blit(
            title,
            title.get_rect(center=(width // 2, int(height * 0.09))),
        )

        panel = pygame.Rect(0, 0, int(width * 0.7), int(height * 0.72))
        panel.center = (width // 2, int(height * 0.53))
        self.draw_input_box(panel)

        margin = panel.width // 18
        x = panel.left + margin
        max_width = panel.width - 2 * margin
        indent = text_font.size("- ")[0]
        y = panel.top + panel.height // 25

        for heading, lines in sections:
            head = head_font.render(heading, True, (255, 255, 0))
            self._screen.blit(head, (x, y))
            y += head.get_height() + 4
            for line in lines:
                parts = self.wrap_text(text_font, line, max_width - indent)
                for i, part in enumerate(parts):
                    prefix = "- " if i == 0 else ""
                    text = text_font.render(
                        prefix + part, True, (255, 255, 255)
                    )
                    pos_x = x if i == 0 else x + indent
                    self._screen.blit(text, (pos_x, y))
                    y += text.get_height() + 2
                y += 5
            y += 12

        hint = hint_font.render(
            "PRESS ESC OR CLICK TO GO BACK", True, (255, 255, 0)
        )
        self._screen.blit(
            hint,
            hint.get_rect(center=(width // 2, height - height // 14)),
        )
