import settings as stgs

from enemy import Enemy


def enemy_creator(game, enemy_group, projectile_group, phase, wave):
    # enemy_formation = randint(0, 4)
    x_pos = stgs.GAME_WINDOW_RESOLUTION[0] // (len(stgs.enemy_waves[phase][wave]) + 1)  # x_pos for first ship
    for i in range(len(stgs.enemy_waves[phase][wave])):
        Enemy(game, stgs.enemy_waves[phase][wave][i], enemy_group, projectile_group, (x_pos + x_pos * i, -50))