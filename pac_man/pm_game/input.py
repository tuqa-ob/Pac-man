import pygame
from .player import Player

def change_dir(player: Player, key: int) -> bool:
    move_player = False
    if key == pygame.K_UP or key == pygame.K_w:
        player.dir = Player.NORTH
        move_player = True
    elif key == pygame.K_DOWN or key == pygame.K_s:
        player.dir = Player.SOUTH
        move_player = True
    elif key == pygame.K_RIGHT or key == pygame.K_d:
        player.dir = Player.EAST
        move_player = True
    elif key == pygame.K_LEFT or key == pygame.K_a:
        player.dir = Player.WEST
        move_player = True
    return move_player

