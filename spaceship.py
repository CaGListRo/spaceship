import settings as stgs
from projectile import PlayerProjectile
from healthbar import Healthbar

import pygame as pg
from typing import Final, TypeVar

Game = TypeVar("Game")
Animation_object = TypeVar("Animation_object")
Healthbar_object = TypeVar("Healthbar_object")


class Spaceship(pg.sprite.Sprite):
    TRANSPARENT_BACKGROUND: Final[tuple[int]] = (0, 0, 0, 0)
    
    def __init__(self, game: Game, player_group: pg.sprite.Group, projectile_group: pg.sprite.Group, pos: tuple[int]) -> None:
        """
        Initialize the Spaceship object.
        Args:
        game (Game): The game object.
        player_group (pg.sprite.Group): The player group object.
        projectile_group (pg.sprite.Group): The projectile group object.
        pos (tuple[int]): The position of the spaceship.
        """
        super().__init__(player_group)
        self.game: Game = game
        self.player_projectile_group: pg.sprite.Group = projectile_group
        self.state: str = "idle"
        self.weapon: str = "laser"
        self.animation: Animation_object = self.game.assets["ship/" + self.state].copy()
        self.ship_image: pg.Surface = self.animation.get_img()
        self.weapon_image: pg.Surface = self.game.assets[self.weapon + "/" + self.state]
        self.image: pg.Surface = pg.Surface((self.ship_image.get_width(), self.ship_image.get_height()), pg.SRCALPHA)
        self.image.fill(self.TRANSPARENT_BACKGROUND)
        self.image.blit(self.weapon_image, (0, 0))
        self.image.blit(self.ship_image, (0, 0))
        self.rect: pg.Rect = self.image.get_rect(center = pos)
        self.mask: pg.mask = pg.mask.from_surface(self.image)
        self.pos: pg.Vector2 = pg.Vector2(self.rect.topleft)
        self.direction: pg.Vector2 = pg.Vector2()
        self.flip_image: bool = False
        self.rocket_flip_flop: bool = True

        self.shoot_timer: int = 0
        self.speed: int = 200
        self.max_health: int = 100
        self.health: int = 100   
        self.laser_fire_rate: float = 0.5
        self.rocket_fire_rate: float = 1.0
        self.laser_damage: int = 10
        self.rocket_damage: int = 50
        self.current_fire_rate: float = self.laser_fire_rate
        self.current_weapon_damage: int = self.laser_damage
        self.auto_fire: bool = True
        self.healthbar: None | Healthbar_object = None

        self.update_healthbar()

    def update_healthbar(self) -> None:
        """ Update the healthbar object. """
        if self.healthbar:
            self.game.healthbars.remove(self.healthbar)
        self.healthbar = Healthbar(self.game, self.max_health, self.health, self.image.get_width(), self.pos, self.image.get_height())

    def take_damage(self, damage: int | float) -> None:
        """
        Take damage from an enemy projectile.
        Args:
        damage (int | float): The damage taken.
        """
        self.health -= damage
        self.healthbar.update(self.health, self.pos)
        if self.health <= 0:
            self.kill()
            getattr(self.game, "handle_live_lost")()

    def return_current_fire_rate(self) -> float:
        """
        Return the current fire rate.
        Returns:
        float: The current fire rate.
        """
        return self.current_fire_rate
    
    def return_current_weapon_damage(self) -> int:
        """
        Return the current weapon damage.
        Returns:
        int: The current weapon damage.
        """
        return self.current_weapon_damage
    
    def create_mask(self) -> None:
        """ Creates the mask for the spaceship. """
        self.mask = pg.mask.from_surface(self.ship_image)

    def handle_animation(self, dt: float, move_x: tuple[int]) -> None:
        """
        Handle the animation of the spaceship.
        Args:
        dt (float): The time difference.
        move_x (tuple[int]): The movement of the spaceship.
        """
        old_state = self.state
        if (move_x[1] - move_x[0]) == 0:
            self.state = "idle"
        else:
            self.state = "curve"
        if old_state != self.state:
            self.animation = self.game.assets["ship/" + self.state].copy()
            self.rect = self.ship_image.get_rect(center = self.pos)
            self.create_mask()

        self.flip_image = True if (move_x[1] - move_x[0]) > 0 else False
        if self.auto_fire:
            self.fire_weapons(dt)
        self.animation.update(dt)

        self.ship_image = self.animation.get_img()
        self.weapon_image = self.game.assets[self.weapon + "/" + self.state]
        self.image.fill(self.TRANSPARENT_BACKGROUND)
        self.image.blit(self.weapon_image, (0, 0))
        self.image.blit(self.ship_image, (0, 0))
        self.image = pg.transform.flip(self.image, self.flip_image, False)

    def update(self, dt: float, move_x: tuple[int] = (0, 0), move_y: tuple[int] = (0, 0)) -> None:
        """
        Update the position of the spaceship and calls the handle_animation-method.
        Args:
        dt (float): The time difference.
        move_x (tuple[int]): The movement of the spaceship in the x-axis.
        move_y (tuple[int]): The movement of the spaceship in the y-axis.
        """
        self.handle_animation(dt, move_x)

        self.pos.x += (move_x[1] - move_x[0]) * self.speed * dt
        if self.game.drones[0] == 0:
            if self.pos.x < 0:
                self.pos.x = 0
        else:
            if self.pos.x - (self.ship_image.get_width() // 2) - (self.game.drones[0].image.get_width() // 2) < 0:
                self.pos.x = (self.ship_image.get_width() // 2) + (self.game.drones[0].image.get_width() // 2)

        if self.game.drones[1] == 0:        
            if self.pos.x + self.ship_image.get_width() > stgs.GAME_WINDOW_RESOLUTION[0]:
                self.pos.x = stgs.GAME_WINDOW_RESOLUTION[0] - self.ship_image.get_width()
        else:
            if self.pos.x + (self.ship_image.get_width() * 1.5) + (self.game.drones[1].image.get_width() // 2) > stgs.GAME_WINDOW_RESOLUTION[0]:
                self.pos.x = stgs.GAME_WINDOW_RESOLUTION[0] - (self.ship_image.get_width() * 1.5) - (self.game.drones[1].image.get_width() // 2)
        self.rect.x = self.pos.x

        self.pos.y += (move_y[1] - move_y[0]) * self.speed *dt
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y + self.ship_image.get_height() > stgs.GAME_WINDOW_RESOLUTION[1]:
            self.pos.y = stgs.GAME_WINDOW_RESOLUTION[1]  - self.ship_image.get_height()
        self.rect.y = self.pos.y

        self.healthbar.update(self.health, self.pos)

    def fire_weapons(self, dt: float) -> None:
        """
        Fires the weapons of the spaceship.
        Args:
        dt (float): The time difference.
        """
        self.shoot_timer += dt
        if self.weapon == "laser":
            self.current_fire_rate = self.laser_fire_rate
            self.current_weapon_damage = self.laser_damage
            if self.shoot_timer > max(0.1, self.laser_fire_rate):
                PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + 25, self.pos.y + 42))
                PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + 74, self.pos.y + 42))
                self.shoot_timer = 0
        elif self.weapon == "rocket_launcher":
            self.current_fire_rate = self.rocket_fire_rate
            self.current_weapon_damage = self.rocket_damage
            if self.shoot_timer > max(0.1, self.rocket_fire_rate):
                if self.rocket_flip_flop:
                    PlayerProjectile(self.game, "rocket1", self.current_weapon_damage, (self.pos.x + 25, self.pos.y + 42))
                    self.rocket_flip_flop = False
                else:
                    PlayerProjectile(self.game, "rocket1", self.current_weapon_damage, (self.pos.x + 74, self.pos.y + 42))
                    self.rocket_flip_flop = True
                self.shoot_timer = 0
        elif self.weapon == "sprayer":
            self.current_fire_rate = self.laser_fire_rate
            self.current_weapon_damage = self.laser_damage
            if self.shoot_timer > max(0.1, self.laser_fire_rate): 
                PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 20), 90)
                PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 20), 120)
                PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 20), 60)
                if self.game.sprayer_state == 5:
                    PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 20), 105)
                    PlayerProjectile(self.game, "laser", self.current_weapon_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 20), 75)
                self.shoot_timer = 0

    def draw(self, surf: pg.Surface) -> None:
        """
        Draws the spaceship on the given surface.
        Args:
        surf (pg.Surface): The surface to draw on.
        """
        surf.blit(self.image, self.pos)