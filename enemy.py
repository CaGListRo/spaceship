import settings as stgs
from projectile import EnemyProjectile
from healthbar import Healthbar
from upgrades import Upgrade
from icecream import ic

import pygame as pg
from random import randint, choice


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, ship_path, enemy_number, enemy_group, pos, phase):
        super().__init__(enemy_group)
        if 1 <= phase <= 3:
            self.multiplicator = 1
        elif 4 <= phase <= 6:
            self.multiplicator = 2
        elif phase > 6:
            self.multiplicator = 3
        self.game = game
        self.health = enemy_number * 50 * self.multiplicator
        self.max_health = self.health
        self.score_factor = enemy_number
        self.animation = self.game.assets[ship_path + "/idle"].copy()
        self.image = self.animation.get_img()
        self.rect = self.image.get_rect(center = pos)
        self.enemy_mask = pg.mask.from_surface(self.image)
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2(0, 1)
        self.speed_y = 100
        self.killed = False

        self.healthbar = Healthbar(self.game, self.max_health, self.health, self.image.get_width(), self.pos)

    def take_damage(self, damage):
        self.health -= damage
        self.healthbar.update(self.health, self.pos)
        if self.health <= 0:
            self.kill()
            self.killed = True
            self.game.score += 50 * self.score_factor * self.multiplicator
        return self.killed

    def create_mask(self):
        self.enemy_mask = pg.mask.from_surface(self.image)

    def update(self, dt):
        self.animation.update(dt)
        self.image = self.animation.get_img()

        self.direction.y = 1
        self.pos.y += self.direction.y * self.speed_y * dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.healthbar.update(self.health, self.pos)

        if self.pos.y > stgs.GAME_WINDOW_RESOLUTION[1]:
            self.kill()
        
        
class EnemyShip1(Enemy):
    def __init__(self, game, enemy_number, enemy_group, pos, phase):
        super().__init__(game, "enemy1", enemy_number, enemy_group, pos, phase)
        self.shooting_timer = 1 / self.multiplicator
        self.timer = self.shooting_timer
        self.laser_damage = 20 * self.multiplicator
    
    def update(self, dt):
        super().update(dt)
        self.shoot(dt)

    def shoot(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.shooting_timer
            if randint(1, 100) > 80 / self.multiplicator:
                EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() + 10), "red")


class EnemyShip2(Enemy):
    def __init__(self, game,  enemy_number, enemy_group, pos, phase):
        super().__init__(game, "enemy2", enemy_number, enemy_group, pos, phase)
        self.shooting_timer = 0.8 / self.multiplicator
        self.timer = self.shooting_timer
        self.laser_damage = 10 * self.multiplicator
    
    def update(self, dt):
        super().update(dt)
        self.shoot(dt)

    def shoot(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.shooting_timer
            if randint(1, 100) > 80 / self.multiplicator:
                EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2 - 10, self.pos.y + self.image.get_height() + 10), "green")
                EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2 + 10, self.pos.y + self.image.get_height() + 10), "green")


