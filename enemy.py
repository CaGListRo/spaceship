import settings as stgs

import pygame as pg


class Enemy(pg.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = pg.Surface((38, 50))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2()
        self.speed = 150

    def update(self, dt):
        self.direction.y = 1
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y > stgs.GAME_WINDOW_RESOLUTION[1]:
            self.kill()