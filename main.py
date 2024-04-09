import settings as stgs
from spaceship import Spaceship
from upgrades import Upgrade
from explosion import ShipExplosion, SmallExplosion
from drone import Drone
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
        self.fx_list = []
        self.healthbars = []

        self.assets = {
            "background": load_image("backgrounds", "00.png", 1),
            "title": load_image("", "title.png", 1),
            "ship/idle": Animation(load_images("ship/idle", scale_factor=0.25), animation_duration=0.5, loop=True),
            "ship/curve": Animation(load_images("ship/curve", scale_factor=0.25), animation_duration=0.5, loop=True),
            "laser/idle": load_image("ship/weapons", "laser idle.png", 0.25),
            "laser/curve": load_image("ship/weapons", "laser curve.png", 0.25),
            "rocket_launcher/idle": load_image("ship/weapons", "rocketlauncher idle.png", 0.25),
            "rocket_launcher/curve": load_image("ship/weapons", "rocketlauncher curve.png", 0.25),
            "sprayer/idle": load_image("ship/weapons", "sprayer idle.png", 0.25),
            "sprayer/curve": load_image("ship/weapons", "sprayer curve.png", 0.25),
            "drone/idle": Animation(load_images("drone/idle", scale_factor=0.3), animation_duration=0.5, loop=True),
            "drone/curve": Animation(load_images("drone/curve", scale_factor=0.3), animation_duration=0.5, loop=True),
            "enemy1/idle": Animation(load_images("enemies/ship1/idle", scale_factor=0.25), animation_duration=0.5, loop=True),
            "enemy2/idle": Animation(load_images("enemies/ship2/idle", scale_factor=0.25), animation_duration=0.5, loop=True),
            "enemy3/idle": Animation(load_images("enemies/ship3/idle", scale_factor=0.25), animation_duration=0.5, loop=True),
            "boss1/idle": Animation(load_images("enemies/boss1/idle", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss1/left": Animation(load_images("enemies/boss1/left(right)", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss1/right": Animation(load_images("enemies/boss1/right(left)", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss2/idle": Animation(load_images("enemies/boss2/idle", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss2/left": Animation(load_images("enemies/boss2/left(right)", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss2/right": Animation(load_images("enemies/boss2/right(left)", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss2/flight": Animation(load_images("enemies/boss2/flight", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss2/open": Animation(load_images("enemies/boss2/open", scale_factor=0.75), animation_duration=2, loop=False),
            "boss3/idle": Animation(load_images("enemies/boss3/idle", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss3/left": Animation(load_images("enemies/boss3/left(right)", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss3/right": Animation(load_images("enemies/boss3/right(left)", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss3/flight": Animation(load_images("enemies/boss3/flight", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss3/open": Animation(load_images("enemies/boss3/open", scale_factor=0.75), animation_duration=2, loop=False),
            "laser": load_images("ammo/lasers", scale_factor=0.5),
            "rocket1": Animation(load_images("ammo/rockets/rocket1", scale_factor=0.25), animation_duration=2, loop=True),
            "upgrade/background": load_images("upgrades/backgrounds", scale_factor=0.5),
            "upgrade/image": load_images("upgrades/images", scale_factor=0.5),
            "explosion": Animation(load_images("fx/ship explosion", scale_factor=0.5), animation_duration=1, loop=False),
            "projectile_hit": Animation(load_images("fx/small explosion", scale_factor=0.5), animation_duration=0.5, loop=False),
        }
        
        self.player_pos = (stgs.GAME_WINDOW_RESOLUTION[0] // 2, stgs.GAME_WINDOW_RESOLUTION[1] // 5 * 4)
        self.spaceship = Spaceship(self, self.player_group, self.player_projectile_group, self.player_pos)
        self.move_x, self.move_y = [0, 0], [0, 0]

        self.score_font = pg.font.SysFont("comicsans", 42)

        self.background_start_y = -2000
        self.background_y = self.background_start_y

        self.lives = 3
        self.drones = [0, 0]
        self.drones_to_get = 0
        self.drones_max = 2
        self.run = True
        self.score = 0
        self.phase = 3
        self.wave = 19
        self.sprayer_state = 0

    def add_drones(self):
        for i, _ in enumerate(self.drones):
            if self.drones[i] == 0 and self.drones_to_get > 0:
                # self.drones[i] = 1
                self.drones_to_get -= 1
                side_picker = -1 if i == 0 else 1
                self.drones[i] = Drone(self, self.player_group, self.player_projectile_group, side_picker)

    def handle_upgrade_collision(self):
        for upgrade in self.upgrade_group:
            if pg.sprite.spritecollide(upgrade, self.player_group, False, pg.sprite.collide_mask):
                if upgrade.upgrade_number == 0:
                    self.drones_to_get = min(self.drones_to_get + 1, self.drones_max)  # drone/s
                    if self.drones[0] == 0 or self.drones[1] == 0:
                        self.add_drones()
                elif upgrade.upgrade_number == 1:
                    self.lives += 1
                elif upgrade.upgrade_number == 2:
                    self.spaceship.laser_damage -= 1
                    self.spaceship.rocket_damage -= 5
                elif upgrade.upgrade_number == 3:
                    self.spaceship.laser_damage += 1
                    self.spaceship.rocket_damage += 5
                elif upgrade.upgrade_number == 4:
                    self.spaceship.laser_fire_rate += 0.05
                    self.spaceship.rocket_fire_rate += 0.1
                elif upgrade.upgrade_number == 5:
                    self.spaceship.laser_fire_rate -= 0.05
                    self.spaceship.rocket_fire_rate -= 0.1
                elif upgrade.upgrade_number == 6:
                    self.spaceship.health = 100
                elif upgrade.upgrade_number == 7:
                    self.spaceship.health = min(self.spaceship.health + 25, 100)
                elif upgrade.upgrade_number == 8:
                    self.spaceship.weapon = "laser"  # parallel fire
                    self.spaceship.current_weapon_damage = self.spaceship.laser_damage
                    self.sprayer_state = 0
                elif upgrade.upgrade_number == 9:
                    self.spaceship.weapon = "rocket_launcher"  # rockets
                    self.spaceship.current_weapon_damage = self.spaceship.rocket_damage
                    self.sprayer_state = 0
                elif upgrade.upgrade_number == 10:
                    self.spaceship.weapon = "sprayer"  # spray
                    self.spaceship.current_weapon_damage = self.spaceship.laser_damage
                    self.sprayer_state = 3 if self.sprayer_state == 0 else 5

                upgrade.kill()

    def handle_projectile_player_collision(self):
        for projectile in self.enemy_projectile_group:
            overlap_sprites = pg.sprite.spritecollide(projectile, self.player_group, False, pg.sprite.collide_mask)
            if overlap_sprites:
                for sprite in overlap_sprites:
                    self.fx_list.append(SmallExplosion(self, (projectile.pos.x, projectile.pos.y)))
                    sprite.take_damage(projectile.damage)
                    projectile.kill()

    def handle_projectile_enemy_collision(self):
        for projectile in self.player_projectile_group:
            overlap_sprites = pg.sprite.spritecollide(projectile, self.enemy_group, False, pg.sprite.collide_mask)
            if overlap_sprites:
                for sprite in overlap_sprites:
                    killed = sprite.take_damage(projectile.damage)
                    self.fx_list.append(SmallExplosion(self, (projectile.pos.x, projectile.pos.y)))
                    if killed:
                        Upgrade(self, (sprite.pos.x + sprite.image.get_width() // 2, sprite.pos.y + sprite.image.get_height() // 2))
                        self.fx_list.append(ShipExplosion(self, (sprite.pos.x + sprite.image.get_width() // 2, sprite.pos.y + sprite.image.get_height() + 20)))
                    projectile.kill()
                    self.score += 10

    def handle_enemies(self):
        if self.wave != 20:
            if len(self.enemy_group) < 1:
                enemy_creator(self, self.enemy_group, self.phase, self.wave)
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
        self.enemy_projectile_group.update(dt)
        self.enemy_group.update(dt)
        self.upgrade_group.update(dt)

        for projectile_hit in self.fx_list:
            remove_hit = projectile_hit.update(dt)
            if remove_hit:
                self.fx_list.remove(projectile_hit)

        for healthbar in self.healthbars:
            if healthbar.current_health <= 0:
                self.healthbars.remove(healthbar)

    def draw_score(self):
        score_to_blit = self.score_font.render(str(self.score), True, (247, 247, 247))
        self.main_window.blit(score_to_blit, (8, 8))

    def move_background(self, dt):
        self.background_y += dt * 10
        self.background_y = min(0, self.background_y)

    def draw_window(self):
        self.main_window.blit(self.assets["title"], (0, 0))
        self.game_window.blit(self.assets["background"], (0, self.background_y))

        self.draw_score()
        self.upgrade_group.draw(self.game_window)
        self.enemy_projectile_group.draw(self.game_window)
        self.enemy_group.draw(self.game_window)
        self.player_projectile_group.draw(self.game_window)
        self.player_group.draw(self.game_window)
        for effect in self.fx_list:
            effect.draw(self.game_window)
        for healthbar in self.healthbars:
            healthbar.draw(self.game_window)

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
            self.handle_upgrade_collision()
            self.handle_projectile_enemy_collision()
            self.handle_projectile_player_collision()

            self.move_background(dt)

            self.draw_window()


if __name__ == "__main__":
    Game().main()