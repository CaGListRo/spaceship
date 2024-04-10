import settings as stgs

import pygame as pg
import math


class Projectile(pg.sprite.Sprite):
    def __init__(self, game, projectile_type, damage, group, pos, direction, laser_color=None, angle=90):
        super().__init__(group)
        self.game = game
        self.damage = damage
        color = self.color_picker(laser_color)
        self.angle = angle
        if self.angle != 90:
            self.image_rotate_angle = self.angle - 90
        self.animate = self.get_image(projectile_type, color)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = direction
        

    def get_image(self, type, color=None):
        if type == "laser":
            self.image = self.game.assets[type][color]
            if self.game.spaceship.weapon == "sprayer" and self.angle != 90:
                self.image = pg.transform.rotate(self.image, -self.image_rotate_angle)
            return False
        elif type == "rocket1":
            self.animation = self.game.assets[type].copy()
            self.image = self.animation.get_img()
            self.image = pg.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
            return True

    def color_picker(self, color):
        if color == "blue":
            return 0
        elif color == "green":
            return 1
        elif color == "orange":
            return 2
        elif color == "red":
            return 3
        else:
            return 4    

    def update(self, dt):
        if self.angle == 90:
            if self.animate:
                self.animation.update(dt)
                self.image = self.animation.get_img()
            self.pos.y += self.direction * self.speed * dt
        else:
            x_move = self.speed * dt * math.cos(math.radians(self.angle))
            y_move = self.speed * dt * math.sin(math.radians(self.angle))   
            self.pos.x -= x_move
            self.pos.y -= y_move

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y < -10 or self.pos.y > stgs.GAME_WINDOW_RESOLUTION[1] + 10:
            self.kill()
        
        if self.pos.x < -10 or self.pos.x > stgs.GAME_WINDOW_RESOLUTION[0] + 10:
            self.kill()


class PlayerProjectile(Projectile):
    def __init__(self, game, projectile_type, damage, pos, angle=90):
        super().__init__(game, projectile_type, damage, game.player_projectile_group, pos, direction=-1, laser_color="blue", angle=angle)
        self.speed = 250
        
    def get_image(self, type, color):
        super().get_image(type, color)

        if type == "rocket1":
            self.image = pg.transform.rotate(self.image, 180)


class EnemyProjectile(Projectile):
    def __init__(self, game, projectile_type, damage, pos, laser_color, angle=90):
        super().__init__(game, projectile_type, damage, game.enemy_projectile_group, pos, direction=1, laser_color=laser_color, angle=angle)
        self.speed = 150