class EnemyShip3(Enemy):
    def __init__(self, game,  enemy_number, enemy_group, pos, phase):
        super().__init__(game, "enemy3", enemy_number, enemy_group, pos, phase)
        self.shooting_timer = 2 / self.multiplicator
        self.timer = self.shooting_timer
        self.rocket_damage = 40 * self.multiplicator

    def update(self, dt):
        super().update(dt)
        self.shoot(dt)

    def shoot(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.shooting_timer
            if randint(1, 100) > 80 / self.multiplicator:
                EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + self.image.get_width() // 2 + 10, self.pos.y + self.image.get_height() + 10), "green")


class Boss1(Enemy):
    def __init__(self, game, enemy_number, enemy_group, pos, phase):
        super().__init__(game, "boss1", enemy_number, enemy_group, pos, phase)
        self.game = game
        self.state = "idle"
        self.state_hold_time = randint(1, (20 // self.multiplicator))
        self.state_timer = 0
        self.speed_x = 50

        self.hold_fire = randint(1, (10 // self.multiplicator))
        self.shoot_timer = 0 
        self.laser_damage = 10 * self.multiplicator
        self.rocket_damage = 40 * self.multiplicator
        self.fire_mode = None
        self.shooting_state = "not shooting"
        self.projectile_interval_timer = 0
        self.shot_counter = 0

        self.active_laser = 0
        self.second_active_laser = 11
        self.laser_shifter = 1
        self.upgrade_counter = 0

        self.game.spaceship.auto_fire = False

    def take_damage(self, damage):
        self.health -= damage
        self.healthbar.update(self.health, self.pos)
        if self.health <= 0:
            self.kill()
            self.killed = True
            self.game.score += 50 * self.score_factor * self.multiplicator
            getattr(self.game, "proceed_level")()
        return self.killed

    def create_mask(self):
        self.mask = pg.mask.from_surface(self.image)    

    def set_x_direction(self):
        if self.state == "left":
            self.direction.x = -1
        elif self.state == "right":
            self.direction.x = 1
        else:
            self.direction.x = 0

    def handle_state(self, dt):
        self.state_timer += dt
        if self.state_timer >= self.state_hold_time:
            old_state = self.state
            self.state = choice(["left", "right", "idle"])
            self.state_hold_time = randint(1, 15)
            self.state_timer = 0
            if old_state != self.state:
                self.handle_image_and_mask()
                self.set_x_direction()

    def handle_image_and_mask(self):
        self.animation = self.game.assets["boss1/" + self.state].copy()
        self.rect = self.image.get_rect(center = self.pos)
        self.create_mask()

    def update(self, dt):
        self.animation.update(dt)
        self.image = self.animation.get_img()
        if self.pos.y < 10:
            self.direction.y = 1
            self.direction.x = 0
        
        elif self.pos.y >= 10 and self.speed_y > 0:
            self.speed_y = max(0, self.speed_y - dt * 150)
            
        else:
            if not self.game.spaceship.auto_fire:
                self.game.spaceship.auto_fire = True
            self.direction.y = 0
            self.handle_state(dt)
            if self.shooting_state == "not shooting":
                self.handle_shooting(dt)
                
        self.pos.y += self.direction.y * self.speed_y * dt
        self.pos.x += self.direction.x * self.speed_x * dt

        if self.pos.x < 0:
            self.pos.x = 0
            self.direction.x *= -1
            self.state = "right"
            self.handle_image_and_mask()

        if self.pos.x + self.image.get_width() > stgs.GAME_WINDOW_RESOLUTION[0]:
            self.pos.x = stgs.GAME_WINDOW_RESOLUTION[0] - self.image.get_width()
            self.direction.x *= -1
            self.state = "left"
            self.handle_image_and_mask()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.healthbar.update(self.health, self.pos)
        self.handle_fire_modi(dt)

    def handle_shooting(self, dt):
        self.shoot_timer += dt
        if self.shoot_timer >= self.hold_fire:
            self.fire_mode = choice(["all", "cylone", "knight_rider", "laola", "random", "rocket"])
            self.shooting_state = "shooting"

    def reset_shooting(self):
        self.shooting_state = "not shooting"
        self.shoot_timer = 0
        self.hold_fire = randint(1, 10)
        self.shot_counter = 0

    def handle_fire_modi(self, dt):
        if self.shooting_state == "shooting":
            self.projectile_interval_timer += dt

            if self.fire_mode == "all":
                if self.projectile_interval_timer >= 1:
                    for i in range(13):
                        self.fire_weapon(i + 1)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                    if self.shot_counter > 10:
                        self.reset_shooting()

            elif self.fire_mode == "cylone":
                if self.projectile_interval_timer >= 0.1:
                    self.active_laser += self.laser_shifter
                    self.second_active_laser -= self.laser_shifter
                        
                    if self.active_laser > 5:
                        self.active_laser = 4
                        self.second_active_laser = 7
                        self.laser_shifter *= -1
                    elif self.active_laser < 1:
                        self.active_laser = 2
                        self.second_active_laser = 9
                        self.laser_shifter *= -1
                    self.fire_weapon(self.active_laser)
                    self.fire_weapon(self.second_active_laser)
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1

                        
                if self.shot_counter > 47:
                    self.reset_shooting()
                    self.active_laser = 0
                    self.second_active_laser = 11

            elif self.fire_mode == "knight_rider":
                if self.projectile_interval_timer >= 0.1:
                    self.active_laser += self.laser_shifter
                    if self.active_laser > 10:
                        self.active_laser = 9
                        self.laser_shifter *= -1
                    elif self.active_laser < 1:
                        self.active_laser = 2
                        self.laser_shifter *= -1
                    self.fire_weapon(self.active_laser)
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1
                        
                if self.shot_counter > 90:
                    self.reset_shooting()
                    self.active_laser = 0
            
            elif self.fire_mode == "laola":
                if self.projectile_interval_timer >= 0.1:
                    self.active_laser += self.laser_shifter
                    if self.active_laser > 10:
                        self.active_laser = 1
                    self.fire_weapon(self.active_laser)
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1
                        
                if self.shot_counter >= 100:
                    self.reset_shooting()
                    self.active_laser = 0

            elif self.fire_mode == "random":
                if self.projectile_interval_timer >= 0.5:
                    laser_number = randint(1, 10)
                    self.fire_weapon(laser_number)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                    if self.shot_counter > 10:
                        self.reset_shooting()

            elif self.fire_mode == "rocket":
                if self.projectile_interval_timer >= 1:
                    self.fire_weapon(11)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                if self.shot_counter > 10:
                    self.reset_shooting()

            if self.upgrade_counter >= self.multiplicator and len(self.game.upgrade_group) < 1:
                Upgrade(self.game, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() // 2))
                self.reset_shooting()

    def fire_weapon(self, weapon_number):
        if weapon_number == 1:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 232, self.pos.y + self.image.get_height() - 166), "red")       
        elif weapon_number == 2:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 248, self.pos.y + self.image.get_height() - 152), "red")
        elif weapon_number == 3:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 264, self.pos.y + self.image.get_height() - 142), "red")
        elif weapon_number == 4:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 279, self.pos.y + self.image.get_height() - 125), "red")       
        elif weapon_number == 5:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 295, self.pos.y + self.image.get_height() - 110), "red")       
        elif weapon_number == 6:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 456, self.pos.y + self.image.get_height() - 110), "red")
        elif weapon_number == 7:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 472, self.pos.y + self.image.get_height() - 125), "red")
        elif weapon_number == 8:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 487, self.pos.y + self.image.get_height() - 142), "red")
        elif weapon_number == 9:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 502, self.pos.y + self.image.get_height() - 152), "red")
        elif weapon_number == 10:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 518, self.pos.y + self.image.get_height() - 166), "red")
        elif weapon_number == 11:
            EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() - 20), "green")


