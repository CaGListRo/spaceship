import settings as stgs

import pygame as pg
from random import randint, choice


class Upgrade(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.upgrade_group)
        background_number = randint(0, 6)
        self.upgrade_number = randint(0, 10)
        self.image = pg.Surface((50, 50))  # depends on the scale factor
        self.image.set_colorkey("black")
        self.image.blit(game.assets["upgrade/background"][background_number], (0, 0))
        self.image.blit(game.assets["upgrade/image"][int(self.upgrade_number)], (0, 0))
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.mask = pg.mask.from_surface(self.image)
        self.speed = 50

    def update(self, dt):
        self.pos.y += self.speed * dt
        self.rect.y = self.pos.y

        if self.rect.top > stgs.GAME_WINDOW_RESOLUTION[1]:
            self.kill()