import settings as stgs

import pygame as pg


class Projectile(pg.sprite.Sprite):
    def __init__(self, game, p_type, group, pos, direction):
        super().__init__(group)
        image_count = 3 if direction > 0 else 1
        # self.game = game
        self.image = game.assets[p_type][image_count]
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = direction
        self.speed = 150 if direction > 0 else 250

    def update(self, dt):
        self.pos.y += self.direction * self.speed * dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y < -10 or self.pos.x < -10 or self.pos.x > stgs.GAME_WINDOW_RESOLUTION[0] + 10:
            self.kill()


class PlayerProjectile(Projectile):
    def __init__(self, game, p_type, group, pos):
        super().__init__(game, p_type, group, pos, direction=-1)


class EnemyProjectile(Projectile):
    def __init__(self, game, p_type, group, pos):
        super().__init__(game, p_type, group, pos, direction=1)