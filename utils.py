import settings as stgs

import os
import pygame as pg
from random import randint
from typing import Final, TypeVar

Game = TypeVar("Game")
Animation_object = TypeVar("Animation_object")


BASE_PATH: Final[str] = "images/"
TRANSPARENT_BACKGROUND: Final[tuple[int]] = (0, 0, 0, 0)
WHITE: Final[tuple[int]] = (247, 247, 247)

def load_image(path: str, imagename: str, scale_factor: float) -> pg.Surface:
    """
    Load an image from a file and scale it by a factor.
    Args:
    path (str): The path to the image file.
    imagename (str): The name of the image file.
    scale_factor (float): The factor by which to scale the image.
    Returns:
    pg.Surface: The loaded and scaled image.
    """
    img: pg.Surface = pg.image.load(BASE_PATH + path + "/" + imagename).convert_alpha()
    return pg.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor))

def load_images(path: str, scale_factor: float) -> list[pg.Surface]:
    """
    Get's a path, calls for every item in the path the load_image function 
    and append the loaded image to a list, which it returns.
    Args:
    path (str): The path to the images.
    scale_factor (float): The factor by which to scale the images.
    Returns:
    list[pg.Surface]: A list of loaded and scaled images.
    """
    images = []
    for img_name in sorted(os.listdir(BASE_PATH + path)):  # sorted because of not Windows systems
        images.append(load_image(path + '/', img_name, scale_factor))
    return images

def create_highscores_screen(font: pg.font.Font) -> tuple[pg.Surface, list[str]]:
    """
    Creates a highscores screen with the current highscores.
    Args:
    font (pg.font.Font): The font to use for the highscores.
    Returns:
    tuple[pg.Surface, list[str]]: A tuple containing the highscores screen and
    the highscores as a list of strings.
    """
    surf: pg.Surface = pg.Surface((1600, 900), pg.SRCALPHA)
    surf.fill(TRANSPARENT_BACKGROUND)
    highscores_list = []
    with open("highscores_list.txt", "r", encoding="utf-8") as file:
        text = file.read()
        lines = text.splitlines()
        for i, line in enumerate(lines):
            word = line.split(" ")
            number_to_render = f"{str(i+1)}."
            number_to_blit = font.render(number_to_render, True, WHITE)
            surf.blit(number_to_blit, (450, 100 + i * 60))
            name_to_render = word[0]
            name_to_blit = font.render(name_to_render, True, WHITE)
            surf.blit(name_to_blit, (600, 100 + i * 60))
            score_to_render = word[1]
            score_to_blit = font.render(score_to_render, True, WHITE)
            surf.blit(score_to_blit, (950, 100 + i * 60))
            highscores_list.append([word[0], int(word[1])])
    return surf, highscores_list

def sort_and_write_highscores(highscores_list: list[str], name: str, score: int) -> None:
    """
    Sorts the highscores list, writes the new highscore to the list, pops the last item
    in the list to have 10 items in the list and writes the list to the highscores file.
    Args:
    highscores_list (list[str]): The list of highscores.
    name (str): The name of the player.
    score (int): The score of the player.
    """
    highscores_list.append([str(name), int(score)])

    while True:
        bubbled: bool = False
        for i in range(len(highscores_list)-1):  
            if highscores_list[i][1] < highscores_list[i+1][1]:
                highscores_list[i+1], highscores_list[i] = highscores_list[i], highscores_list[i+1]
                bubbled = True
                
        if not bubbled:
            break

    highscores_list.pop(-1)

    with open("highscores_list.txt", "w", encoding="utf-8") as file:
        for i in range(10):
            for j in range(2):
                
                file.write(str(highscores_list[i][j]))
                if j == 0:
                    file.write(" ")
                if j == 1:
                    file.write("\n")


class Animation:
    def __init__(self, image_list: list[pg.Surface], animation_duration: int | float, loop: bool = True) -> None:
        """
        Initializes an animation object.
        Args:
        image_list (list[pg.Surface]): The list of images to animate.
        animation_duration (int | float): The duration of the animation in seconds.
        loop (bool): Whether the animation should loop or not. Defaults to True.
        """
        self.img_list: list[pg.Surface] = list(image_list)
        self.anim_dur: int | float = animation_duration
        self.loop: bool = loop
        self.done: bool = False
        self.current_frame: int = 0
        self.img_duration: float = animation_duration / len(image_list)
        self.img_timer: int | float = 0

    def copy(self) -> Animation_object:
        """
        Creates a copy of the animation object and returns it.
        Returns:
        Animation_object: The copied animation object.
        """
        return Animation(self.img_list, self.anim_dur, self.loop)

    def update(self, dt: float) -> None:
        """
        Updates the animation.
        Args:
        dt (float): The time elapsed since the last frame.
        """
        self.img_timer += dt
        if self.img_timer >= self.img_duration and not self.done:
            self.current_frame += 1
            self.img_timer = 0
            if self.current_frame >= len(self.img_list):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.done = True

    def get_img(self) -> pg.Surface | None:
        """
        Gets the current image of the animation.
        Returns:
        pg.Surface | None: The current image of the animation, or None if the animation is done
        """
        if 0 <= self.current_frame < len(self.img_list):
            return self.img_list[self.current_frame]
        else:
            return None
        

