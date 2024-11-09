import settings as stgs

import pygame as pg
from random import randint
from typing import Final, TypeVar

Game = TypeVar("Game")


class Upgrade(pg.sprite.Sprite):
    TRANSPARENT_BACKGROUND: Final[tuple[int]] = (0, 0, 0, 0)
    SPEED: Final[int] = 50

    def __init__(self, game: Game, pos: tuple[int]) -> None:
        """
        Initialize the Upgrade sprite.
        Args:
        game: The game instance.
        pos: The position of the upgrade.
        """
        super().__init__(game.upgrade_group)
        background_number: int = randint(0, 6)
        self.upgrade_number: int = randint(0, 10)
        self.image: pg.Surface = pg.Surface((50, 50), pg.SRCALPHA)  # depends on the scale factor
        self.image.fill(self.TRANSPARENT_BACKGROUND)
        self.image.blit(game.assets["upgrade/background"][background_number], (0, 0))
        self.image.blit(game.assets["upgrade/image"][int(self.upgrade_number)], (0, 0))
        self.rect: pg.Rect = self.image.get_rect(center = pos)
        self.pos: pg.Vector2 = pg.Vector2(self.rect.topleft)
        self.mask: pg.mask = pg.mask.from_surface(self.image)

    def update(self, dt: float) -> None:
        """
        Update the upgrade position.
        Args:
        dt: The time elapsed since the last update.
        """
        self.pos.y += self.SPEED * dt
        self.rect.y = self.pos.y

        if self.rect.top > stgs.GAME_WINDOW_RESOLUTION[1]:
            self.kill()