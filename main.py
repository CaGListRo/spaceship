import settings as stgs
from spaceship import Spaceship
from enemy_creator import enemy_creator
from utils import load_image, load_images, Animation

from time import time
import pygame as pg
from random import randint


class Game:
    def __init__(self) -> None:
        pg.init()
        self.main_window = pg.display.set_mode(stgs.MAIN_WINDOW_RESOLUTION)
        self.game_window = pg.Surface(stgs.GAME_WINDOW_RESOLUTION)

        self.player_group = pg.sprite.Group()
        self.player_projectile_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.enemy_projectile_group = pg.sprite.Group()
        self.upgrade_group = pg.sprite.Group()

        self.assets = {
            "background": load_image("backgrounds", "00.png", 1),
            "ship/idle": Animation(load_images("Ship/idle", scale_factor=0.25), animation_duration=0.5),
            "ship/curve": Animation(load_images("Ship/curve", scale_factor=0.25), animation_duration=0.5),
            "enemy1/idle": Animation(load_images("enemies/ship1/idle", scale_factor=0.25), animation_duration=0.5),
            "enemy1/curve": Animation(load_images("enemies/ship1/curve", scale_factor=0.25), animation_duration=0.5),
            "enemy2/idle": Animation(load_images("enemies/ship2/idle", scale_factor=0.25), animation_duration=0.5),
            "enemy2/curve": Animation(load_images("enemies/ship2/curve", scale_factor=0.25), animation_duration=0.5),
            "enemy3/idle": Animation(load_images("enemies/ship3/idle", scale_factor=0.25), animation_duration=0.5),
            "laser": load_images("ammo/lasers", scale_factor=0.5),
            "rocket1": Animation(load_images("ammo/rockets/rocket1", scale_factor=0.25), animation_duration=2),
            "upgrade/background": load_images("upgrades/backgrounds", scale_factor=0.5),
            "upgrade/image": load_images("upgrades/images", scale_factor=0.5),
        }
        
        # Create player and add to groups
        self.player_pos = (stgs.GAME_WINDOW_RESOLUTION[0] // 2, stgs.GAME_WINDOW_RESOLUTION[1] // 5 * 4)
        self.spaceship = Spaceship(self, self.player_group, self.player_projectile_group, self.player_pos)
        self.move_x, self.move_y = [0, 0], [0, 0]

        self.score_font = pg.font.SysFont("comicsans", 42)

        self.background_start_y = -2000
        self.background_y = self.background_start_y

        self.run = True
        self.score = 0
        self.phase = 1
        self.wave = 0

    def handle_projectile_player_collision(self):
        for projectile in self.enemy_projectile_group:
            overlap_sprites = pg.sprite.spritecollide(projectile, self.player_group, False, pg.sprite.collide_mask)
            if overlap_sprites:
                for sprite in overlap_sprites:
                    sprite.take_damage(projectile.damage)
                    projectile.kill()

    def handle_projectile_enemy_collision(self):
        for projectile in self.player_projectile_group:
            overlap_sprites = pg.sprite.spritecollide(projectile, self.enemy_group, False, pg.sprite.collide_mask)
            if overlap_sprites:
                for sprite in overlap_sprites:
                    sprite.take_damage(projectile.damage)
                    projectile.kill()
                    self.score += 10

    def handle_enemies(self):
        if self.wave != 20:
            if len(self.enemy_group) < 2:
                enemy_creator(self, self.enemy_group, self.enemy_projectile_group, self.upgrade_group, self.phase, self.wave)
                self.wave += 1

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.move_y[0] = 1
                if event.key == pg.K_DOWN:
                    self.move_y[1] = 1
                if event.key == pg.K_LEFT:
                    self.move_x[0] = 1
                if event.key == pg.K_RIGHT:
                    self.move_x[1] = 1

            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.move_y[0] = 0
                if event.key == pg.K_DOWN:
                    self.move_y[1] = 0
                if event.key == pg.K_LEFT:
                    self.move_x[0] = 0
                if event.key == pg.K_RIGHT:
                    self.move_x[1] = 0

    def update_groups(self, dt):
        self.player_group.update(dt, self.move_x, self.move_y)
        self.player_projectile_group.update(dt)
        self.enemy_group.update(dt)
        self.enemy_projectile_group.update(dt)
        self.upgrade_group.update(dt)

    def draw_score(self):
        score_to_blit = self.score_font.render(str(self.score), True, (247, 247, 247))
        self.main_window.blit(score_to_blit, (8, 8))
        health_to_blit = self.score_font.render(str(self.spaceship.health), True, (247, 0, 0))
        self.main_window.blit(health_to_blit, (8, 200))

    def move_background(self, dt):
        self.background_y += dt * 10
        self.background_y = min(0, self.background_y)


    def draw_window(self):
        self.main_window.fill('blue')
        self.game_window.blit(self.assets["background"], (0, self.background_y))

        self.draw_score()
        self.upgrade_group.draw(self.game_window)
        self.enemy_group.draw(self.game_window)
        self.enemy_projectile_group.draw(self.game_window)
        self.player_projectile_group.draw(self.game_window)
        self.player_group.draw(self.game_window)

        pg.draw.rect(self.main_window, (247, 247, 247), (190, 90, 1410, 810))
        self.main_window.blit(self.game_window, (195, 95))
        pg.display.update()

    def main(self):
        last_time = time()
        while self.run:
            dt = time() - last_time
            last_time = time()

            self.handle_events()
            self.handle_enemies()

            self.update_groups(dt)
            self.handle_projectile_enemy_collision()
            self.handle_projectile_player_collision()

            self.move_background(dt)

            self.draw_window()


if __name__ == "__main__":
    Game().main()