import settings as stgs

import pygame as pg


class Spaceship(pg.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pg.Surface((38, 50))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2()
        self.speed = 300

    def update(self, dt, move_x=(0, 0), move_y=(0, 0)):
        self.pos.x += (move_x[1] - move_x[0]) * self.speed * dt
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x + self.image.get_width()> stgs.GAME_WINDOW_RESOLUTION[0]:
            self.pos.x = stgs.GAME_WINDOW_RESOLUTION[0]  - self.image.get_width()
        self.rect.x = self.pos.x

        self.pos.y += (move_y[1] - move_y[0]) * self.speed *dt
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y + self.image.get_height() > stgs.GAME_WINDOW_RESOLUTION[1]:
            self.pos.y = stgs.GAME_WINDOW_RESOLUTION[1]  - self.image.get_height()
        self.rect.y = self.pos.y
