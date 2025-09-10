import pygame
from util.settings import *
from util.camera import Camera
from entities.entity import Entity

class Player(Entity):
    def __init__(self, game, group, name, scene, pos, obstacle_sprites, layer):
        super().__init__(game, group, obstacle_sprites, layer)
        self.name = name
        self.scene = scene

        self.speed = 2
        self.base_speed = self.speed
        self.import_images(f"assets/characters/{self.name}/")
        self.image = self.animations[f"idle_{self.direction_status}"][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width/2, -self.rect.height/2)

        self.attacking = False
        self.attack_cooldown = 400
        self.invincibility_duration = 500
        self.hurt_time = None

        self.dashing = False
        self.dash_duration = 500
        self.dash_time = None
        self.pending = False
        self.dash_vec = None
        self.mouse_vec = vec()

    def input(self):

        if self.alive():
            self.movement_input()
            self.attack_input()
        
    def movement_input(self):
        # Movement inputs
        if not self.attacking:
            if INPUTS["up"]:
                self.direction.y = -1
                self.set_direction("up")
                self.acc.y = -self.force
                
            elif INPUTS["down"]:
                self.direction.y = 1
                self.set_direction("down")
                self.acc.y = self.force
            else:
                self.direction.y = 0
                self.acc.y = 0
            
            if INPUTS["right"]:
                self.direction.x = 1
                self.set_direction("right")
                self.acc.x = self.force
            
            elif INPUTS["left"]:
                self.direction.x = -1
                self.set_direction("left")
                self.acc.x = -self.force
            else:
                self.direction.x = 0
                self.acc.x = 0
            
            # Dash functionality
            if INPUTS["right_click"]:
                self.dash()

    def attack_input(self):
        # Attack input
        if INPUTS["left_click"] and not self.attacking and not self.dashing:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            # self.create_attack()

    def handle_cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.dashing:
            if current_time - self.dash_time >= self.dash_duration:
                self.dashing = False
                self.dash_time = None
                # self.speed = self.base_speed
                self.frict = -15
                self.dash_vec = None
                self.mouse_vec = vec()
                self.vulnerable = True
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.attack_time = None
                # self.destroy_attack()
    
    def dash(self):
        self.dashing = True
        self.dash_time = pygame.time.get_ticks()
        self.frict = -2
        self.dash_vec = self.vec_to_mouse(200)
        self.vulnerable = False

    def vec_to_mouse(self, speed):
        self.mouse_vec = vec(pygame.mouse.get_pos()) - (vec(self.hitbox.center) - vec(self.scene.camera.offset))
        if self.mouse_vec.length() > 0 : self.mouse_vec.normalize_ip()
        self.evaluate_dash_direction(self.mouse_vec)
        return self.mouse_vec * speed
    
    def evaluate_dash_direction(self, dash_vec: vec):
        # Check absolute values to determine primary direction
        # if the x component is greater, dash horizontally; otherwise, dash vertically
        if abs(dash_vec.x) > abs(dash_vec.y):
            if dash_vec.x > 0:
                self.set_direction("right")
            else:
                self.set_direction("left")
        else:
            if dash_vec.y > 0:
                self.set_direction("down")
            else:
                self.set_direction("up")

    def get_status(self):
        if self.direction.magnitude() != 0:
            self.set_state("run")
            return
        if self.dashing:
            self.set_state("dashing")
            return
        if self.attacking:
            self.set_state("attack")
            return
        self.set_state("idle")

    def update(self, dt):
        if self.alive():
            self.input()
            self.move(self.speed)
            self.get_status()
            self.animate()
            self.handle_cooldowns()
            if self.dashing:
                self.acc = vec()
                self.vel = self.dash_vec
                self.physics(dt, self.frict, 30)
            else:
                self.physics(dt, self.frict, 60)