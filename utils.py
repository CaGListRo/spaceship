import settings as stgs

from enemy import Enemy

import pygame as pg
from random import randint

formations = [
    [1, 1],
    [1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
]

def enemy_creator(enemy_group, projectile_group):
    enemy_formation = randint(0, 4)
    x_pos = stgs.GAME_WINDOW_RESOLUTION[0] // (len(formations[enemy_formation]) + 1)  # x_pos for first ship
    for i in range(len(formations[enemy_formation])):
        Enemy(enemy_group, projectile_group, (x_pos + x_pos * i, -50))
    