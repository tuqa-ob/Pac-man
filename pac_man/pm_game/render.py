import pygame
from .ghost import Ghost, GhostState
from pm_game.adapter import MazeAdapter
from pm_game.player import Player
from pathlib import Path


class Renderer:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    
    def __init__(self, screen: pygame.Surface, maze: MazeAdapter) -> None:
        self._screen = screen
        self._maze = maze
        self._cell_width = self._screen.get_width() // self._maze.width
        self._cell_height = self._screen.get_height() // self._maze.height
        self.cell_size = min(self._cell_width, self._cell_height)
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

    def draw_maze(self) -> None:
        cell = self.cell_size
        offset_x, offset_y = self.calculate_pos()
        maze_width = self._maze.width * cell
        maze_height = self._maze.height * cell
        maze_right = offset_x + maze_width - 1
        maze_bottom = offset_y + maze_height - 1
        for r in range(self._maze.height):
            for c in range(self._maze.width):
                if self._maze.has_wall(r, c, self.NORTH):
                    pygame.draw.line(
                        self._screen,
                        (255, 255, 255),
                        (offset_x + c * cell, offset_y + r * cell),
                        (offset_x + (c + 1 ) * cell, offset_y + r * cell))
                if self._maze.has_wall(r, c, self.EAST):
                    if c == self._maze.width - 1:
                        x = maze_right
                    else:
                        x = offset_x + (c + 1) * cell
                    pygame.draw.line(
                            self._screen,
                            (255, 255, 255),
                            (x, offset_y + r * cell),
                            (x, offset_y + (r + 1) * cell))
                if self._maze.has_wall(r, c, self.SOUTH):
                    if r == self._maze.height - 1:
                        y = maze_bottom 
                    else:
                        y = offset_y + (r + 1) * cell
                    pygame.draw.line(
                            self._screen,
                            (255, 255, 255),
                            (offset_x + c * cell, y),
                            (offset_x + (c + 1) * cell, y))
                if self._maze.has_wall(r, c, self.WEST):
                    pygame.draw.line(
                            self._screen,
                            (255, 255, 255),
                            (offset_x + c * cell, offset_y + r * cell),
                            (offset_x + c * cell, offset_y + (r + 1) * cell))

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
        self._cell_width = self._screen.get_width() // self._maze.width
        self._cell_height = self._screen.get_height() // self._maze.height
        self.cell_size = min(self._cell_width, self._cell_height)

    def draw_pac_gum(self, pacgums: set[tuple[int, int]]) -> None:
        offset_x, offset_y = self.calculate_pos()
        cell = self.cell_size
        for r, c in pacgums:
            x = offset_x + (c + 0.5) * cell
            y = offset_y + (r + 0.5) * cell
            pygame.draw.circle(
                    self._screen,
                    (255, 255, 255),
                    (x, y),
                    (cell // 10))

    def draw_super_pacgum(self,
                          pacgums: set[tuple[int, int]]
                          ) -> None:
        offset_x, offset_y = self.calculate_pos()
        cell = self.cell_size

        for r, c in pacgums:
            x = offset_x + (c + 0.5) * cell
            y = offset_y + (r + 0.5) * cell

            pygame.draw.circle(
                    self._screen,
                    (255, 105, 180),
                    (x, y),
                    cell // 5
                    )

    def draw_hud(self, score: int, lives: int, level: int) -> None:
        self.font = pygame.font.Font(None, 30)
        score_text = self.font.render(
                f"Score : {score}",
                True,
                (255, 255, 255))
        lives_text = self.font.render(
                f"Lives : {lives}",
                True,
                (255, 255, 255))
        level_text = self.font.render(
                f"Level : {level}",
                True,
                (255, 255, 255))

        self._screen.blit(score_text, (10, 10))
        self._screen.blit(lives_text, (200, 10))
        self._screen.blit(level_text, (350, 10))


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
        self._cell_width = (
            self._screen.get_width() // maze.width
        )
        self._cell_height = (
            self._screen.get_height() // maze.height
        )
        self.cell_size = min(
            self._cell_width,
            self._cell_height
        )



    def draw_game_over(self, score: int, player_name: str = "") -> None:
        """Draw the Game Over screen."""
        background = pygame.transform.scale(
            self.all_bg,
            self._screen.get_size(),
        )
        self._screen.blit(background, (0, 0))

        font = pygame.font.Font(None, 64)
        score_font = pygame.font.Font(None, 36)
        input_font = pygame.font.Font(None, 32)
        instruction_font = pygame.font.Font(None, 26)

        message = font.render("GAME OVER", True, (255, 0, 0))
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
            message,
            message.get_rect(center=(center_x, center_y - 110)),
        )
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
        pygame.draw.rect(
            self._screen, (60, 60, 80), input_rect, border_radius=5
        )
        pygame.draw.rect(
            self._screen, (255, 255, 0), input_rect, 2,
            border_radius=5,
        )
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
            self.all_bg,
            self._screen.get_size(),
        )
        self._screen.blit(background, (0, 0))


        font = pygame.font.Font(None, 64)
        score_font = pygame.font.Font(None, 36)
        input_font = pygame.font.Font(None, 32)
        instruction_font = pygame.font.Font(None, 26)

        message = font.render("YOU WIN!", True, (0, 255, 0))
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
            message,
            message.get_rect(center=(center_x, center_y - 110)),
        )
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
        pygame.draw.rect(
            self._screen, (60, 60, 80), input_rect, border_radius=5
        )
        pygame.draw.rect(
            self._screen, (255, 255, 0), input_rect, 2,
            border_radius=5,
        )
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


