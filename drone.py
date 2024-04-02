import settings as stgs
from projectile import PlayerProjectile

import pygame as pg


class Drone(pg.sprite.Sprite):
    def __init__(self, game, player_group, projectile_group, side):
        super().__init__(player_group)
        self.game = game
        self.player_projectile_group = projectile_group
        self.state = "idle"
        self.side = side
        self.animation = self.game.assets["drone/" + self.state].copy()
        self.image = self.animation.get_img()
        self.x_pos = self.game.spaceship.image.get_width() // 2 if self.side < 0 else round(self.game.spaceship.image.get_width() * 1.5) - self.image.get_width()
        self.pos = pg.math.Vector2(self.game.spaceship.pos.x + (self.x_pos * self.side), self.game.spaceship.pos.y + (self.game.spaceship.image.get_height() // 2))
        self.rect = self.image.get_rect(center = self.pos)
        self.drone_mask = pg.mask.from_surface(self.image)
        
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
        self.x_pos = self.game.spaceship.image.get_width() // 2 if self.side < 0 else round(self.game.spaceship.image.get_width() * 1.5) - self.image.get_width()
        self.pos = pg.math.Vector2(self.game.spaceship.pos.x + (self.x_pos * self.side), self.game.spaceship.pos.y + (self.game.spaceship.image.get_height() // 2))
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def auto_fire(self, dt):
        self.shoot_timer += dt
        if self.shoot_timer > max(0.1, self.laser_fire_rate):
            PlayerProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 5))
            self.shoot_timer = 0
                
