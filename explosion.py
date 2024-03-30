import pygame as pg

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, pos, rotate=180):
        super().__init__(game.fx_group)
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
        self.image = pg.transform.rotate(self.animation.get_img(), self.rotate)

        return self.remove_explosion
