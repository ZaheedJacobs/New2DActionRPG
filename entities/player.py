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

    def input(self):

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

    def handle_cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.dashing:
            if current_time - self.dash_time >= self.dash_duration:
                self.dashing = False
                self.dash_time = None
                self.speed = self.base_speed
                self.frict = -15
                self.dash_vec = None
    
    def dash(self):
        self.dashing = True
        self.dash_time = pygame.time.get_ticks()
        self.frict = -2
        self.dash_vec = self.vec_to_mouse(200)

    def vec_to_mouse(self, speed):
        direction = vec(pygame.mouse.get_pos())
        if direction.length() > 0 : direction.normalize_ip()
        return direction * speed

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
        self.input()
        self.move(self.speed)
        self.get_status()
        self.animate()
        self.handle_cooldowns()
        self.physics(dt, self.frict, 60)
        if self.dashing:
            self.acc = vec()
            self.vec = self.dash_vec