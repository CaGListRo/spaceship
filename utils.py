import settings as stgs

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

def create_highscore_screen(font):
    surf = pg.Surface((1600, 900))
    surf.set_colorkey("black")
    highscore_list = []
    with open("highscore_list.txt", "r", encoding="utf-8") as file:
        text = file.read()
        lines = text.splitlines()
        for i, line in enumerate(lines):
            word = line.split(" ")
            number_to_render = f"{str(i+1)}."
            number_to_blit = font.render(number_to_render, True, (247, 247, 247))
            surf.blit(number_to_blit, (450, 100 + i * 60))
            name_to_render = word[0]
            name_to_blit = font.render(name_to_render, True, (247, 247, 247))
            surf.blit(name_to_blit, (600, 100 + i * 60))
            score_to_render = word[1]
            score_to_blit = font.render(score_to_render, True, (247, 247, 247))
            surf.blit(score_to_blit, (950, 100 + i * 60))
            highscore_list.append([word[0], int(word[1])])
    return surf, highscore_list

def sort_and_write_highscore(highscore_list, name, score):
    highscore_list.append([str(name), int(score)])

    while True:
        bubbled = False
        for i in range(len(highscore_list)-1):  
            if highscore_list[i][1] < highscore_list[i+1][1]:
                highscore_list[i+1], highscore_list[i] = highscore_list[i], highscore_list[i+1]
                bubbled = True
                
        if not bubbled:
            break

    highscore_list.pop(-1)

    with open("highscore_list.txt", "w", encoding="utf-8") as file:
        for i in range(10):
            for j in range(2):
                
                file.write(str(highscore_list[i][j]))
                if j == 0:
                    file.write(" ")
                if j == 1:
                    file.write("\n")


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
        

class Helpsite:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.SysFont("comicsans", 32)
        self.surface = pg.Surface((1600, 900))
        self.surface.fill((111, 111, 111))
        self.surface.set_colorkey((111, 111, 111))
        self.text_surf = pg.Surface((530, 150))
        self.text_surf.fill((111, 111, 111))
        self.text_surf.set_colorkey((111, 111, 111))
        self.mouse_pos = pg.mouse.get_pos()
        self.upgrade_rect_list = []
        self.rect_width_height = self.game.assets["upgrade/background"][0].get_width()
        self.text_list = []
        self.text_number = -1
        self.generate_background_numbers()
        self.load_upgrade_texts()
        self.draw_help_text()
        self.draw_upgrades()

    def generate_background_numbers(self):
        self.background_numbers = [randint(0, 6) for _ in range(11)]

    def draw_help_text(self):       
        with open("help_text.txt", "r", encoding="utf-8") as file:
            text = file.read()
            lines = text.splitlines()
            for i, line in enumerate(lines):
                text = self.font.render(line, True, (247, 247, 247))
                self.surface.blit(text, (50, 50 + i * 50))

    def draw_upgrades(self):
        self.upgrade_rect_list = []
        for i, upgrade in enumerate(self.game.assets["upgrade/image"]):
            self.surface.blit(self.game.assets["upgrade/background"][self.background_numbers[i]], (50 + i * 130, 420))
            self.surface.blit(upgrade, (50 + i * 130, 420))
            self.upgrade_rect_list.append(pg.Rect(50 + i * 130, 420, self.rect_width_height, self.rect_width_height))

    def check_rect_collision(self):
        self.mouse_pos = pg.mouse.get_pos()
        for i, rect in enumerate(self.upgrade_rect_list):
            if rect.collidepoint(self.mouse_pos):
                return i
        return -1
    
    def handle_upgrade_texts(self):
        self.text_number = self.check_rect_collision()
        self.text_surf.fill((111, 111, 111))
        for i, line in enumerate(self.text_list[self.text_number]):
            line_to_blit = self.font.render(line, True, (247, 247, 247))
            self.text_surf.blit(line_to_blit, (0, 0 + i * 50))


    def load_upgrade_texts(self):        
        with open("upgrade_texts.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            help_list = []
            for line in lines:         
                if line == "\n":
                    self.text_list.append(help_list)
                    help_list = []
                elif line:
                    line = line.strip()
                    help_list.append(line)
            self.text_list.append(help_list)

    def update(self):
        self.surface.fill((111, 111, 111))
        self.handle_upgrade_texts()
        self.draw_help_text()
        self.draw_upgrades()

    def render(self, surf):
        
        if self.text_number != -1:
            if self.mouse_pos[0] + self.text_surf.get_width() > stgs.MAIN_WINDOW_RESOLUTION[0]:
                
                self.mouse_pos = (stgs.MAIN_WINDOW_RESOLUTION[0] - self.text_surf.get_width(), self.mouse_pos[1])
            self.surface.blit(self.text_surf, self.mouse_pos)
        surf.blit(self.surface, (0, 0))
        