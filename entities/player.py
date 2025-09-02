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
        self.import_images(f"assets/characters/{self.name}/")
        self.image = self.animations[f"idle_{self.direction_status}"][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width/2, -self.rect.height/2)

        self.attacking = False

    def input(self):

        # Movement inputs
        if not self.attacking:
            if INPUTS["up"]:
                self.direction.y = -1
                self.set_direction("up")
                
            
            elif INPUTS["down"]:
                self.direction.y = 1
                self.set_direction("down")
            else:
                self.direction.y = 0
            
            if INPUTS["right"]:
                self.direction.x = 1
                self.set_direction("right")
            
            elif INPUTS["left"]:
                self.direction.x = -1
                self.set_direction("left")
            else:
                self.direction.x = 0

    def get_status(self):
        if self.direction.magnitude() != 0:
            self.set_state("run")
        else:
            self.set_state("idle")

    def update(self, dt):
        self.input()
        self.move(self.speed)
        self.get_status()
        self.animate()  