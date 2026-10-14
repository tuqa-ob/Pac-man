import sys
import pygame
from pm_game.config import Config
from pm_game.game import Game
from pm_game.player import Player
from pm_game.input import change_dir
from pm_game.render import Renderer
from pm_game.highscore import Highscore
from pm_game.menu import BUTTONS, get_clicked_button, make_rects


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
    highscore = Highscore(file_name)
    
    print("Game Settings Loaded Successfully:")
    print(f" - Initial Lives: {lives}")
    print(f" - Maze Seed: {seed}")
    print(game.player.curr_row, game.player.curr_col)
    
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    
    renderer = Renderer(screen, game.maze)
    rects = make_rects(screen.get_width(), screen.get_height())
    state = "menu"

    print(renderer.cell_size)
    print(len(game.level.pacgum_positions))
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                renderer.update_screen(screen)
                rects = make_rects(event.w, event.h)

            elif event.type == pygame.MOUSEBUTTONDOWN and state == "menu":
                choice = get_clicked_button(rects, event.pos)
                if choice == "Start Game":
                    state = "playing"
                    print("DEBUG: state changed to playyyy")
                elif choice == "High Score":
                    state = "highscores"
                    print("DEBUG: state changed to highscores")
                elif choice == "Exit Game":
                    print("DEBUG: state changed to xxxxxxxxxxx")
                    running = False

            elif event.type == pygame.KEYDOWN:

                if game.entering_name:
                    if event.key == pygame.K_BACKSPACE:
                        game.player_name = game.player_name[:-1]

                    elif event.key == pygame.K_RETURN:
                        highscore.add_score(game.player_name, game.score)
                        game.entering_name = False
                        state = "menu"

                    elif (event.unicode
                          and event.unicode.isprintable()
                          and (event.unicode.isalnum()
                               or event.unicode == " ")
                          and len(game.player_name) < 10
                          ):
                        game.player_name += event.unicode

                elif state == "playing" and not game.game_over and not game.game_won:
                    if change_dir(game.player, event.key):
                        game.move_player()

                        print(game.player.curr_row, game.player.curr_col)
                        print(game.score)
                        print(game.lives)

        if game.game_over or game.game_won:
            game.entering_name = True

        if state == "playing" and not game.game_over and not game.game_won:
            for ghost in game.ghosts:
                ghost.update(
                        dt,
                        game.level,
                        game.player.curr_row,
                        game.player.curr_col
                        )
            game.check_collisions()

        if not game.game_won:
            if game.advance_level_if_cleared():
                renderer.update_maze(game.maze)

        screen.fill((0, 0, 0))

        if state == "menu":
            renderer.draw_main_menu(rects, pygame.mouse.get_pos())
        elif state == "highscores":
            renderer.draw_highscores(highscore.top())
        elif game.game_over:
            renderer.draw_game_over(game.score, game.player_name)
        elif game.game_won:
            renderer.draw_victory(game.score, game.player_name)
        else:
            renderer.draw_pac_gum(game.level.pacgum_positions)
            renderer.draw_super_pacgum(
                    game.level.super_pacgum_positions)
            renderer.draw_maze()
            renderer.draw_player(game.player)
            renderer.draw_hud(game.score, game.lives, game.current_level)
            for ghost in game.ghosts:
                renderer.draw_ghost(ghost)

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
