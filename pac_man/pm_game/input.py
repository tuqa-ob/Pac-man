import pygame
from .player import Player
from .direction import Direction

def change_dir(player: Player, key: int) -> bool:
    move_player = False
    if key == pygame.K_UP or key == pygame.K_w:
        player.dir = Direction.UP
        move_player = True
    elif key == pygame.K_DOWN or key == pygame.K_s:
        player.dir = Direction.DOWN
        move_player = True
    elif key == pygame.K_RIGHT or key == pygame.K_d:
        player.dir = Direction.RIGHT
        move_player = True
    elif key == pygame.K_LEFT or key == pygame.K_a:
        player.dir = Direction.LEFT
        move_player = True
    return move_player

