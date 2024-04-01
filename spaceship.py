import settings as stgs
from projectile import PlayerProjectile

import pygame as pg


class Spaceship(pg.sprite.Sprite):
    def __init__(self, game, player_group, projectile_group, pos):
        super().__init__(player_group)
        self.game = game
        self.player_projectile_group = projectile_group
        self.state = "idle"
        self.weapon = "laser"
        self.animation = self.game.assets["ship/" + self.state].copy()
        self.ship_image = self.animation.get_img()
        self.weapon_image = self.game.assets[self.weapon + "/" + self.state]
        self.image = pg.Surface((self.ship_image.get_width(), self.ship_image.get_height()))
        self.image.blit(self.weapon_image, (0, 0))
        self.image.blit(self.ship_image, (0, 0))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect(center = pos)
        self.spaceship_mask = pg.mask.from_surface(self.image)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2()
        self.flip_image = False
        self.shoot_timer = 0
        
        self.speed = 200
        self.health = 100

        
        self.laser_fire_rate = 0.5
        self.rocket_fire_rate = 1
        self.laser_damage = 10
        self.rocket_damage = 50
        self.current_weapon_damage = self.laser_damage

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
    
    def create_mask(self):
        self.spaceship_mask = pg.mask.from_surface(self.ship_image)

    def handle_animation(self, dt, move_x):
        old_state = self.state
        if (move_x[1] - move_x[0]) == 0:
            self.state = "idle"
        else:
            self.state = "curve"
        if old_state != self.state:
            self.animation = self.game.assets["ship/" + self.state].copy()
            self.rect = self.ship_image.get_rect(center = self.pos)
            self.create_mask()

        self.flip_image = True if (move_x[1] - move_x[0]) > 0 else False
        self.auto_fire(dt)
        self.animation.update(dt)

        self.ship_image = self.animation.get_img()
        self.weapon_image = self.game.assets[self.weapon + "/" + self.state]
        self.image.fill("black")
        self.image.blit(self.weapon_image, (0, 0))
        self.image.blit(self.ship_image, (0, 0))
        self.image = pg.transform.flip(self.image, self.flip_image, False)

    def update(self, dt, move_x=(0, 0), move_y=(0, 0)):
        self.handle_animation(dt, move_x)

        self.pos.x += (move_x[1] - move_x[0]) * self.speed * dt
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x + self.ship_image.get_width()> stgs.GAME_WINDOW_RESOLUTION[0]:
            self.pos.x = stgs.GAME_WINDOW_RESOLUTION[0]  - self.ship_image.get_width()
        self.rect.x = self.pos.x

        self.pos.y += (move_y[1] - move_y[0]) * self.speed *dt
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y + self.ship_image.get_height() > stgs.GAME_WINDOW_RESOLUTION[1]:
            self.pos.y = stgs.GAME_WINDOW_RESOLUTION[1]  - self.ship_image.get_height()
        self.rect.y = self.pos.y

    def auto_fire(self, dt):
        self.shoot_timer += dt
        if self.weapon == "laser":
            if self.shoot_timer > max(0.1, self.laser_fire_rate):
                PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + 25, self.pos.y + 42))
                PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + 74, self.pos.y + 42))
                self.shoot_timer = 0
        elif self.weapon == "rocket_launcher":
            if self.shoot_timer > max(0.1, self.laser_fire_rate):
                PlayerProjectile(self.game, "rocket1", self.current_weapon_damage, (self.pos.x + 25, self.pos.y + 42))
                PlayerProjectile(self.game, "rocket1", self.current_weapon_damage, (self.pos.x + 74, self.pos.y + 42))
                self.shoot_timer = 0
        elif self.weapon == "sprayer":
            if self.shoot_timer > max(0.1, self.laser_fire_rate):
                PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + 25, self.pos.y + 42))
                PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + 74, self.pos.y + 42))
                self.shoot_timer = 0

