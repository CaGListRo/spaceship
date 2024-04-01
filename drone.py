import settings as stgs
from projectile import PlayerProjectile

import pygame as pg


class Drone(pg.sprite.Sprite):
    def __init__(self, game, player_group, projectile_group, pos):
        super().__init__(player_group)
        self.game = game
        self.player_projectile_group = projectile_group
        self.state = "idle"
        self.animation = self.game.assets["drone/" + self.state].copy()
        self.image = self.animation.get_img()
        self.rect = self.image.get_rect(center = pos)
        self.drone_mask = pg.mask.from_surface(self.image)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2()
        self.flip_image = False
        self.shoot_timer = 0
        
        self.speed = 200
        self.health = 100

        self.laser_fire_rate = 0.5
        self.laser_damage = 10

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
    
    def create_mask(self):
        self.spaceship_mask = pg.mask.from_surface(self.image)

    def handle_animation(self, dt, move_x):
        old_state = self.state
        if (move_x[1] - move_x[0]) == 0:
            self.state = "idle"
        else:
            self.state = "curve"
        if old_state != self.state:
            self.animation = self.game.assets["drone/" + self.state].copy()
            self.rect = self.image.get_rect(center = self.pos)
            self.create_mask()

        self.flip_image = True if (move_x[1] - move_x[0]) > 0 else False
        self.auto_fire(dt)
        self.animation.update(dt)

        self.image = pg.transform.flip(self.animation.get_img(), self.flip_image, False)

    def update(self, dt, move_x=(0, 0), move_y=(0, 0)):
        self.handle_animation(dt, move_x)

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

    def auto_fire(self, dt):
        self.shoot_timer += dt
        if self.shoot_timer > max(0.1, self.laser_fire_rate):
            PlayerProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 25, self.pos.y + 42))
            self.shoot_timer = 0
                

