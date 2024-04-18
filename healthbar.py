import pygame as pg

class Healthbar:
    def __init__(self, game, max_health, current_health, image_width, sprite_pos, image_height=0):
        self.game = game
        self.max_health = max_health
        self.current_health = current_health
        self.img_width = image_width
        self.img_height = image_height
        self.healthbar_width = self.img_width * 0.9
        self.healthbar_height = 6
        self.healthbar_height_offset = self.healthbar_height if self.img_height == 0 else -20
        self.side_picker = -1 if self.img_height == 0 else 1
        self.center_pos = [0, 0]
        self.center_pos[0] = sprite_pos[0] + (self.img_width // 2)
        self.center_pos[1] = sprite_pos[1] + (self.side_picker * self.img_height) + 10 + self.healthbar_height_offset
        self.health_percent = self.current_health * 100 / self.max_health
        self.healthbar_length = round(self.health_percent * (self.healthbar_width - 2) / 100)
        self.game.healthbars.append(self)

    def update(self, current_health, sprite_pos):
        self.current_health = current_health
        self.center_pos[0] = sprite_pos[0] + (self.img_width // 2)
        self.center_pos[1] = sprite_pos[1] + (self.side_picker * self.img_height) + 10 + self.healthbar_height_offset
        self.health_percent = self.current_health * 100 / self.max_health
        self.healthbar_length = round(self.health_percent * (self.healthbar_width - 2) / 100)

    def draw(self, surf):
        pg.draw.rect(surf, "darkorange", (self.center_pos[0] - self.healthbar_width // 2, self.center_pos[1] - self.healthbar_height // 2, self.healthbar_width, self.healthbar_height))
        pg.draw.rect(surf, "red", (self.center_pos[0] - self.healthbar_width // 2 + 1, self.center_pos[1] - self.healthbar_height // 2 + 1, self.healthbar_width - 2, self.healthbar_height - 2))
        pg.draw.rect(surf, "green", (self.center_pos[0] - self.healthbar_width // 2 + 1, self.center_pos[1] - self.healthbar_height // 2 + 1, self.healthbar_length, self.healthbar_height - 2))