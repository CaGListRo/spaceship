import settings as stgs
from spaceship import Spaceship
from utils import enemy_creator

from time import time
import pygame as pg
from random import randint


class Game:
    def __init__(self) -> None:
        pg.init()
        self.main_window = pg.display.set_mode(stgs.MAIN_WINDOW_RESOLUTION)
        self.game_window = pg.Surface(stgs.GAME_WINDOW_RESOLUTION)

        self.player_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.projectile_group = pg.sprite.Group()

        # Create player and add to groups
        self.player_pos = (stgs.GAME_WINDOW_RESOLUTION[0] // 2, stgs.GAME_WINDOW_RESOLUTION[1] // 5 * 4)
        self.spaceship = Spaceship(self.player_group, self.projectile_group, self.player_pos)
        self.move_x, self.move_y = [0, 0], [0, 0]

        self.run = True

    def handle_projectile_player_collision(self):
        for projectile in self.projectile_group:
            overlap_sprites = pg.sprite.spritecollide(projectile, self.player_group, True)
            if overlap_sprites:
                projectile.kill()

    def handle_projectile_enemy_collision(self):
        for projectile in self.projectile_group:
            overlap_sprites = pg.sprite.spritecollide(projectile, self.enemy_group, True)
            if overlap_sprites:
                projectile.kill()

    def handle_enemies(self):
        if len(self.enemy_group) < 3:
            enemy_creator(self.enemy_group, self.projectile_group)

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
        self.projectile_group.update(dt)
        self.enemy_group.update(dt)

    def draw_window(self):
        self.main_window.fill('black')
        self.game_window.fill('blue')

        self.enemy_group.draw(self.game_window)
        self.projectile_group.draw(self.game_window)
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

            self.draw_window()


if __name__ == "__main__":
    Game().main()