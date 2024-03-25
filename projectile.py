import settings as stgs

import pygame as pg


class Projectile(pg.sprite.Sprite):
    def __init__(self, group, pos, direction):
        super().__init__(group)
        self.image = pg.Surface((5, 10))
        self.image.fill("white")
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