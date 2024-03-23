import settings as stgs
from projectile import Projectile

import pygame as pg
from random import randint


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, health, enemy_group, projectile_group, pos):
        super().__init__(enemy_group)
        self.game = game
        self.health = int(health)
        self.score_factor = int(health)
        self.projectile_group = projectile_group
        self.image = pg.Surface((38, 50))
        color = 'red' if self.health == 1 else 'orange'
        self.image.fill(color)
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2()
        self.speed = 100
        self.shooting_timer = 1

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            self.game.score += 50 * self.score_factor

    def update(self, dt):
        self.direction.y = 1
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y > stgs.GAME_WINDOW_RESOLUTION[1]:
            self.kill()

        self.shoot(dt)

    def shoot(self, dt):
        self.shooting_timer -= dt
        if self.shooting_timer <= 0:
            self.shooting_timer = 1
            if randint(1, 100) > 80:
                Projectile(self.projectile_group, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() + 10), 1)