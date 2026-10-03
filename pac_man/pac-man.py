import sys
import pygame
from pm_game.config import Config
from pm_game.game import Game
from pm_game.player import Player
from pm_game.input import change_dir
from pm_game.render import Renderer


def main() -> None:
    """main entry point to pac-man game"""
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config_file.json>")
        sys.exit(1)
    config_path = sys.argv[1]
    print(f"Loading game with config : {config_path}")
    config = Config(config_path)
    game = Game(config)
    game.load_level()
    file_name = config.get("highscore_filename")
    lives = config.get("lives")
    seed = config.get("seed")

    print("Game Settings Loaded Successfully:")
    print(f" - Initial Lives: {lives}")
    print(f" - Maze Seed: {seed}")
    print(game.player.curr_row, game.player.curr_col)
    pygame.init()
    screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    renderer = Renderer(screen, game.maze)
    print(renderer.cell_size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                renderer.update_screen(screen)
            elif event.type == pygame.KEYDOWN:
                if change_dir(game.player, event.key):
                    game.move_player()
                print(game.player.curr_row, game.player.curr_col)
        screen.fill((0, 0, 0))
        renderer.draw_maze()
        renderer.draw_player(game.player)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
