from projectile import PlayerProjectile
from healthbar import Healthbar

import pygame as pg
from typing import Final, TypeVar

Game = TypeVar("Game")
Animation = TypeVar("Animation")


class Drone(pg.sprite.Sprite):
    MAX_HEALTH: Final[int] = 50

    def __init__(self, game: Game, drone_group: pg.sprite.Group, projectile_group: pg.sprite.Group, side: int) -> None:
        """
        Initializes a drone object.
        Args:
        game (Game): The game object.
        drone_group (pg.sprite.Group): The group of drones.
        projectile_group (pg.sprite.Group): The group of projectiles.
        side (int): The side of the drone (1 = right or -1 = left).
        """
        super().__init__(drone_group)
        self.game: Game = game
        self.player_projectile_group: pg.sprite.Group = projectile_group
        self.state: str = "idle"
        self.side: int = side
        self.animation: Animation = self.game.assets["drone/" + self.state].copy()
        self.image: pg.Surface = self.animation.get_img()
        self.x_pos: int = self.game.spaceship.image.get_width() // 2 if self.side < 0 else round(self.game.spaceship.image.get_width() * 1.5) - self.image.get_width()
        self.pos: pg.Vector2 = pg.Vector2(self.game.spaceship.pos.x + (self.x_pos * self.side), self.game.spaceship.pos.y + (self.game.spaceship.image.get_height() // 2))
        self.rect: pg.Rect = self.image.get_rect(center = self.pos)
        self.drone_mask: pg.mask = pg.mask.from_surface(self.image)
        
        self.direction: pg.Vector2 = pg.Vector2()
        self.flip_image: bool = False
        self.shoot_timer: int | float = 0
        self.laser_fire_rate: float = 0.5
        self.laser_damage: int = 5
        self.auto_fire: bool = True
        self.health: int | float = 50    
        self.healthbar = Healthbar(self.game, self.MAX_HEALTH, self.health, self.image.get_width(), self.pos, self.image.get_height())

    def take_damage(self, damage: int | float) -> None:
        """
        Takes damage from the drone.
        Args:
        damage (int | float): The amount of damage taken.
        """

        self.health -= damage
        self.healthbar.update(self.health, self.pos)
        if self.health <= 0:
            self.game.healthbars.remove(self.healthbar)
            if self.side < 0 or self.game.drones[0] == 0:              
                self.kill()
                self.game.drones[0] = 0
                      
            elif self.side > 0 or self.game.drones[1] == 0:
                self.kill()
                self.game.drones[1] = 0
                
    def create_mask(self) -> None:
        """ Creates the mask for the drone. """
        self.drone_mask = pg.mask.from_surface(self.image)

    def handle_animation(self, dt: float, move_x: list[int]) -> None:
        """
        Handles the animation of the drone.
        Args:
        dt (float): The time since the last frame.
        move_x (list[int]): The x movement of the drone.
        """

        old_state = self.state
        if (move_x[1] - move_x[0]) == 0:
            self.state = "idle"
        else:
            self.state = "curve"
        if old_state != self.state:
            self.animation = self.game.assets["drone/" + self.state].copy()
            self.rect = self.image.get_rect(center = self.pos)
            self.create_mask()

        self.flip_image = True if (move_x[1] - move_x[0]) > 0 else False
        if self.auto_fire:
            self.fire_weapon(dt)
        self.animation.update(dt)

        self.image = pg.transform.flip(self.animation.get_img(), self.flip_image, False)

    def update(self, dt: float, move_x: list[int] = [0, 0]) -> None:
        """
        Updates the drone.
        Args:
        dt (float): The time difference between the current frame and the previous frame.
        move_x (list[int]): The x movement of the drone.
        """

        self.handle_animation(dt, move_x)
        self.x_pos = self.game.spaceship.image.get_width() // 2 if self.side < 0 else round(self.game.spaceship.image.get_width() * 1.5) - self.image.get_width()
        self.pos = pg.Vector2(self.game.spaceship.pos.x + (self.x_pos * self.side), self.game.spaceship.pos.y + (self.game.spaceship.image.get_height() // 2))
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        self.healthbar.update(self.health, self.pos)

    def fire_weapon(self, dt: float) -> None:
        """
        Fires the drone's weapon.
        Args:
        dt (float): The time difference between the current frame and the previous frame.
        """
        self.shoot_timer += dt
        if self.shoot_timer > max(0.1, self.laser_fire_rate):
            PlayerProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 5))
            self.shoot_timer = 0