import settings as stgs

import pygame as pg
import math

from typing import TypeVar

Game = TypeVar("Game")


class Projectile(pg.sprite.Sprite):
    def __init__(self, game: Game, projectile_type: str, damage: int, group: pg.sprite.Group, pos: tuple[int], direction: int, laser_color: str = None, angle: int = 90) -> None:
        """
        A projectile class that can be used to create different types of projectiles.
        Args:
        game (Game): The game object.
        projectile_type (str): The type of projectile. Can be 'laser' or 'rocket'.
        damage (int): The damage of the projectile.
        group (pg.sprite.Group): The group that the projectile belongs to.
        pos (tuple[int]): The position of the projectile.
        direction (int): The direction of the projectile.
        laser_color (str): The color of the laser. Defaults to None.
        angle (int): The angle of the projectile. Defaults to 90.
        """
        super().__init__(group)
        self.game: Game = game
        self.damage: int = damage
        color: int = self.color_picker(color=laser_color)
        self.angle: int = angle
        if self.angle != 90:
            self.image_rotate_angle: int = self.angle - 90
        self.animate: bool = self.get_image(type=projectile_type, color=color)
        self.rect: pg.Rect = self.image.get_rect(center=pos)
        self.pos: pg.Vector2 = pg.Vector2(self.rect.topleft)
        self.direction: int = direction
        
    def get_image(self, type: str, color: str = None) -> bool:
        """
        Get the image of the projectile.
        Args:
        type (str): The type of projectile.
        color (str): The color of the projectile. Defaults to None.
        Returns:
        bool: Whether the image is animated or not.
        """
        if type == "laser":
            self.image: pg.Surface = self.game.assets[type][color]
            if self.game.spaceship.weapon == "sprayer" and self.angle != 90:
                self.image = pg.transform.rotate(self.image, -self.image_rotate_angle)
            return False
        elif type == "rocket1":
            self.animation = self.game.assets[type].copy()
            self.image: pg.Surface = self.animation.get_img()
            self.image = pg.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
            return True

    def color_picker(self, color: str) -> int:
        """
        Pick a color for the projectile.
        Args:
        color (str): The color of the projectile.
        Returns:
        int: The color code.
        """
        if color == "blue":
            return 0
        elif color == "green":
            return 1
        elif color == "orange":
            return 2
        elif color == "red":
            return 3
        else:
            return 4    

    def update(self, dt: float) -> None:
        """
        Update the projectile.
        Args:
        dt (float): The time difference.
        """
        if self.angle == 90:
            if self.animate:
                self.animation.update(dt)
                self.image = self.animation.get_img()
            self.pos.y += self.direction * self.speed * dt
        else:
            x_move = self.speed * dt * math.cos(math.radians(self.angle))
            y_move = self.speed * dt * math.sin(math.radians(self.angle))   
            self.pos.x -= x_move
            self.pos.y -= y_move

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y < -10 or self.pos.y > stgs.GAME_WINDOW_RESOLUTION[1] + 10:
            self.kill()
        
        if self.pos.x < -10 or self.pos.x > stgs.GAME_WINDOW_RESOLUTION[0] + 10:
            self.kill()


class PlayerProjectile(Projectile):
    def __init__(self, game: Game, projectile_type: str, damage: int, pos: tuple[int], angle: int = 90) -> None:
        """
        Initializes a PlayerProjectile object with inheritance from the Projectile class.
        Args:
        game (Game): The game object.
        projectile_type (str): The type of projectile.
        damage (int): The damage of the projectile.
        pos (tuple[int]): The position of the projectile.
        angle (int): The angle of the projectile. Defaults to 90.
        """
        super().__init__(game=game, projectile_type=projectile_type, damage=damage, group=game.player_projectile_group, pos=pos, direction=-1, laser_color="blue", angle=angle)
        self.speed: int = 250
        
    def get_image(self, type: str, color: str) -> None:
        """
        Returns the image of the projectile.
        Args:
        type (str): The type of projectile.
        color (str): The color of the projectile.
        """
        super().get_image(type, color)

        if type == "rocket1":
            self.image = pg.transform.rotate(self.image, 180)


class EnemyProjectile(Projectile):
    def __init__(self, game: Game, projectile_type: str, damage: int, pos: tuple[int], laser_color: str, angle: int = 90) -> None:
        """
        Initializes a EnemyProjectile object with inheritance from the Projectile class.
        Args:
        game (Game): The game object.
        projectile_type (str): The type of projectile.
        damage (int): The damage of the projectile.
        pos (tuple[int]): The position of the projectile.
        angle (int): The angle of the projectile. Defaults to 90.
        """
        super().__init__(game, projectile_type=projectile_type, damage=damage, group=game.enemy_projectile_group, pos=pos, direction=1, laser_color=laser_color, angle=angle)
        self.speed: int = 150