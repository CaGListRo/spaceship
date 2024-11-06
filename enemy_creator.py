import settings as stgs

from enemy import *
from typing import TypeVar

Game = TypeVar("Game")

def enemy_creator(game: Game, enemy_group: pg.sprite.Group, phase: int, wave: int, multiplicand: int) -> None:
    """
    Creates the waves of the enemy ships and bosses.
    Args:
    game (Game): The game object.
    enemy_group (pg.sprite.Group): The group of enemy sprites.
    phase (int): The current phase of the game.
    wave (int): The current wave of the enemy ships.
    multiplicand (int): The difficulty multiplicand (1, 2 or 3).
    """
    x_pos = stgs.GAME_WINDOW_RESOLUTION[0] // (len(stgs.enemy_waves[phase][wave]) + 1)  # x_pos for first ship
    for i in range(len(stgs.enemy_waves[phase][wave])):
        if stgs.enemy_waves[phase][wave][i] == 1:
            EnemyShip1(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 2:
            EnemyShip2(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 3:
            EnemyShip3(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 100:
            Boss1(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 120:
            Boss2(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 140:
            Boss3(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 160:
            Boss1(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 180:
            Boss2(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 200:
            Boss3(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 220:
            Boss1(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 240:
            Boss2(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
        elif stgs.enemy_waves[phase][wave][i] == 260:
            Boss3(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50), multiplicand)
