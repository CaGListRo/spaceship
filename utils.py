import os
import pygame as pg


BASE_PATH = "images/"

def load_image(path, imagename):
    return pg.image.load(BASE_PATH + path + "/" + imagename + ".png").convert_alpha()

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_PATH + path)):  # sorted because of not Windows systems
        images.append(load_image(path + '/' + img_name))
    return images