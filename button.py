import settings as stgs

import pygame as pg


class Button:
    def __init__(self, surf, text, pos):
        self.surface = surf
        self.text = text
        self.pos = list(pos)
        self.button_size = (300, 50)
        self.button_offset = 5
        self.font = pg.font.SysFont('comicsans', 32)
        self.button_top_rect = pg.Rect(self.pos[0] - self.button_size[0] // 2, self.pos[1] - self.button_size[1] // 2 - self.button_offset, self.button_size[0], self.button_size[1])
        self.button_bottom_rect = pg.Rect(self.pos[0] - self.button_size[0] // 2, self.pos[1] - self.button_size[1] // 2, self.button_size[0], self.button_size[1])
        self.button_top_color = ((244, 164, 96))
        self.color2 = ((222, 184, 135))
        self.button_bottom_color = ((210, 180, 140))
        self.color4 = ((194, 178, 128))
        self.clicked = False

    def render(self):
        pg.draw.rect(self.surface, "black", (self.button_bottom_rect[0] - 2, self.button_bottom_rect[1] - 2, self.button_size[0] + 4, self.button_size[1] + 4), border_radius=5)
        pg.draw.rect(self.surface, self.button_bottom_color, self.button_bottom_rect, border_radius=5)
        pg.draw.rect(self.surface, self.button_top_color, self.button_top_rect, border_radius=5)
        pg.draw.rect(self.surface, "black", self.button_top_rect, border_radius=5, width=2)
        button_label = self.font.render(self.text, True, "black")
        self.surface.blit(button_label, (self.pos[0] - button_label.get_width() // 2, self.pos[1] - button_label.get_height() // 2 - self.button_offset))

    def check_button_collision(self):
        mouse_pos = pg.mouse.get_pos()
        if self.button_top_rect.collidepoint(mouse_pos):
            self.button_top_color = self.color2
            if pg.mouse.get_pressed()[0]:
                self.button_offset = 0
                self.clicked = True
            else:
                self.button_offset = 5
                if self.clicked == True:
                    self.clicked = False
        else:
            self.button_top_color = ((244, 164, 96))
            self.clicked = False
        return self.clicked