class Boss2(Enemy):
    def __init__(self, game,  enemy_number, enemy_group, pos, phase):
        super().__init__(game, "boss2", enemy_number, enemy_group, pos, phase)
        self.game = game
        self.state = "flight"
        self.state_hold_time = randint(1, (20 // self.multiplicator))
        self.state_timer = 0
        self.speed_x = 50

        self.animation = self.game.assets["boss2/" + self.state].copy()
        self.rect = self.image.get_rect(center = self.pos)

        self.hold_fire = randint(1, (10 // self.multiplicator))
        self.shoot_timer = 0 
        self.laser_damage = 15 * self.multiplicator
        self.rocket_damage = 50 * self.multiplicator
        self.fire_mode = None
        self.shooting_state = "not shooting"
        self.projectile_interval_timer = 0
        self.shot_counter = 0

        self.active_laser = 0
        self.second_active_laser = 11
        self.laser_shifter = 1
        self.upgrade_counter = 0

        self.game.spaceship.auto_fire = False
        for drone in self.game.drones:
            if drone != 0:
                drone.auto_fire = False
        self.start_fight = False

    def take_damage(self, damage):
        self.health -= damage
        self.healthbar.update(self.health, self.pos)
        if self.health <= 0:
            self.kill()
            self.killed = True
            self.game.score += 50 * self.score_factor * self.multiplicator
            getattr(self.game, "proceed_level")()
        return self.killed

    def create_mask(self):
        self.mask = pg.mask.from_surface(self.image)    

    def set_x_direction(self):
        if self.state == "left":
            self.direction.x = -1
        elif self.state == "right":
            self.direction.x = 1
        else:
            self.direction.x = 0

    def handle_state(self, dt):
        self.state_timer += dt
        if self.state_timer >= self.state_hold_time:
            old_state = self.state
            self.state = choice(["left", "right", "idle"])
            self.state_hold_time = randint(1, 15)
            self.state_timer = 0
            if old_state != self.state:
                self.handle_image_and_mask()
                self.set_x_direction()

    def handle_image_and_mask(self):
        self.animation = self.game.assets["boss2/" + self.state].copy()
        self.rect = self.image.get_rect(center = self.pos)
        self.create_mask()

    def update(self, dt):
        if self.state != "open":
            self.animation.update(dt)
            self.image = self.animation.get_img()

        if self.pos.y < 10:
            self.direction.y = 1
            self.direction.x = 0

        elif self.pos.y >= 10 and self.speed_y > 0:
            self.speed_y = max(0, self.speed_y - dt * 150)

        elif self.pos.y >= 10 and self.speed_y <= 0 and not self.start_fight:
            if self.state != "open":
                self.state = "open"
                self.animation = self.game.assets["boss2/" + self.state].copy()
            self.image = self.animation.get_img()
            self.animation.update(dt)

            if self.animation.done:
                self.state = "idle"
                self.handle_state(dt)
                self.handle_image_and_mask()
                self.start_fight = True
            
        elif self.pos.y >= 10 and self.start_fight:
            if not self.game.spaceship.auto_fire:
                self.game.spaceship.auto_fire = True
            self.direction.y = 0
            self.handle_state(dt)

            if self.shooting_state == "not shooting":
                self.handle_shooting(dt)
                
        self.pos.y += self.direction.y * self.speed_y * dt
        self.pos.x += self.direction.x * self.speed_x * dt

        if self.pos.x < 0:
            self.pos.x = 0
            self.direction.x *= -1
            self.state = "right"
            self.handle_image_and_mask()

        if self.pos.x + self.image.get_width() > stgs.GAME_WINDOW_RESOLUTION[0]:
            self.pos.x = stgs.GAME_WINDOW_RESOLUTION[0] - self.image.get_width()
            self.direction.x *= -1
            self.state = "left"
            self.handle_image_and_mask()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.healthbar.update(self.health, self.pos)
        self.handle_fire_modi(dt)

    def handle_shooting(self, dt):
        self.shoot_timer += dt
        if self.shoot_timer >= self.hold_fire:
            self.fire_mode = choice(["all", "cylone", "knight_rider", "laola", "random", "rocket", "spray"])
            self.shooting_state = "shooting"

    def reset_shooting(self):
        self.shooting_state = "not shooting"
        self.shoot_timer = 0
        self.hold_fire = randint(1, 10)
        self.shot_counter = 0

    def handle_fire_modi(self, dt):
        if self.shooting_state == "shooting":
            self.upgrade_counter += 1
            self.projectile_interval_timer += dt

            if self.fire_mode == "all":
                if self.projectile_interval_timer >= 1:
                    for i in range(13):
                        self.fire_weapon(i + 1)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                    if self.shot_counter > 10:
                        self.reset_shooting()

            elif self.fire_mode == "cylone":
                if self.projectile_interval_timer >= 0.1:
                    self.active_laser += self.laser_shifter
                    self.second_active_laser -= self.laser_shifter
                        
                    if self.active_laser > 5:
                        self.active_laser = 4
                        self.second_active_laser = 7
                        self.laser_shifter *= -1
                    elif self.active_laser < 1:
                        self.active_laser = 2
                        self.second_active_laser = 9
                        self.laser_shifter *= -1
                    self.fire_weapon(self.active_laser)
                    self.fire_weapon(self.second_active_laser)
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1

                        
                if self.shot_counter > 47:
                    self.reset_shooting()
                    self.active_laser = 0
                    self.second_active_laser = 11

            elif self.fire_mode == "knight_rider":
                if self.projectile_interval_timer >= 0.1:
                    self.active_laser += self.laser_shifter
                    if self.active_laser > 10:
                        self.active_laser = 9
                        self.laser_shifter *= -1
                    elif self.active_laser < 1:
                        self.active_laser = 2
                        self.laser_shifter *= -1
                    self.fire_weapon(self.active_laser)
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1
                        
                if self.shot_counter > 90:
                    self.reset_shooting()
                    self.active_laser = 0
            
            elif self.fire_mode == "laola":
                if self.projectile_interval_timer >= 0.1:
                    self.active_laser += self.laser_shifter
                    if self.active_laser > 10:
                        self.active_laser = 1
                    self.fire_weapon(self.active_laser)
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1
                        
                if self.shot_counter >= 100:
                    self.reset_shooting()
                    self.active_laser = 0

            elif self.fire_mode == "random":
                if self.projectile_interval_timer >= 0.5:
                    laser_number = randint(1, 10)
                    self.fire_weapon(laser_number)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                    if self.shot_counter > 10:
                        self.reset_shooting()

            elif self.fire_mode == "rocket":
                if self.projectile_interval_timer >= 1:
                    self.fire_weapon(11)
                    self.fire_weapon(12)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                if self.shot_counter > 10:
                    self.reset_shooting()

            elif self.fire_mode == "spray":
                if self.projectile_interval_timer >= 0.5:
                    self.fire_weapon(13)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                if self.shot_counter > 10:
                    self.reset_shooting()

            if self.upgrade_counter >= self.multiplicator and len(self.game.upgrade_group) < 1:
                Upgrade(self.game, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() // 2))
                self.upgrade_counter = 0

    def fire_weapon(self, weapon_number):
        if weapon_number == 1:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 96, self.pos.y + 202), "green")      
        elif weapon_number == 2:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 117, self.pos.y + 184), "green")
        elif weapon_number == 3:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 138, self.pos.y + 175), "green")
        elif weapon_number == 4:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 159, self.pos.y + 171), "green")       
        elif weapon_number == 5:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 180, self.pos.y + 176), "green")       
        elif weapon_number == 6:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 571, self.pos.y + 176), "green")
        elif weapon_number == 7:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 592, self.pos.y + 171), "green")
        elif weapon_number == 8:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 613, self.pos.y + 175), "green")
        elif weapon_number == 9:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 634, self.pos.y + 184), "green")
        elif weapon_number == 10:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 655, self.pos.y + 202), "green")
        elif weapon_number == 11:
            EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + 46, self.pos.y + 188), "green")
        elif weapon_number == 12:
            EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + 703, self.pos.y + 188), "green")
        elif weapon_number == 13:  # sprayer
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 265), "green", 240)
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 265), "green", 270)
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 265), "green", 300)


