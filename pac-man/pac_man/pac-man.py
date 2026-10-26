import sys
import signal
import pygame
import types
from pm_game.config import Config
from pm_game.game import Game
from pm_game.input import change_dir
from pm_game.render import Renderer
from pm_game.highscore import Highscore
from pm_game.menu import (
    get_clicked_button,
    get_instructions,
    make_pause_rects,
    make_rects,
)


def handle_exit_signal(signum: int, frame: types.FrameType | None) -> None:
    raise KeyboardInterrupt


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

    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

    renderer = Renderer(screen, game.maze)
    rects = make_rects(screen.get_width(), screen.get_height())
    state = "menu"

    clock = pygame.time.Clock()
    time_limit = config.get("level_max_time")
    elapsed_time = 0.0
    instructions = get_instructions(config)

    running = True

    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
                renderer.update_screen(screen)
                rects = make_rects(event.w, event.h)

            elif event.type == pygame.MOUSEBUTTONDOWN and state == "menu":
                choice = get_clicked_button(rects, event.pos)
                if choice == "Start Game":
                    game = Game(config)
                    game.load_level()
                    elapsed_time = 0.0
                    renderer.update_maze(game.maze)
                    state = "playing"
                elif choice == "High Scores":
                    state = "highscores"
                elif choice == "Instructions":
                    state = "instructions"
                elif choice == "Exit Game":
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and state == "playing":
                if renderer.pause_button_rect().collidepoint(event.pos):
                    state = "paused"

            elif event.type == pygame.MOUSEBUTTONDOWN and state == "paused":
                pause_rects = make_pause_rects(
                    screen.get_width(), screen.get_height()
                )
                choice = get_clicked_button(pause_rects, event.pos)
                if choice == "Resume":
                    state = "playing"
                elif choice == "Exit":
                    game.game_over = True
                    state = "playing"

            elif (event.type == pygame.MOUSEBUTTONDOWN and
                  state in ("highscores", "instructions")):
                state = "menu"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and (
                        event.mod & pygame.KMOD_CTRL):
                    running = False

                elif state in ("highscores", "instructions"):
                    if event.key == pygame.K_ESCAPE:
                        state = "menu"

                elif game.entering_name:
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

                elif (state == "playing"
                      and not game.game_over
                      and not game.game_won):
                    if event.key == pygame.K_c:
                        game.toggle_cheat_mode()
                    elif game.cheat_mode and event.key == pygame.K_l:
                        game.skip_level()
                        renderer.update_maze(game.maze)
                        elapsed_time = 0.0
                    elif game.cheat_mode and event.key == pygame.K_e:
                        game.lives += 1
                    elif game.cheat_mode and event.key == pygame.K_i:
                        game.invincible = not game.invincible
                    elif game.cheat_mode and event.key == pygame.K_f:
                        game.ghosts_frozen = not game.ghosts_frozen
                    elif game.cheat_mode and event.key == pygame.K_b:
                        game.speed_boost = not game.speed_boost
                    elif change_dir(game.player, event.key):
                        game.move_player()
                        if game.speed_boost:
                            game.move_player()

        if state == "playing" and (game.game_over or game.game_won):
            game.entering_name = True

        if state == "playing" and not game.game_over and not game.game_won:
            if not game.ghosts_frozen:
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
                elapsed_time = 0.0

        screen.fill((4, 8, 28))

        if state == "playing" and not game.game_over and not game.game_won:
            elapsed_time += dt
            if elapsed_time >= time_limit:
                game.game_over = True

        if state == "menu":
            renderer.draw_main_menu(rects, pygame.mouse.get_pos())

        elif state == "highscores":
            renderer.draw_highscores(highscore.top())

        elif state == "instructions":
            renderer.draw_instructions(instructions)

        elif game.game_over:
            renderer.draw_game_over(game.score, game.player_name)

        elif game.game_won:
            renderer.draw_victory(game.score, game.player_name)

        else:
            renderer.draw_maze()
            renderer.draw_pac_gum(game.level.pacgum_positions)
            renderer.draw_super_pacgum(
                    game.level.super_pacgum_positions)
            renderer.draw_player(game.player)
            renderer.draw_pause_button(pygame.mouse.get_pos())
            renderer.draw_hud(
                game.score,
                game.lives,
                game.current_level,
                max(0.0, time_limit - elapsed_time),
            )
            if game.cheat_mode:
                renderer.draw_cheat_help(game.cheat_lines())
            for ghost in game.ghosts:
                renderer.draw_ghost(ghost)

        if state == "paused":
            renderer.draw_pause_menu(
                make_pause_rects(screen.get_width(), screen.get_height()),
                pygame.mouse.get_pos(),
            )

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    signal.signal(signal.SIGTSTP, handle_exit_signal)
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