#     def draw_main_menu(
#         self,
#         rects: dict[str, pygame.Rect],
#         mouse_pos: tuple[int, int],
#         ) -> None:
# 
#         """Draw the main menu: background and pill buttons."""
#         width = self._screen.get_width()
#         height = self._screen.get_height()
# 
#         if self.menu_bg is not None:
#             background = pygame.transform.smoothscale(
#                 self.menu_bg, (width, height)
#             )
#             self._screen.blit(background, (0, 0))
# 
#         first = next(iter(rects.values()))
#         button_font = self.make_font(int(first.height * 0.75))
#         colors = [
#             (255, 255, 0),
#             (255, 192, 203),
#             (0, 0, 255),
#             (255, 128, 0),
#         ]
# 
#         for (name, rect), color in zip(rects.items(), colors):
#             hovered = rect.collidepoint(mouse_pos)
#             radius = rect.height // 2
#             thickness = max(3, rect.height // 11)
#             if hovered:
#                 thickness += 2
#             glass = pygame.Surface(rect.size, pygame.SRCALPHA)
#             area = glass.get_rect()
#             pygame.draw.rect(glass, (0, 0, 0, 90), area, border_radius=radius)
#             pygame.draw.rect(
#                 glass, color, area, thickness, border_radius=radius
#             )
#             self._screen.blit(glass, rect.topleft)
#             text_color = color if hovered else (255, 255, 255)
#             text = button_font.render(name.upper(), True, text_color)
#             self._screen.blit(text, text.get_rect(center=rect.center))

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




    def draw_highscores(
        self,
        entries: list[dict[str, str | int]],
    ) -> None:
        """Draw the top 10 highscores screen."""

        background = pygame.transform.scale(
            self.all_bg,
            self._screen.get_size(),
        )
        self._screen.blit(background, (0, 0))

        screen_width, screen_height = self._screen.get_size()

        title_font = pygame.font.Font(None, 64)
        entry_font = pygame.font.Font(None, 34)
        help_font = pygame.font.Font(None, 28)

        title = title_font.render(
            "HIGH SCORES",
            True,
            (255, 255, 0),
        )
        title_rect = title.get_rect(
            center=(screen_width // 2, 70),
        )
        self._screen.blit(title, title_rect)

        if not entries:
            message = entry_font.render(
                "No scores yet!",
                True,
                (255, 255, 255),
            )
            message_rect = message.get_rect(
                center=(screen_width // 2, screen_height // 2),
            )
            self._screen.blit(message, message_rect)

        else:
            start_y = 140
            line_height = 40

            for index, entry in enumerate(entries[:10]):
                name = str(entry["name"])
                score = int(entry["score"])

                line = entry_font.render(
                    f"{index + 1:>2}. {name:<10} {score:>6}",
                    True,
                    (255, 255, 255),
                )
                line_rect = line.get_rect(
                    center=(
                        screen_width // 2,
                        start_y + index * line_height,
                    ),
                )
                self._screen.blit(line, line_rect)

        help_text = help_font.render(
            "Press ESC to return to Main Menu",
            True,
            (0, 255, 255),
        )
        help_rect = help_text.get_rect(
            center=(
                screen_width // 2,
                screen_height - 40,
            ),
        )
        self._screen.blit(help_text, help_rect)