class Boss3(Enemy):
    def __init__(self, game,  enemy_number, enemy_group, pos, phase):
        super().__init__(game, "boss3", enemy_number, enemy_group, pos, phase)
        self.game = game
        self.state = "flight"
        self.state_hold_time = randint(1, (20 // self.multiplicator))
        self.state_timer = 0
        self.speed_x = 50

        self.animation = self.game.assets["boss3/" + self.state].copy()
        self.rect = self.image.get_rect(center = self.pos)

        self.hold_fire = randint(1, (10 // self.multiplicator))
        self.shoot_timer = 0 
        self.laser_damage = 20
        self.rocket_damage = 80
        self.fire_mode = None
        self.shooting_state = "not shooting"
        self.projectile_interval_timer = 0
        self.shot_counter = 0

        self.active_laser = 0
        self.second_active_laser = 25
        self.laser_shifter = 1
        self.upgrade_counter = 0

        self.game.spaceship.auto_fire = False
        for drone in self.game.drones:
            if drone != 0:
                drone.auto_fire = False
        self.start_fight = False

    def take_damage(self, damage):
        self.health -= damage
        self.healthbar.update(self.health, self.pos)
        if self.health <= 0:
            self.kill()
            self.killed = True
            self.game.score += 50 * self.score_factor * self.multiplicator
            getattr(self.game, "proceed_level")()
        return self.killed

    def create_mask(self):
        self.mask = pg.mask.from_surface(self.image)    

    def set_x_direction(self):
        if self.state == "left":
            self.direction.x = -1
        elif self.state == "right":
            self.direction.x = 1
        else:
            self.direction.x = 0

    def handle_state(self, dt):
        self.state_timer += dt
        if self.state_timer >= self.state_hold_time:
            old_state = self.state
            self.state = choice(["left", "right", "idle"])
            self.state_hold_time = randint(1, 15)
            self.state_timer = 0
            if old_state != self.state:
                self.handle_image_and_mask()
                self.set_x_direction()

    def handle_image_and_mask(self):
        self.animation = self.game.assets["boss3/" + self.state].copy()
        self.rect = self.image.get_rect(center = self.pos)
        self.create_mask()

    def update(self, dt):
        if self.state != "open":
            self.animation.update(dt)
            self.image = self.animation.get_img()

        if self.pos.y < 10:
            self.direction.y = 1
            self.direction.x = 0

        elif self.pos.y >= 10 and self.speed_y > 0:
            self.speed_y = max(0, self.speed_y - dt * 150)

        elif self.pos.y >= 10 and self.speed_y <= 0 and not self.start_fight:
            if self.state != "open":
                self.state = "open"
                self.animation = self.game.assets["boss3/" + self.state].copy()
            self.image = self.animation.get_img()
            self.animation.update(dt)

            if self.animation.done:
                self.state = "idle"
                self.handle_state(dt)
                self.handle_image_and_mask()
                self.start_fight = True
            
        elif self.pos.y >= 10 and self.start_fight:
            if not self.game.spaceship.auto_fire:
                self.game.spaceship.auto_fire = True
            self.direction.y = 0
            self.handle_state(dt)

            if self.shooting_state == "not shooting":
                self.handle_shooting(dt)
                
        self.pos.y += self.direction.y * self.speed_y * dt
        self.pos.x += self.direction.x * self.speed_x * dt

        if self.pos.x < 0:
            self.pos.x = 0
            self.direction.x *= -1
            self.state = "right"
            self.handle_image_and_mask()

        if self.pos.x + self.image.get_width() > stgs.GAME_WINDOW_RESOLUTION[0]:
            self.pos.x = stgs.GAME_WINDOW_RESOLUTION[0] - self.image.get_width()
            self.direction.x *= -1
            self.state = "left"
            self.handle_image_and_mask()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.healthbar.update(self.health, self.pos)
        self.handle_fire_modi(dt)

    def handle_shooting(self, dt):
        self.shoot_timer += dt
        if self.shoot_timer >= self.hold_fire:
            self.fire_mode = choice(["all", "cylone", "knight_rider", "laola", "random", "rocket", "spray"])
            self.shooting_state = "shooting"

    def reset_shooting(self):
        self.shooting_state = "not shooting"
        self.shoot_timer = 0
        self.hold_fire = randint(1, 10)
        self.shot_counter = 0

    def handle_fire_modi(self, dt):
        if self.shooting_state == "shooting":
            self.upgrade_counter += 1
            self.projectile_interval_timer += dt

            if self.fire_mode == "all":
                if self.projectile_interval_timer >= 1:
                    for i in range(27):
                        self.fire_weapon(i + 1)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                    if self.shot_counter > 10:
                        self.reset_shooting()

            elif self.fire_mode == "cylone":
                if self.projectile_interval_timer >= 0.1:
                    self.active_laser += self.laser_shifter
                    self.second_active_laser -= self.laser_shifter
                        
                    if self.active_laser > 12:
                        self.active_laser = 11
                        self.second_active_laser = 14
                        self.laser_shifter *= -1
                    elif self.active_laser < 1:
                        self.active_laser = 2
                        self.second_active_laser = 23
                        self.laser_shifter *= -1
                    self.fire_weapon(self.active_laser)
                    self.fire_weapon(self.second_active_laser)
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1

                        
                if self.shot_counter > 115:
                    self.reset_shooting()
                    self.active_laser = 0
                    self.second_active_laser = 25

            elif self.fire_mode == "knight_rider":
                if self.projectile_interval_timer >= 0.1:
                    self.active_laser += self.laser_shifter
                    if self.active_laser > 24:
                        self.active_laser = 23
                        self.laser_shifter *= -1
                    elif self.active_laser < 1:
                        self.active_laser = 2
                        self.laser_shifter *= -1
                    self.fire_weapon(self.active_laser)
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1
                        
                if self.shot_counter > 235:
                    self.reset_shooting()
                    self.active_laser = 0
            
            elif self.fire_mode == "laola":
                if self.projectile_interval_timer >= 0.1:
                    self.active_laser += self.laser_shifter
                    if self.active_laser > 24:
                        self.active_laser = 1
                    self.fire_weapon(self.active_laser)
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1
                        
                if self.shot_counter >= 100:
                    self.reset_shooting()
                    self.active_laser = 0

            elif self.fire_mode == "random":
                if self.projectile_interval_timer >= 0.1:
                    laser_number = randint(1, 24)
                    self.fire_weapon(laser_number)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                    if self.shot_counter > 50:
                        self.reset_shooting()

            elif self.fire_mode == "rocket":
                if self.projectile_interval_timer >= 1:
                    self.fire_weapon(25)
                    self.fire_weapon(26)
                    self.fire_weapon(27)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                if self.shot_counter > 10:
                    self.reset_shooting()

            elif self.fire_mode == "spray":
                if self.projectile_interval_timer >= 0.5:
                    self.fire_weapon(28)
                    self.fire_weapon(29)
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                if self.shot_counter > 10:
                    self.reset_shooting()

            if self.upgrade_counter >= self.multiplicator and len(self.game.upgrade_group) < 1:
                self.upgrade_counter = 0
                Upgrade(self.game, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() // 2))


    def fire_weapon(self, weapon_number):
        if weapon_number == 1:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 122, self.pos.y + 214), "violet")      
        elif weapon_number == 2:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 134, self.pos.y + 218), "violet")
        elif weapon_number == 3:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 147, self.pos.y + 223), "violet")
        elif weapon_number == 4:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 159, self.pos.y + 227), "violet")       
        elif weapon_number == 5:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 172, self.pos.y + 231), "violet")       
        elif weapon_number == 6:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 185, self.pos.y + 236), "violet")
        elif weapon_number == 7:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 281, self.pos.y + 257), "violet")
        elif weapon_number == 8:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 294, self.pos.y + 259), "violet")
        elif weapon_number == 9:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 306, self.pos.y + 260), "violet")
        elif weapon_number == 10:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 319, self.pos.y + 262), "violet")
        elif weapon_number == 11:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 331, self.pos.y + 263), "violet")
        elif weapon_number == 12:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 344, self.pos.y + 265), "violet")

        elif weapon_number == 13:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 407, self.pos.y + 265), "violet")      
        elif weapon_number == 14:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 420, self.pos.y + 263), "violet")
        elif weapon_number == 15:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 432, self.pos.y + 262), "violet")
        elif weapon_number == 16:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 445, self.pos.y + 260), "violet")       
        elif weapon_number == 17:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 458, self.pos.y + 259), "violet")       
        elif weapon_number == 18:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 470, self.pos.y + 257), "violet")
        elif weapon_number == 19:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 566, self.pos.y + 236), "violet")
        elif weapon_number == 20:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 579, self.pos.y + 231), "violet")
        elif weapon_number == 21:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 592, self.pos.y + 227), "violet")
        elif weapon_number == 22:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 604, self.pos.y + 223), "violet")
        elif weapon_number == 23:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 617, self.pos.y + 218), "violet")
        elif weapon_number == 24:
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 629, self.pos.y + 214), "violet")

        elif weapon_number == 25:
            EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + 251, self.pos.y + 290), "violet")
        elif weapon_number == 26:
            EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + 358), "violet")
        elif weapon_number == 27:
            EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + 501, self.pos.y + 290), "violet")

        elif weapon_number == 28:  # sprayer
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 53, self.pos.y + 158), "green", 240)
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 53, self.pos.y + 158), "green", 270)
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 53, self.pos.y + 158), "green", 300)
        elif weapon_number == 29:  # sprayer
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 697, self.pos.y + 158), "green", 240)
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 697, self.pos.y + 158), "green", 270)
            EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 697, self.pos.y + 158), "green", 300)
