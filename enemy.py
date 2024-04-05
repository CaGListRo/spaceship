import settings as stgs
from projectile import EnemyProjectile
from healthbar import Healthbar
from upgrades import Upgrade

import pygame as pg
from random import randint, choice


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, ship_path, enemy_number, enemy_group, pos):
        super().__init__(enemy_group)
        self.game = game
        self.health = enemy_number * 50
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
            self.game.score += 50 * self.score_factor
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
    def __init__(self, game, enemy_number, enemy_group, pos):
        super().__init__(game, "enemy1", enemy_number, enemy_group, pos)
        self.shooting_timer = 1
        self.timer = self.shooting_timer
        self.laser_damage = 20
    
    def update(self, dt):
        super().update(dt)
        self.shoot(dt)

    def shoot(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.shooting_timer
            if randint(1, 100) > 80:
                EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() + 10), "red")


class EnemyShip2(Enemy):
    def __init__(self, game,  enemy_number, enemy_group, pos):
        super().__init__(game, "enemy2", enemy_number, enemy_group, pos)
        self.shooting_timer = 0.8
        self.timer = self.shooting_timer
        self.laser_damage = 10
    
    def update(self, dt):
        super().update(dt)
        self.shoot(dt)

    def shoot(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.shooting_timer
            if randint(1, 100) > 80:
                EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2 - 10, self.pos.y + self.image.get_height() + 10), "green")
                EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + self.image.get_width() // 2 + 10, self.pos.y + self.image.get_height() + 10), "green")


