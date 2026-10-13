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
        pygame.draw.circle(
                self._screen,
                (255, 255, 0),
                (x, y),
                (cell // 3))

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

    def draw_main_menu(self, rects: dict[str, pygame.Rect]) -> None:
        """Draw the main menu: title, buttons and tagline."""

        width = self._screen.get_width()
        height = self._screen.get_height()
        
        if self.menu_bg is not None:

            background = pygame.transform.smoothscale(
                self.menu_bg, (width, height)
            )
            self._screen.blit(background, (0, 0))

        title_font = pygame.font.Font(None, height // 6)
        button_font = pygame.font.Font(None, height // 14)
        tag_font = pygame.font.Font(None, height // 28)
        colors = [
            (255, 255, 0),
            (255, 192, 203),
            (0, 0, 255),
            (255, 128, 0),
        ]

        title = title_font.render("PAC-MAN", True, (255, 255, 0))
        self._screen.blit(
            title,
            title.get_rect(center=(width // 2, height // 6)),
        )
        for (name, rect), color in zip(rects.items(), colors):
            pygame.draw.rect(
                self._screen,
                color,
                rect,
                4,
                border_radius=rect.height // 2,
            )
            text = button_font.render(name.upper(), True, (255, 255, 255))
            self._screen.blit(text, text.get_rect(center=rect.center))

        tagline = tag_font.render(
            "EAT ALL DOTS - AVOID THE GHOSTS - BE THE CHAMPION!",
            True,
            (255, 255, 0),
        )
        self._screen.blit(
            tagline,
            tagline.get_rect(center=(width // 2, height - height // 12)),
        )




