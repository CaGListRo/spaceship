import settings as stgs

from enemy import *


def enemy_creator(game, enemy_group, phase, wave):
    # enemy_formation = randint(0, 4)
    x_pos = stgs.GAME_WINDOW_RESOLUTION[0] // (len(stgs.enemy_waves[phase][wave]) + 1)  # x_pos for first ship
    for i in range(len(stgs.enemy_waves[phase][wave])):
        if stgs.enemy_waves[phase][wave][i] == 1:
            EnemyShip1(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50))
        if stgs.enemy_waves[phase][wave][i] == 2:
            EnemyShip2(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50))
        if stgs.enemy_waves[phase][wave][i] == 3:
            EnemyShip3(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50))
        if stgs.enemy_waves[phase][wave][i] >= 100:
            Boss1(game, stgs.enemy_waves[phase][wave][i], enemy_group, (x_pos + x_pos * i, -50))
