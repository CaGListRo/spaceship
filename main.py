import settings as stgs
from spaceship import Spaceship
from explosion import SmallExplosion
from drone import Drone
from enemy_creator import enemy_creator
from utils import load_image, load_images, create_highscores_screen, sort_and_write_highscores, Animation, Helpsite
from button import Button

from time import time
import pygame as pg
from typing import Final


class Game:
    WHITE: Final[tuple[int]] = (247, 247, 247)

    def __init__(self) -> None:
        """ Initializes the game. """
        pg.init()
        self.main_window: pg.display = pg.display.set_mode(stgs.MAIN_WINDOW_RESOLUTION)
        self.game_window: pg.Surface = pg.Surface(stgs.GAME_WINDOW_RESOLUTION)
        self.fps: int = 0

        self.player_group: pg.sprite.Group = pg.sprite.Group()
        self.drone_group: pg.sprite.Group = pg.sprite.Group()
        self.player_projectile_group: pg.sprite.Group = pg.sprite.Group()
        self.enemy_group: pg.sprite.Group = pg.sprite.Group()
        self.enemy_projectile_group: pg.sprite.Group = pg.sprite.Group()
        self.upgrade_group: pg.sprite.Group = pg.sprite.Group()
        self.fx_list: list[object] = []
        self.healthbars: list[object] = []

        self.assets: dict[function | object] = {
            "background": load_image("backgrounds", "00.png", 1),
            "title": load_image("", "title.png", 1),
            "logo": load_image("", "logo.png", 1),
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
            "bigger_explosion": Animation(load_images("fx/small explosion", scale_factor=1), animation_duration=0.5, loop=False),
        }
        
        self.player_pos: tuple[int] = (stgs.GAME_WINDOW_RESOLUTION[0] // 2, stgs.GAME_WINDOW_RESOLUTION[1] // 5 * 4)
        self.spaceship = Spaceship(self, self.player_group, self.player_projectile_group, self.player_pos)
        self.move_x: list[int] = [0, 0]
        self.move_y: list[int] = [0, 0]

        
        self.score_font: pg.font.Font = pg.font.SysFont("comicsans", 42)
        self.highscores_font: pg.font.Font = pg.font.SysFont("comicsans", 52)
        self.get_ready_text: pg.Surface = self.score_font.render("GET READY!", True, self.WHITE)
        self.fight_text: pg.Surface = self.score_font.render("FIGHT!", True, self.WHITE)
        self.start_text: pg.Surface = self.score_font.render("START!", True, self.WHITE)
        self.game_over_text: pg.Surface = self.highscores_font.render("GAME OVER!", True, self.WHITE)
        self.enter_name_text: pg.Surface = self.highscores_font.render("Enter your name.", True, self.WHITE)
        self.player_name: str = ""

        self.background_start_y: int = -2000
        self.background_y: int = self.background_start_y

        self.lives: int = 3
        self.drones: list[int] = [0, 0]
        self.drones_to_get: int = 0
        self.drones_max: int = 2
        self.run: bool = True
        self.countdown: bool = True
        self.countdown_start_value: float = 3.99999
        self.countdown_time: float = self.countdown_start_value
        self.score: int = 0
        self.phase: int = 1
        self.wave: int = 0
        self.multiplicand: int = 1
        self.sprayer_state: int = 0
        self.enemy_appearance_timer: int | float = 10

        self.game_state: str = "menu"
        self.game_over_timer: int | float = 0
        self.help_site = Helpsite(self)
        self.highscores_site, self.highscores_list = create_highscores_screen(self.highscores_font)

    def add_drones(self) -> None:
        """ Add drones to the sides of the player. (One at a time) """
        for i, _ in enumerate(self.drones):
            if self.drones[i] == 0 and self.drones_to_get > 0:
                self.drones_to_get -= 1
                side_picker = -1 if i == 0 else 1
                self.drones[i] = Drone(self, self.drone_group, self.player_projectile_group, side_picker)

    def handle_upgrade_collision(self) -> None:
        """ Handle collision with upgrade items. """
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
                    self.spaceship.laser_damage = max(self.spaceship.laser_damage - 1, 5 * self.multiplicand)
                    self.spaceship.rocket_damage = max(self.spaceship.rocket_damage - 5, 20 * self.multiplicand)
                elif upgrade.upgrade_number == 3:
                    self.spaceship.laser_damage = min(self.spaceship.laser_damage + 1, 20 * self.multiplicand)
                    self.spaceship.rocket_damage = min(self.spaceship.rocket_damage + 5, 100 * self.multiplicand)
                elif upgrade.upgrade_number == 4:
                    self.spaceship.laser_fire_rate = min(self.spaceship.laser_fire_rate + 0.05, 1)
                    self.spaceship.rocket_fire_rate = min(self.spaceship.rocket_fire_rate + 0.1, 2)
                elif upgrade.upgrade_number == 5:
                    self.spaceship.laser_fire_rate = max(self.spaceship.laser_fire_rate - 0.05, 0.05)
                    self.spaceship.rocket_fire_rate = max(self.spaceship.rocket_fire_rate - 0.1, 0.1)
                elif upgrade.upgrade_number == 6:
                    self.spaceship.max_health = min(self.spaceship.max_health + 10, 100 + 50 * self.multiplicand)
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

    def proceed_level(self) -> None:
        """ Proceed to the next level. """
        self.countdown = True
        self.countdown_time = self.countdown_start_value
        self.phase += 1
        self.wave = 0
        self.background_y = self.background_start_y
        if 1 <= self.phase <= 3:
            self.multiplicand = 1
        elif 4 <= self.phase <= 6:
            self.multiplicand = 2
        elif self.phase > 6:
            self.multiplicand = 3

    def handle_enemy_drone_collision(self) -> None:
        """ Handle collision with the enemy and the drones. """
        for enemy in self.enemy_group:
            overlap = pg.sprite.spritecollide(enemy, self.drone_group, False, pg.sprite.collide_mask)
            if overlap:
                print("test")
                for collided_drone in overlap:
                    collided_drone.take_damage(min(enemy.health, 50))
                    enemy.take_damage(50 * self.multiplicand)

    def handle_enemy_player_collision(self) -> None:
        """ Handle collision with the enemy and the player. """
        for enemy in self.enemy_group:
            if pg.sprite.spritecollide(enemy, self.player_group, False, pg.sprite.collide_mask):
                self.spaceship.take_damage(min(enemy.health, 50))
                enemy.take_damage(150 * self.multiplicand)

    def handle_projectile_player_collision(self) -> None:
        """ Handle collision with the enemy projectiles and the player. """
        for projectile in self.enemy_projectile_group:
            overlap_sprites = pg.sprite.spritecollide(projectile, self.player_group, False, pg.sprite.collide_mask)
            if overlap_sprites:
                for sprite in overlap_sprites:
                    self.fx_list.append(SmallExplosion(self, (projectile.pos.x, projectile.pos.y)))
                    sprite.take_damage(projectile.damage)
                    projectile.kill()

    def handle_projectile_enemy_collision(self) -> None:
        """ Handle collision with the player projectiles and the enemy. """
        for projectile in self.player_projectile_group:
            overlap_sprites = pg.sprite.spritecollide(projectile, self.enemy_group, False, pg.sprite.collide_mask)
            if overlap_sprites:
                for sprite in overlap_sprites:
                    sprite.take_damage(projectile.damage)
                    self.fx_list.append(SmallExplosion(self, (projectile.pos.x, projectile.pos.y)))
                    projectile.kill()
                    self.score += 10

    def handle_enemies(self, dt: float) -> None:
        """
        Creates the new enemy wave after a certain time 
        or if all enemies from the wave before are destroyed.
        """
        self.enemy_appearance_timer += dt
        if len(self.enemy_group) < 1 and self.enemy_appearance_timer >= 10:
            enemy_creator(self, self.enemy_group, self.phase, self.wave, self.multiplicand)
            self.enemy_appearance_timer = 0
            self.wave += 1

    def check_score(self) -> None:
        """ Check if the player has reached the score required to rank in the highscores list. """
        if self.score >= self.highscores_list[-1][1]:
            self.game_state = "game over"
        else:
            self.game_state = "highscores"

    def handle_events(self) -> None:
        """ Handle events such as closing the game window, quitting the game, steering the spaceship, etc. """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

            if self.game_state == "play":
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
                            
            elif self.game_state == "game over":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.player_name = self.player_name[0:-1]
                    elif event.key == pg.K_RETURN:
                        sort_and_write_highscores(self.highscores_list, self.player_name, self.score)
                        self.highscores_site, self.highscores_list = create_highscores_screen(self.highscores_font)
                        self.game_state = "highscores"
                    else:
                        if len(self.player_name) < 8:    
                            self.player_name += event.unicode

    def update_groups(self, dt: float) -> None:
        """ Update the groups of objects in the game. """
        self.player_group.update(dt, self.move_x, self.move_y)
        self.drone_group.update(dt)
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

    def move_background(self, dt: float) -> None:
        """ Move the background of the game. """
        self.background_y += dt * 10
        self.background_y = min(0, self.background_y)

    def handle_live_lost(self) -> None:
        """ Handle the player losing a life. """
        if self.lives > 0:
            for element in self.drone_group:
                element.take_damage(555)
            self.drones = [0, 0]
            self.spaceship = Spaceship(self, self.player_group, self.player_projectile_group, self.player_pos)
            self.lives -= 1
        else:
            self.game_state = "game over"

    def draw_lives(self) -> None:
        """ Draw the lives of the player. """
        if self.lives < 10:
            for i in range(self.lives):
                self.main_window.blit(pg.transform.scale(self.assets["live_image"], (50, 82)), (10, 800 - 90 * i))
        else:
            self.main_window.blit(pg.transform.scale(self.assets["live_image"], (50, 82)), (10, 800))
            lives_to_render = f"x {self.lives}"
            lives_to_blit = self.score_font.render(lives_to_render, True, self.WHITE)
            self.main_window.blit(lives_to_blit, (80, 809))

    def draw_stats_and_score(self) -> None:
        """ Draw the stats and score of the player. """
        score_to_render: str = f"Score: {self.score}"
        score_to_blit: pg.Surface = self.score_font.render(score_to_render, True, self.WHITE)
        self.main_window.blit(score_to_blit, (200, 8))

        fire_power_to_render: str = f"FP: {self.spaceship.current_weapon_damage}"
        fire_power_to_blit: pg.Surface = self.score_font.render(fire_power_to_render, True, self.WHITE)
        self.main_window.blit(fire_power_to_blit, (600, 8))

        fire_rate_to_render: str = f"FR: {round(self.spaceship.current_fire_rate, 2)}"
        fire_rate_to_blit: pg.Surface = self.score_font.render(fire_rate_to_render, True, self.WHITE)
        self.main_window.blit(fire_rate_to_blit, (800, 8))

        hp_to_render: str = f"HP: {self.spaceship.health}/{self.spaceship.max_health}"
        hp_to_blit: pg.Surface = self.score_font.render(hp_to_render, True, self.WHITE)
        self.main_window.blit(hp_to_blit, (1000, 8))

        fps_to_render: str = f"FPS: {self.fps}"
        fps_to_blit: pg.Surface = self.score_font.render(fps_to_render, True, self.WHITE)
        self.main_window.blit(fps_to_blit, (1400, 8))

    def show_countdown(self, dt: float) -> None:
        """ Show the 'get ready' countdown before the game starts. """
        countdown_to_render = self.countdown_time // 1
        if self.countdown_time >= 1:
            countdown_to_blit: pg.Surface = self.score_font.render(str(int(countdown_to_render)), True, self.WHITE)
            self.game_window.blit(countdown_to_blit, (stgs.GAME_WINDOW_RESOLUTION[0] // 2 - countdown_to_blit.get_width() // 2, 
                                                    stgs.GAME_WINDOW_RESOLUTION[1] // 2 - countdown_to_blit.get_height() // 2))
            self.game_window.blit(self.get_ready_text, (stgs.GAME_WINDOW_RESOLUTION[0] // 2 - self.get_ready_text.get_width() // 2, 
                                                        stgs.GAME_WINDOW_RESOLUTION[1] // 2 - 100 ))
        else:
            self.game_window.blit(self.fight_text, (stgs.GAME_WINDOW_RESOLUTION[0] // 2 - self.fight_text.get_width() // 2, 
                                                        stgs.GAME_WINDOW_RESOLUTION[1] // 2 - self.fight_text.get_height() // 2))
        self.countdown_time -= dt
        if self.countdown_time <= 0:
            self.countdown = False

    def draw_window(self, dt: float) -> None:
        """ Draw the game window. """
        self.main_window.blit(pg.transform.scale(self.assets["title"], stgs.MAIN_WINDOW_RESOLUTION), (0, 0))
        if self.game_state == "menu":
            self.main_window.blit(pg.transform.scale(self.assets["logo"], stgs.MAIN_WINDOW_RESOLUTION), (0, 0))
            self.start_button.render()
            self.help_button.render()
            self.highscores_button.render()
            self.quit_button.render()

        elif self.game_state == "help":
            self.help_site.render(self.main_window)
            self.back_button.render()

        elif self.game_state == "highscores":
            self.main_window.blit(self.highscores_site, (0, 0))
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
            self.drone_group.draw(self.game_window)

            for effect in self.fx_list:
                effect.draw(self.game_window)
            for healthbar in self.healthbars:
                healthbar.draw(self.game_window)

            pg.draw.rect(self.main_window, self.WHITE, (190, 90, 1410, 810))
            self.main_window.blit(self.game_window, (195, 95))

        elif self.game_state == "game over":
            if self.game_over_timer < 5:
                self.game_window.blit(self.assets["background"], (0, self.background_y))
                self.game_over_timer += dt
                self.game_window.blit(self.game_over_text, (stgs.GAME_WINDOW_RESOLUTION[0] // 2 - self.game_over_text.get_width() // 2,
                                                            stgs.GAME_WINDOW_RESOLUTION[1] // 2 - self.game_over_text.get_height() // 2))
                pg.draw.rect(self.main_window, self.WHITE, (190, 90, 1410, 810))
                self.main_window.blit(self.game_window, (195, 95))
            elif self.game_over_timer >= 5:
                self.main_window.blit(self.highscores_site, (0, 0))
                player_name_to_blit = self.highscores_font.render(self.player_name, True, self.WHITE)
                pg.draw.rect(self.main_window, self.WHITE, (590, 740, max(30, player_name_to_blit.get_width() + 20), 80), width=3)
                self.main_window.blit(player_name_to_blit, (600, 745))
                self.main_window.blit(self.enter_name_text, (stgs.MAIN_WINDOW_RESOLUTION[0] // 2 - self.enter_name_text.get_width() // 2, 820))
            

        pg.display.update()

    def create_buttons(self) -> None:
        """ Creates the menu buttons. """
        self.start_button = Button(self.main_window, "Start", (1380, 630))
        self.help_button =  Button(self.main_window, "Help", (1380, 700))
        self.highscores_button = Button(self.main_window, "highscores", (1380, 770))
        self.quit_button = Button(self.main_window, "Quit", (1380, 840))
        self.back_button = Button(self.main_window, "back", (200, 800))

    def main(self) -> None:
        """ The main function of the game, containing the game loop. """
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
                if self.highscores_button.check_button_collision():
                    self.game_state = "highscores"
                if self.quit_button.check_button_collision():
                    self.run = False
            elif self.game_state == "help":
                self.help_site.update()
                if self.back_button.check_button_collision():
                    self.game_state = "menu"
            elif self.game_state == "highscores":
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
                    self.handle_enemy_player_collision()
                    self.handle_enemy_drone_collision()
                    self.move_background(dt)

            elif self.game_state == "game over" and self.game_over_timer > 4.5:
                self.check_score()
                

            self.draw_window(dt)


if __name__ == "__main__":
    Game().main()