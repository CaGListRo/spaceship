import settings as stgs
from projectile import EnemyProjectile
from upgrades import Upgrade
from explosion import Explosion

import pygame as pg
from random import randint


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, ship_path, enemy_number, enemy_group, pos):
        super().__init__(enemy_group)
        self.game = game
        self.health = enemy_number * 50
        self.score_factor = enemy_number
        # self.enemy_projectile_group = projectile_group
        # self.upgrade_group = upgrade_group
        self.animation = self.game.assets[ship_path + "/idle"].copy()
        self.image = self.animation.get_img()
        self.rect = self.image.get_rect(center = pos)
        self.enemy_mask = pg.mask.from_surface(self.image)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2(0, 1)
        self.speed = 100

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            Upgrade(self.game, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() // 2))
            Explosion(self.game, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() + 20))
            self.game.score += 50 * self.score_factor

    def create_mask(self):
        self.enemy_mask = pg.mask.from_surface(self.image)

    def update(self, dt):
        self.animation.update(dt)
        self.image = self.animation.get_img()

        self.direction.y = 1
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y > stgs.GAME_WINDOW_RESOLUTION[1]:
            self.kill()
        


class EnemyShip1(Enemy):
    def __init__(self, game, enemy_number, enemy_group, pos):
        super().__init__(game, "enemy1", enemy_number, enemy_group, pos)
        self.shooting_timer = 1
        self.timer = self.shooting_timer
        self.laser_damage = 10
    
    def update(self, dt):
        super().update(dt)
        self.shoot(dt)

    def shoot(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.shooting_timer
            if randint(1, 100) > 80:
                EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() + 10), "red")


class EnemyShip2(Enemy):
    def __init__(self, game,  enemy_number, enemy_group, pos):
        super().__init__(game, "enemy2", enemy_number, enemy_group, pos)
        self.shooting_timer = 0.8
        self.timer = self.shooting_timer
        self.laser_damage = 5
    
    def update(self, dt):
        super().update(dt)
        self.shoot(dt)

    def shoot(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.shooting_timer
            if randint(1, 100) > 80:
                EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2 - 10, self.pos.y + self.image.get_height() + 10), "green")
                EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2 + 10, self.pos.y + self.image.get_height() + 10), "green")


class EnemyShip3(Enemy):
    def __init__(self, game,  enemy_number, enemy_group, pos):
        super().__init__(game, "enemy3", enemy_number, enemy_group, pos)
        self.shooting_timer = 2
        self.timer = self.shooting_timer
        self.rocket_damage = 50

    def update(self, dt):
        super().update(dt)
        self.shoot(dt)

    def shoot(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.shooting_timer
            if randint(1, 100) > 80:
                EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + self.image.get_width() // 2 + 10, self.pos.y + self.image.get_height() + 10), "green")


class Boss1(Enemy):
    def __init__(self, game,  enemy_number, enemy_group, pos):
        super().__init__(game, "boss1", enemy_number, enemy_group, pos)