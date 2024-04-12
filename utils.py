import os
import pygame as pg
from random import randint


BASE_PATH = "images/"

def load_image(path, imagename, scale_factor):
    img = pg.image.load(BASE_PATH + path + "/" + imagename).convert_alpha()
    return pg.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor))

def load_images(path, scale_factor):
    images = []
    for img_name in sorted(os.listdir(BASE_PATH + path)):  # sorted because of not Windows systems
        images.append(load_image(path + '/', img_name, scale_factor))
    return images


class Animation:
    def __init__(self, image_list, animation_duration, loop=True):
        self.img_list = list(image_list)
        self.anim_dur = animation_duration
        self.loop = loop
        self.done = False
        self.current_frame = 0
        self.img_duration = animation_duration / len(image_list)
        self.img_timer = 0

    def copy(self):
        return Animation(self.img_list, self.anim_dur, self.loop)

    def update(self, dt):
        self.img_timer += dt
        if self.img_timer >= self.img_duration and not self.done:
            self.current_frame += 1
            self.img_timer = 0
            if self.current_frame >= len(self.img_list):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.done = True

    def get_img(self):
        if 0 <= self.current_frame < len(self.img_list):
            return self.img_list[self.current_frame]
        else:
            return None
        

def help_site_creator(game, font):
    surf = pg.Surface((1600, 900))
    surf.set_colorkey("black")
    with open("help_text.txt", "r", encoding="utf-8") as file:
        text = file.read()
        lines = text.splitlines()
        for i, line in enumerate(lines):
            text = font.render(line, True, (247, 247, 247))
            surf.blit(text, (50, 50 + i * 50))
    for i, upgrade in enumerate(game.assets["upgrade/image"]):
        background_number = randint(0, 6)
        surf.blit(game.assets["upgrade/background"][background_number], (50 + i * 130, 400))
        surf.blit(upgrade, (50 + i * 130, 400))
    return surf