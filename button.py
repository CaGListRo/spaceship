import settings as stgs

import pygame as pg
from typing import Final


class Button:
    BUTTON_SIZE: Final[tuple[int]] = (300, 50)
    BUTTON_OFFSET: Final[int] = 5
    BUTTON_TOP_COLOR: Final[tuple[int]] = (244, 164, 96)
    BUTTON_HOVER_COLOR: Final[tuple[int]] = (222, 184, 135)
    BUTTON_BOTTOM_COLOR: Final[tuple[int]] = (210, 180, 140)
    BUTTON_SHADOW_COLOR: Final[tuple[int]] = (55, 55, 55)

    def __init__(self, surf: pg.Surface, text: str, pos: tuple[int]) -> None:
        """
        Initializes an button object.
        Args:
        surf (pg.Surface): The surface to draw the button on.
        text (str): The text to display on the button.
        pos (tuple[int]): The position of the button.
        """
        self.surface: pg.Surface = surf
        self.text: str = text
        self.pos: list[int] = list(pos)        
        self.font: pg.font.Font = pg.font.SysFont('comicsans', 32)
        self.button_top_rect: pg.Rect = pg.Rect(self.pos[0] - self.BUTTON_SIZE[0] // 2, self.pos[1] - self.BUTTON_SIZE[1] // 2 - self.BUTTON_OFFSET, self.BUTTON_SIZE[0], self.BUTTON_SIZE[1])
        self.button_bottom_rect: pg.Rect = pg.Rect(self.pos[0] - self.BUTTON_SIZE[0] // 2, self.pos[1] - self.BUTTON_SIZE[1] // 2, self.BUTTON_SIZE[0], self.BUTTON_SIZE[1])       
        self.clicked: bool = False
        self.button_color: tuple[int] = self.BUTTON_TOP_COLOR
        self.offset: int = self.BUTTON_OFFSET

    def render(self) -> None:
        """ Renders the button on the screen. """
        pg.draw.rect(self.surface, self.BUTTON_SHADOW_COLOR, (self.button_bottom_rect[0] - 2, self.button_bottom_rect[1] - 2, self.BUTTON_SIZE[0] + 4, self.BUTTON_SIZE[1] + 4), border_radius=5)
        pg.draw.rect(self.surface, self.BUTTON_BOTTOM_COLOR, self.button_bottom_rect, border_radius=5)
        pg.draw.rect(self.surface, self.BUTTON_TOP_COLOR, (self.pos[0] - self.BUTTON_SIZE[0] // 2, self.pos[1] - self.BUTTON_SIZE[1] // 2 - self.BUTTON_OFFSET, self.BUTTON_SIZE[0], self.BUTTON_SIZE[1]), border_radius=5)
        pg.draw.rect(self.surface, self.BUTTON_SHADOW_COLOR, self.button_top_rect, border_radius=5, width=2)
        button_label: pg.Surface = self.font.render(self.text, True, self.BUTTON_SHADOW_COLOR)
        self.surface.blit(button_label, (self.pos[0] - button_label.get_width() // 2, self.pos[1] - button_label.get_height() // 2 - self.BUTTON_OFFSET))

    def check_button_collision(self) -> bool:
        """ Checks if the mouse is colliding with the button and if the left mouse button is clicked on it. """
        mouse_pos = pg.mouse.get_pos()
        if self.button_top_rect.collidepoint(mouse_pos):
            self.button_color = self.BUTTON_HOVER_COLOR
            if pg.mouse.get_pressed()[0]:
                self.offset = 0
                self.clicked = True
            else:
                self.offset = self.BUTTON_OFFSET
                if self.clicked == True:
                    self.clicked = False
        else:
            self.button_color = self.BUTTON_TOP_COLOR
            self.clicked = False
            self.offset = self.BUTTON_OFFSET
        return self.clicked
    