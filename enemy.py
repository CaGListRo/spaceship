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
        self.fire_mode = None
        self.shoot_timer = 0
        self.hold_fire = randint(1, 10)
        self.shooting_state = "not shooting"
        self.projectile_interval_timer = 0
        self.shot_counter = 0

        self.active_laser = 0
        self.laser_shifter = 1
        self.second_active_laser = 11

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
            self.fire_mode = "rocket"#choice(["all", "cylone", "knight_rider", "laola", "random", "rocket", "upgrade"])
            self.shooting_state = "shooting"

    def reset_shooting(self):
        self.shooting_state = "not shooting"
        self.shoot_timer = 0
        self.hold_fire = randint(1, 10)
        self.shot_counter = 0

    def fire_weapons(self, dt):
        if self.shooting_state == "shooting":
            self.projectile_interval_timer += dt

            if self.fire_mode == "all":
                if self.projectile_interval_timer >= 1:
                    for i in range(10):
                        getattr(self, f"fire_laser_{str(i + 1)}")()
                    self.fire_rocket()
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
                    getattr(self, f"fire_laser_{self.active_laser}")()
                    getattr(self, f"fire_laser_{self.second_active_laser}")()
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1
                    print(f"active: {self.active_laser}")
                    print(f"second: {self.second_active_laser}")
                        
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
                    getattr(self, f"fire_laser_{self.active_laser}")()
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
                    getattr(self, f"fire_laser_{self.active_laser}")()
                    self.projectile_interval_timer = 0
                    self.shot_counter += 1
                        
                if self.shot_counter >= 100:
                    self.reset_shooting()
                    self.active_laser = 0

            elif self.fire_mode == "random":
                if self.projectile_interval_timer >= 0.5:
                    laser_number = randint(1, 10)
                    getattr(self, f"fire_laser_{str(laser_number)}")()
                    self.shot_counter += 1
                    self.projectile_interval_timer = 0
                    if self.shot_counter > 10:
                        self.reset_shooting()

            elif self.fire_mode == "rocket":
                if self.projectile_interval_timer >= 1:
                    self.fire_rocket()
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
        EnemyProjectile(self.game, "rocket1", self.rocket_damage, (self.pos.x + self.image.get_width() // 2, self.pos.y + self.image.get_height() - 20), "green")