class EnemyShip3(Enemy):
    def __init__(self, game,  enemy_number, enemy_group, pos):
        super().__init__(game, "enemy3", enemy_number, enemy_group, pos)
        self.shooting_timer = 2
        self.timer = self.shooting_timer
        self.rocket_damage = 40

    def update(self, dt):
        super().update(dt)
        self.shoot(dt)

    def shoot(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.shooting_timer
            if randint(1, 100) > 80:
                EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + self.image.get_width() // 2 + 10, self.pos.y + self.image.get_height() + 10), "green")


class Boss1(Enemy):
    def __init__(self, game,  enemy_number, enemy_group, pos):
        super().__init__(game, "boss1", enemy_number, enemy_group, pos)
        self.state = "idle"
        self.state_hold_time = randint(1, 15)
        self.state_timer = 0
        self.speed_x = 50
        self.laser_damage = 20
        self.rocket_damage = 80
        self.fire_mode = "normal"
        self.shoot_timer = 0
        self.single_shot_timer = 0
        self.hold_fire = randint(1, 10)
        self.shooting_state = "not shooting"
        self.projectile_interval_timer = 0
        self.shot_counter = 0
        self.laser_states = {"laser 1": "ready", 
                             "laser 2": "not ready", 
                             "laser 3": "not ready", 
                             "laser 4": "not ready", 
                             "laser 5": "not ready", 
                             "laser 6": "not ready", 
                             "laser 7": "not ready", 
                             "laser 8": "not ready", 
                             "laser 9": "not ready", 
                             "laser 10": "not ready"}

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
        if self.pos.y < 20:
            self.direction.y = 1
            self.direction.x = 0
            
        else:
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
        self.fire_weapons(dt)

    def handle_shooting(self, dt):
        self.shoot_timer += dt
        if self.shoot_timer >= self.hold_fire:
            self.fire_mode = choice(["laola", "cylone", "rocket", "random", "all", "upgrade"])
            self.shooting_state = "shooting"
            print(self.fire_mode)

    def reset_shooting(self):
        self.shooting_state = "not shooting"
        self.shoot_timer = 0
        self.hold_fire = randint(1, 10)
        self.shot_counter = 0

    def fire_weapons(self, dt):
        if self.shooting_state == "shooting":
            self.projectile_interval_timer += dt
            if self.fire_mode == "laola":
                if self.projectile_interval_timer >= 0.5:
                    self.single_shot_timer += dt
                    if self.single_shot_timer < 0.1 and self.laser_states["laser 1"] == "ready":
                        self.fire_laser_1()
                        self.shot_counter += 1
                        self.laser_states["laser 2"] = "ready"
                        self.laser_states["laser 1"] = "not ready"
                    elif 0.1 < self.single_shot_timer < 0.2 and self.laser_states["laser 2"] == "ready":
                        self.fire_laser_2()
                        self.laser_states["laser 3"] = "ready"
                        self.laser_states["laser 2"] = "not ready"
                    elif 0.2 < self.single_shot_timer < 0.3 and self.laser_states["laser 3"] == "ready":
                        self.fire_laser_3()
                        self.laser_states["laser 4"] = "ready"
                        self.laser_states["laser 3"] = "not ready"
                    elif 0.3 < self.single_shot_timer < 0.4 and self.laser_states["laser 4"] == "ready":
                        self.fire_laser_4()
                        self.laser_states["laser 5"] = "ready"
                        self.laser_states["laser 4"] = "not ready"
                    elif 0.4 < self.single_shot_timer < 0.5 and self.laser_states["laser 5"] == "ready":
                        self.fire_laser_5()
                        self.laser_states["laser 6"] = "ready"
                        self.laser_states["laser 5"] = "not ready"
                    elif 0.5 < self.single_shot_timer < 0.6 and self.laser_states["laser 6"] == "ready":
                        self.fire_laser_6()
                        self.laser_states["laser 7"] = "ready"
                        self.laser_states["laser 6"] = "not ready"
                    elif 0.6 < self.single_shot_timer < 0.7 and self.laser_states["laser 7"] == "ready":
                        self.fire_laser_7()
                        self.laser_states["laser 8"] = "ready"
                        self.laser_states["laser 7"] = "not ready"
                    elif 0.7 < self.single_shot_timer < 0.8 and self.laser_states["laser 8"] == "ready":
                        self.fire_laser_8()
                        self.laser_states["laser 9"] = "ready"
                        self.laser_states["laser 8"] = "not ready"
                    elif 0.8 < self.single_shot_timer < 0.9 and self.laser_states["laser 9"] == "ready":
                        self.fire_laser_9()
                        self.laser_states["laser 10"] = "ready"
                        self.laser_states["laser 9"] = "not ready"
                    elif 0.9 < self.single_shot_timer < 1 and self.laser_states["laser 10"] == "ready":
                        self.fire_laser_10()
                        self.laser_states["laser 9"] = "ready"
                        self.laser_states["laser 10"] = "not ready"
                    elif 1 < self.single_shot_timer < 1.1 and self.laser_states["laser 9"] == "ready":
                        self.fire_laser_9()
                        self.laser_states["laser 8"] = "ready"
                        self.laser_states["laser 9"] = "not ready"
                    elif 1.1 < self.single_shot_timer < 1.2 and self.laser_states["laser 8"] == "ready":
                        self.fire_laser_8()
                        self.laser_states["laser 7"] = "ready"
                        self.laser_states["laser 8"] = "not ready"
                    elif 1.2 < self.single_shot_timer < 1.3 and self.laser_states["laser 7"] == "ready":
                        self.fire_laser_7()
                        self.laser_states["laser 6"] = "ready"
                        self.laser_states["laser 7"] = "not ready"
                    elif 1.3 < self.single_shot_timer < 1.4 and self.laser_states["laser 6"] == "ready":
                        self.fire_laser_6()
                        self.laser_states["laser 5"] = "ready"
                        self.laser_states["laser 6"] = "not ready"
                    elif 1.4 < self.single_shot_timer < 1.5 and self.laser_states["laser 5"] == "ready":
                        self.fire_laser_5()
                        self.laser_states["laser 4"] = "ready"
                        self.laser_states["laser 5"] = "not ready"
                    elif 1.5 < self.single_shot_timer < 1.6 and self.laser_states["laser 4"] == "ready":
                        self.fire_laser_4()
                        self.laser_states["laser 3"] = "ready"
                        self.laser_states["laser 4"] = "not ready"
                    elif 1.6 < self.single_shot_timer < 1.7 and self.laser_states["laser 3"] == "ready":
                        self.fire_laser_3()
                        self.laser_states["laser 2"] = "ready"
                        self.laser_states["laser 3"] = "not ready"
                    elif 1.7 < self.single_shot_timer < 1.8 and self.laser_states["laser 2"] == "ready":
                        self.fire_laser_2()
                        self.laser_states["laser 1"] = "ready"
                        self.laser_states["laser 2"] = "not ready"
                        self.single_shot_timer = 0
                        
                if self.shot_counter > 5:
                    self.reset_shooting()
                    
            elif self.fire_mode == "cylone":
                self.fire_laser_2()
                self.fire_laser_9()
                self.shot_counter += 1
                if self.shot_counter > 5:
                    self.reset_shooting()

            elif self.fire_mode == "rocket":
                if self.projectile_interval_timer >= 1:
                    self.fire_rocket()
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                if self.shot_counter > 10:
                    self.reset_shooting()

            elif self.fire_mode == "random":
                if self.projectile_interval_timer >= 0.5:
                    laser_number = randint(1, 10)
                    if laser_number == 1: self.fire_laser_1()
                    elif laser_number == 2: self.fire_laser_2()
                    elif laser_number == 3: self.fire_laser_3()
                    elif laser_number == 4: self.fire_laser_4()
                    elif laser_number == 5: self.fire_laser_5()
                    elif laser_number == 6: self.fire_laser_6()
                    elif laser_number == 7: self.fire_laser_7()
                    elif laser_number == 8: self.fire_laser_8()
                    elif laser_number == 9: self.fire_laser_9()
                    elif laser_number == 10: self.fire_laser_10()
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                    if self.shot_counter > 10:
                        self.reset_shooting()

            elif self.fire_mode == "all":
                if self.projectile_interval_timer >= 1:
                    self.fire_laser_1()
                    self.fire_laser_2()
                    self.fire_laser_3()
                    self.fire_laser_4()
                    self.fire_laser_5()
                    self.fire_laser_6()
                    self.fire_laser_7()
                    self.fire_laser_8()
                    self.fire_laser_9()
                    self.fire_laser_10()
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                    if self.shot_counter > 10:
                        self.reset_shooting()

            elif self.fire_mode == "upgrade":
                Upgrade(self.game, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() // 2))
                self.reset_shooting()


    def fire_laser_1(self):
        EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 232, self.pos.y + self.image.get_height() - 166), "red")
    
    def fire_laser_2(self):
        EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 248, self.pos.y + self.image.get_height() - 152), "red")

    def fire_laser_3(self):
        EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 264, self.pos.y + self.image.get_height() - 142), "red")

    def fire_laser_4(self):
        EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 279, self.pos.y + self.image.get_height() - 125), "red")
    
    def fire_laser_5(self):
        EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 295, self.pos.y + self.image.get_height() - 110), "red")
    
    def fire_laser_6(self):
        EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 456, self.pos.y + self.image.get_height() - 110), "red")

    def fire_laser_7(self):
        EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 472, self.pos.y + self.image.get_height() - 125), "red")

    def fire_laser_8(self):
        EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 487, self.pos.y + self.image.get_height() - 142), "red")

    def fire_laser_9(self):
        EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 502, self.pos.y + self.image.get_height() - 152), "red")

    def fire_laser_10(self):
        EnemyProjectile(self.game, "laser", self.laser_damage, (self.pos.x + 518, self.pos.y + self.image.get_height() - 166), "red")

    def fire_rocket(self):
        EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + self.image.get_width() // 2 + 10, self.pos.y + self.image.get_height() + 10), "green")