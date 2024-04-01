import settings as stgs

import pygame as pg


class Projectile(pg.sprite.Sprite):
    def __init__(self, game, projectile_type, damage, group, pos, direction, laser_color=None):
        super().__init__(group)
        self.game = game
        self.damage = damage
        color = self.color_picker(laser_color)
        self.animate = self.get_image(projectile_type, color)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = direction
        

    def get_image(self, type, color):
        if type == "laser":
            self.image = self.game.assets[type][color]
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
        if self.animate:
            self.animation.update(dt)
            self.image = self.animation.get_img()
        self.pos.y += self.direction * self.speed * dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y < -10 or self.pos.x < -10 or self.pos.x > stgs.GAME_WINDOW_RESOLUTION[0] + 10:
            self.kill()


class PlayerProjectile(Projectile):
    def __init__(self, game, projectile_type, damage, pos):
        super().__init__(game, projectile_type, damage, game.player_projectile_group, pos, direction=-1, laser_color="blue")
        self.speed = 250
        
    def get_image(self, type, color):
        super().get_image(type, color)

        if type == "rocket1":
            self.image = pg.transform.rotate(self.image, 180)


class EnemyProjectile(Projectile):
    def __init__(self, game, projectile_type, damage, pos, laser_color):
        super().__init__(game, projectile_type, damage, game.enemy_projectile_group, pos, direction=1, laser_color=laser_color)
        self.speed = 150