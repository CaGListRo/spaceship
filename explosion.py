import pygame as pg
from typing import TypeVar

Game = TypeVar("Game")
Animation = TypeVar("Animation")

class ShipExplosion:
    def __init__(self, game: Game, pos: tuple[int], rotate: int = 180) -> None:
        """
        Initialize the ShipExplosion object.
        Args:
        game (Game): The game object.
        pos (tuple[int]): The position of the explosion.
        rotate (int): The rotation of the explosion. Defaults to 180.
        """
        self.rotate: int = rotate
        self.animation: Animation = game.assets["explosion"].copy()
        self.image: pg.Surface = pg.transform.rotate(self.animation.get_img(), self.rotate)
        self.rect: pg.Rect = self.image.get_rect(center = pos)
        self.pos: pg.Vector2 = pg.Vector2(self.rect.topleft)
        self.speed: int = 50
        self.remove_explosion: bool = False
        
    def update(self, dt: float) -> bool:
        """
        Update the explosion animation.
        Args:
        dt (float): The time difference since the last update.
        Returns:
        bool: Whether the explosion should be removed.
        """
        if self.animation.done:
            self.remove_explosion = True

        self.pos.y += self.speed * dt
        self.rect.y = self.pos.y

        self.animation.update(dt)
        self.image = self.animation.get_img()
        if self.image != None:
            self.image = pg.transform.rotate(self.image, self.rotate)

        return self.remove_explosion
    
    def draw(self, surf: pg.Surface) -> None:
        """
        Draw the explosion animation on the given surface.
        Args:
        surf (pg.Surface): The surface to draw on.
        """
        if self.image != None:
            surf.blit(self.image, self.rect)
    

class SmallExplosion:
    def __init__(self, game: Game, pos: tuple[int]) -> None:
        """
        Initialize the SmallExplosion object.
        Args:
        game (Game): The game object.
        pos (tuple[int]): The position of the explosion.
        """
        self.animation: Animation = game.assets["projectile_hit"].copy()
        self.image: pg.Surface = self.animation.get_img()
        self.rect: pg.Rect = self.image.get_rect(center = pos)
        self.pos: pg.Vector2 = pg.Vector2(self.rect.topleft)
        self.remove_hit: bool = False
        
    def update(self, dt: float) -> None:
        """
        Update the explosion animation.
        Args:
        dt (float): The time difference since the last update.
        Returns:
        bool: Whether the explosion should be removed.
        """
        if self.animation.done:
            self.remove_hit = True

        self.animation.update(dt)
        self.image = self.animation.get_img()

        return self.remove_hit
    
    def draw(self, surf: pg.Surface) -> None:
        """
        Draw the explosion animation on the given surface.
        Args:
        surf (pg.Surface): The surface to draw on.
        """
        if self.image != None:
            surf.blit(self.image, self.rect)


class BiggerExplosion:
    def __init__(self, game: Game, pos: tuple[int]) -> None:
        """
        Initialize the BiggerExplosion object.
        Args:
        game (Game): The game object.
        pos (tuple[int]): The position of the explosion.
        """
        self.animation: Animation = game.assets["bigger_explosion"].copy()
        self.image: pg.Surface = self.animation.get_img()
        self.rect: pg.Rect = self.image.get_rect(center = pos)
        self.pos: pg.Vector2 = pg.Vector2(self.rect.topleft)
        self.remove_hit: bool = False
        
    def update(self, dt: float) -> bool:
        """
        Update the explosion animation.
        Args:
        dt (float): The time difference since the last update.
        Returns:
        bool: Whether the explosion should be removed.
        """
        if self.animation.done:
            self.remove_hit = True

        self.animation.update(dt)
        self.image = self.animation.get_img()

        return self.remove_hit
    
    def draw(self, surf: pg.Surface) -> None:
        """
        Draw the explosion animation on the given surface.
        Args:
        surf (pg.Surface): The surface to draw on.
        """
        if self.image != None:
            surf.blit(self.image, self.rect)