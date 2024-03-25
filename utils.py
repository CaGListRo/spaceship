import os
import pygame as pg


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
    def __init__(self, image_list, animation_duration):
        self.img_list = image_list
        self.anim_dur = animation_duration
        self.current_frame = 0
        self.img_duration = animation_duration / len(image_list)
        self.img_timer = 0

    def copy(self):
        return Animation(self.img_list, self.anim_dur)

    def update(self, dt):
        self.img_timer += dt
        if self.img_timer >= self.img_duration:
            self.current_frame += 1
            self.img_timer = 0
            if self.current_frame > len(self.img_list)-1:
                self.current_frame = 0

    def get_img(self):
        return self.img_list[self.current_frame]