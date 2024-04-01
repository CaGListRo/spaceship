import pygame as pg

class ShipExplosion():
    def __init__(self, game, pos, rotate=180):
        self.rotate = rotate
        self.animation = game.assets["explosion"].copy()
        self.image = pg.transform.rotate(self.animation.get_img(), self.rotate)
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.speed = 50
        self.remove_explosion = False
        
    def update(self, dt):
        if self.animation.done:
            self.remove_explosion = True

        self.pos.y += self.speed * dt
        self.rect.y = self.pos.y

        self.animation.update(dt)
        self.image = self.animation.get_img()
        if self.image != None:
            self.image = pg.transform.rotate(self.image, self.rotate)

        return self.remove_explosion
    
    def draw(self, surf):
        if self.image != None:
            surf.blit(self.image, self.rect)
    

class SmallExplosion:
    def __init__(self, game, pos):
        self.animation = game.assets["projectile_hit"].copy()
        self.image = self.animation.get_img()
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.remove_hit = False
        
    def update(self, dt):
        if self.animation.done:
            self.remove_hit = True

        self.animation.update(dt)
        self.image = self.animation.get_img()

        return self.remove_hit
    
    def draw(self, surf):
        if self.image != None:
            surf.blit(self.image, self.rect)
