import pygame as pg

from typing import Final, TypeVar

Game = TypeVar("Game")


class Healthbar:
    DARK_ORANGE: Final[tuple[int]] = (238, 106, 80)
    RED: Final[tuple[int]] = (247, 0, 0)
    GREEN: Final[tuple[int]] = (0, 247, 0)
    HEALTHBAR_HEIGHT: Final[int] = 6
    
    def __init__(self, game: Game, max_health: int, current_health: int, image_width: int, sprite_pos: tuple[int], image_height: int = 0) -> None:
        self.game: Game = game
        self.max_health: int = max_health
        self.current_health: int = current_health
        self.img_width: int = image_width
        self.img_height: int = image_height
        self.healthbar_width: int = int(self.img_width * 0.9)
        self.healthbar_height_offset: int = self.HEALTHBAR_HEIGHT if self.img_height == 0 else -20
        self.side_picker: int = -1 if self.img_height == 0 else 1
        self.center_pos: list[int] = [0, 0]
        self.center_pos[0] = sprite_pos[0] + (self.img_width // 2)
        self.center_pos[1] = sprite_pos[1] + (self.side_picker * self.img_height) + 10 + self.healthbar_height_offset
        self.health_percent: float = self.current_health * 100 / self.max_health
        self.healthbar_length: int = round(self.health_percent * (self.healthbar_width - 2) / 100)
        self.game.healthbars.append(self)

    def update(self, current_health: int | float, sprite_pos: tuple[int]) -> None:
        self.current_health = current_health
        self.center_pos[0] = sprite_pos[0] + (self.img_width // 2)
        self.center_pos[1] = sprite_pos[1] + (self.side_picker * self.img_height) + 10 + self.healthbar_height_offset
        self.health_percent = self.current_health * 100 / self.max_health
        self.healthbar_length = round(self.health_percent * (self.healthbar_width - 2) / 100)

    def draw(self, surf: pg.Surface) -> None:
        pg.draw.rect(surf, self.DARK_ORANGE, (self.center_pos[0] - self.healthbar_width // 2, self.center_pos[1] - self.HEALTHBAR_HEIGHT // 2, self.healthbar_width, self.HEALTHBAR_HEIGHT))
        pg.draw.rect(surf, self.RED, (self.center_pos[0] - self.healthbar_width // 2 + 1, self.center_pos[1] - self.HEALTHBAR_HEIGHT // 2 + 1, self.healthbar_width - 2, self.HEALTHBAR_HEIGHT - 2))
        pg.draw.rect(surf, self.GREEN, (self.center_pos[0] - self.healthbar_width // 2 + 1, self.center_pos[1] - self.HEALTHBAR_HEIGHT // 2 + 1, self.healthbar_length, self.HEALTHBAR_HEIGHT - 2))