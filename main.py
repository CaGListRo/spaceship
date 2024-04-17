import settings as stgs
from spaceship import Spaceship
from upgrades import Upgrade
from explosion import ShipExplosion, SmallExplosion
from drone import Drone
from enemy_creator import enemy_creator
from utils import load_image, load_images, Animation, help_site_creator
from button import Button

from time import time
import pygame as pg


class Game:
    def __init__(self) -> None:
        pg.init()
        self.main_window = pg.display.set_mode(stgs.MAIN_WINDOW_RESOLUTION)
        self.game_window = pg.Surface(stgs.GAME_WINDOW_RESOLUTION)
        self.fps = 0

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
            "live_image": load_image("", "spaceship.png", 1),
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
            "boss1/flight": Animation(load_images("enemies/boss1/flight", scale_factor=0.75), animation_duration=0.5, loop=True),
            "boss1/open": Animation(load_images("enemies/boss1/open", scale_factor=0.75), animation_duration=2, loop=False),
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

        self.help_font = pg.font.SysFont("comicsans", 32)
        self.score_font = pg.font.SysFont("comicsans", 42)
        self.get_ready_text = self.score_font.render("GET READY!", True, (247, 247, 247))

        self.background_start_y = -2000
        self.background_y = self.background_start_y

        self.lives = 3
        self.drones = [0, 0]
        self.drones_to_get = 0
        self.drones_max = 2
        self.run = True
        self.countdown = True
        self.countdown_start_value = 3.99999
        self.countdown_time = self.countdown_start_value
        self.score = 0
        self.phase = 1
        self.wave = 0
        self.multiplicator = 1
        self.sprayer_state = 0
        self.enemy_appearance_timer = 10

        self.game_state = "menu"
        self.help_site = help_site_creator(self, self.help_font)

    def add_drones(self):
        for i, _ in enumerate(self.drones):
            if self.drones[i] == 0 and self.drones_to_get > 0:
                self.drones_to_get -= 1
                side_picker = -1 if i == 0 else 1
                self.drones[i] = Drone(self, self.player_group, self.player_projectile_group, side_picker)

    def handle_upgrade_collision(self):
        for upgrade in self.upgrade_group:
            if pg.sprite.spritecollide(upgrade, self.player_group, False, pg.sprite.collide_mask):
                self.score += 5
                if upgrade.upgrade_number == 0:
                    self.drones_to_get = min(self.drones_to_get + 1, self.drones_max)  # drone/s
                    if self.drones[0] == 0 or self.drones[1] == 0:
                        self.add_drones()
                elif upgrade.upgrade_number == 1:
                    self.lives += 1
                elif upgrade.upgrade_number == 2:
                    self.spaceship.laser_damage = max(self.spaceship.laser_damage - 1, 5 * self.multiplicator)
                    self.spaceship.rocket_damage = max(self.spaceship.rocket_damage - 5, 20 * self.multiplicator)
                elif upgrade.upgrade_number == 3:
                    self.spaceship.laser_damage = min(self.spaceship.laser_damage + 1, 20 * self.multiplicator)
                    self.spaceship.rocket_damage = min(self.spaceship.rocket_damage + 5, 100 * self.multiplicator)
                elif upgrade.upgrade_number == 4:
                    self.spaceship.laser_fire_rate = min(self.spaceship.laser_fire_rate + 0.05, 1)
                    self.spaceship.rocket_fire_rate = min(self.spaceship.rocket_fire_rate + 0.1, 2)
                elif upgrade.upgrade_number == 5:
                    self.spaceship.laser_fire_rate = max(self.spaceship.laser_fire_rate - 0.05, 0.05)
                    self.spaceship.rocket_fire_rate = max(self.spaceship.rocket_fire_rate - 0.1, 0.1)
                elif upgrade.upgrade_number == 6:
                    self.spaceship.max_health += 10
                    getattr(self.spaceship, "update_healthbar")()
                elif upgrade.upgrade_number == 7:
                    self.spaceship.health = min(self.spaceship.health + 25, self.spaceship.max_health)
                elif upgrade.upgrade_number == 8:
                    self.spaceship.weapon = "laser"  # parallel fire
                    self.spaceship.current_weapon_damage = self.spaceship.laser_damage
                    self.spaceship.current_fire_rate = self.spaceship.laser_fire_rate
                    self.sprayer_state = 0
                elif upgrade.upgrade_number == 9:
                    self.spaceship.weapon = "rocket_launcher"  # rockets
                    self.spaceship.current_weapon_damage = self.spaceship.rocket_damage
                    self.spaceship.current_fire_rate = self.spaceship.rocket_fire_rate
                    self.sprayer_state = 0
                elif upgrade.upgrade_number == 10:
                    self.spaceship.weapon = "sprayer"  # spray
                    self.spaceship.current_weapon_damage = self.spaceship.laser_damage
                    self.spaceship.current_fire_rate = self.spaceship.laser_fire_rate
                    self.sprayer_state = 3 if self.sprayer_state == 0 else 5

                upgrade.kill()

    def proceed_level(self):
        self.countdown = True
        self.countdown_time = self.countdown_start_value
        self.phase += 1
        self.wave = 0
        self.background_y = self.background_start_y
        if 1 <= self.phase <= 3:
            self.multiplicator = 1
        elif 4 <= self.phase <= 6:
            self.multiplicator = 2
        elif self.phase > 6:
            self.multiplicator = 3

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

    def handle_enemies(self, dt):
        self.enemy_appearance_timer += dt
        if len(self.enemy_group) < 1 and self.enemy_appearance_timer >= 10:
            enemy_creator(self, self.enemy_group, self.phase, self.wave)
            self.enemy_appearance_timer = 0
            self.wave += 1

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

            if not self.countdown:
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

    def move_background(self, dt):
        self.background_y += dt * 10
        self.background_y = min(0, self.background_y)

    def handle_live_lost(self):
        if self.lives > 0:
            for element in self.player_group:
                element.kill()
            self.drones = [0, 0]
            self.spaceship = Spaceship(self, self.player_group, self.player_projectile_group, self.player_pos)
            self.lives -= 1
        else:
            self.run = False

    def draw_lives(self):
            if self.lives < 10:
                for i in range(self.lives):
                    self.main_window.blit(pg.transform.scale(self.assets["live_image"], (50, 82)), (10, 800 - 90 * i))
            else:
                self.main_window.blit(pg.transform.scale(self.assets["live_image"], (50, 82)), (10, 800))
                lives_to_render = f"x {self.lives}"
                lives_to_blit = self.score_font.render(lives_to_render, True, (247, 247, 247))
                self.main_window.blit(lives_to_blit, (80, 809))

    def draw_stats_and_score(self):
        score_to_render = f"Score: {self.score}"
        score_to_blit = self.score_font.render(score_to_render, True, (247, 247, 247))
        self.main_window.blit(score_to_blit, (200, 8))

        fire_power_to_render = f"FP: {self.spaceship.current_weapon_damage}"
        fire_power_to_blit = self.score_font.render(fire_power_to_render, True, (247, 247, 247))
        self.main_window.blit(fire_power_to_blit, (600, 8))

        fire_rate_to_render = f"FR: {round(self.spaceship.current_fire_rate, 2)}"
        fire_rate_to_blit = self.score_font.render(fire_rate_to_render, True, (247, 247, 247))
        self.main_window.blit(fire_rate_to_blit, (800, 8))

        hp_to_render = f"HP: {self.spaceship.health}/{self.spaceship.max_health}"
        hp_to_blit = self.score_font.render(hp_to_render, True, (247, 247, 247))
        self.main_window.blit(hp_to_blit, (1000, 8))

        fps_to_render = f"FPS: {self.fps}"
        fps_to_blit = self.score_font.render(fps_to_render, True, (247, 247, 247))
        self.main_window.blit(fps_to_blit, (1400, 8))

    def show_countdown(self, dt):     
        countdown_to_render = self.countdown_time // 1
        countdown_to_blit = self.score_font.render(str(int(countdown_to_render)), True, (247, 247, 247))
        self.game_window.blit(countdown_to_blit, (stgs.GAME_WINDOW_RESOLUTION[0] // 2 - countdown_to_blit.get_width() // 2, 
                                                  stgs.GAME_WINDOW_RESOLUTION[1] // 2 - countdown_to_blit.get_height() // 2))
        self.game_window.blit(self.get_ready_text, (stgs.GAME_WINDOW_RESOLUTION[0] // 2 - self.get_ready_text.get_width() // 2, 
                                                    stgs.GAME_WINDOW_RESOLUTION[1] // 2 - 100 ))
        self.countdown_time -= dt
        if self.countdown_time <= 0:
            self.countdown = False

    def draw_window(self, dt):
        self.main_window.blit(pg.transform.scale(self.assets["title"], (1600, 900)), (0, 0))
        if self.game_state == "menu":
            self.start_button.render()
            self.help_button.render()
        elif self.game_state == "help":
            self.main_window.blit(self.help_site, (0, 0))
            self.back_button.render()
        elif self.game_state == "play":
            self.game_window.blit(self.assets["background"], (0, self.background_y))

            self.draw_stats_and_score()
            self.draw_lives()
            if not self.countdown:
                self.upgrade_group.draw(self.game_window)
                self.enemy_projectile_group.draw(self.game_window)
                self.enemy_group.draw(self.game_window)
                self.player_projectile_group.draw(self.game_window)
            else:
                self.show_countdown(dt)
            self.player_group.draw(self.game_window)

            for effect in self.fx_list:
                effect.draw(self.game_window)
            for healthbar in self.healthbars:
                healthbar.draw(self.game_window)

            pg.draw.rect(self.main_window, (247, 247, 247), (190, 90, 1410, 810))
            self.main_window.blit(self.game_window, (195, 95))
        pg.display.update()

    def create_buttons(self):
        self.start_button = Button(self.main_window, "Start", (1300, 700))
        self.help_button =  Button(self.main_window, "Help", (1300, 800))
        self.back_button = Button(self.main_window, "back", (200, 800))

    def main(self):
        frame_counter = 0
        time_counter = 0
        self.create_buttons()
        last_time = time()
        while self.run:
            dt = time() - last_time
            last_time = time()
            self.handle_events()

            if self.game_state == "menu":
                if self.start_button.check_button_collision():
                    self.game_state = "play"
                if self.help_button.check_button_collision():
                    self.game_state = "help"
            elif self.game_state == "help":
                if self.back_button.check_button_collision():
                    self.game_state = "menu"

            elif self.game_state == "play":
                frame_counter += 1
                time_counter += dt
                if time_counter > 1:
                    self.fps = frame_counter
                    frame_counter = 0
                    time_counter = 0
                if not self.countdown:
                    self.handle_enemies(dt)
                    self.update_groups(dt)
                    self.handle_upgrade_collision()
                    self.handle_projectile_enemy_collision()
                    self.handle_projectile_player_collision()
                    self.move_background(dt)
                

            self.draw_window(dt)


if __name__ == "__main__":
    Game().main()