class Helpsite:
    TRANSPARENT_BACKGROUND: Final[tuple[int]] = (0, 0, 0, 0)

    def __init__(self, game: Game) -> None:
        """
        Initializes the help site.
        Args:
        game (Game): The game object.
        """
        self.game: Game = game
        self.font = pg.font.SysFont("comicsans", 32)
        self.surface = pg.Surface((1600, 900), pg.SRCALPHA)
        self.surface.fill(self.TRANSPARENT_BACKGROUND)
        self.text_surf = pg.Surface((530, 150), pg.SRCALPHA)
        self.text_surf.fill(self.TRANSPARENT_BACKGROUND)
        self.mouse_pos = pg.mouse.get_pos()
        self.upgrade_rect_list: list[pg.Rect] = []
        self.rect_width_height: int = self.game.assets["upgrade/background"][0].get_width()
        self.text_list: list[str] = []
        self.text_number: int = -1
        self.generate_background_numbers()
        self.load_upgrade_texts()
        self.draw_help_text()
        self.draw_upgrades()

    def generate_background_numbers(self) -> None:
        """ Generate a list of 11 numbers from 0 to 6 for the upgrade background colors. """
        self.background_numbers = [randint(0, 6) for _ in range(11)]

    def draw_help_text(self) -> None:
        """ Opens the help_text.txt and draws its content on the help site surface. """
        with open("help_text.txt", "r", encoding="utf-8") as file:
            text = file.read()
            lines = text.splitlines()
            for i, line in enumerate(lines):
                text = self.font.render(line, True, (247, 247, 247))
                self.surface.blit(text, (50, 50 + i * 50))

    def draw_upgrades(self) -> None:
        """
        Draws the upgrade background and the upgrade image on the help site surface.
        And places an collision rectangle over each upgrade for the help text display.
        """
        self.upgrade_rect_list = []
        for i, upgrade in enumerate(self.game.assets["upgrade/image"]):
            self.surface.blit(self.game.assets["upgrade/background"][self.background_numbers[i]], (50 + i * 130, 420))
            self.surface.blit(upgrade, (50 + i * 130, 420))
            self.upgrade_rect_list.append(pg.Rect(50 + i * 130, 420, self.rect_width_height, self.rect_width_height))

    def check_rect_collision(self) -> int:
        """
        Checks if the mouse is over any of the upgrade rectangles.
        Returns the index of the rectangle if the mouse is over it, otherwise returns -1.
        Returns:
        int: The index of the rectangle if the mouse is over it, otherwise -1.
        """
        self.mouse_pos = pg.mouse.get_pos()
        for i, rect in enumerate(self.upgrade_rect_list):
            if rect.collidepoint(self.mouse_pos):
                return i
        return -1
    
    def handle_upgrade_texts(self) -> None:
        """
        Gets the upgrade text number from the check_rect_collision-method,
        loads it from self.text_list, renders it and blits the result to self.text_surf. 
        """
        self.text_number = self.check_rect_collision()
        self.text_surf.fill(self.TRANSPARENT_BACKGROUND)
        for i, line in enumerate(self.text_list[self.text_number]):
            line_to_blit = self.font.render(line, True, (247, 247, 247))
            self.text_surf.blit(line_to_blit, (0, 0 + i * 50))

    def load_upgrade_texts(self) -> None:
        """
        Loads the upgrade text from the upgrade_texts.txt file, stplits it in lines 
        and stores it in the two dimensional self.text_list. """
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

    def update(self) -> None:
        """ Updates the help site. """
        self.surface.fill(self.TRANSPARENT_BACKGROUND)
        self.handle_upgrade_texts()
        self.draw_help_text()
        self.draw_upgrades()

    def render(self, surf: pg.Surface) -> None:
        """
        Renders the help site to the given surface.
        Args:
        surf: The surface to render the help site to.
        """ 
        if self.text_number != -1:
            if self.mouse_pos[0] + self.text_surf.get_width() > stgs.MAIN_WINDOW_RESOLUTION[0]:
                
                self.mouse_pos = (stgs.MAIN_WINDOW_RESOLUTION[0] - self.text_surf.get_width(), self.mouse_pos[1])
            self.surface.blit(self.text_surf, self.mouse_pos)
        surf.blit(self.surface, (0, 0))
        