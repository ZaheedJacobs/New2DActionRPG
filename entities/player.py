import pygame
from util.settings import *
from util.camera import Camera
from entities.entity import Entity
from entities.entity_state import PlayerState

class Player(Entity):
    def __init__(self, game, group, name, scene, pos, obstacle_sprites, layer):
        super().__init__(game, group, obstacle_sprites, layer)
        self.name = name
        self.scene = scene
        self.pos = pos
        self.state = PlayerState()

        self.speed = 5
        self.import_images(f"assets/characters/{self.name}/")
        self.image = self.animations[f"idle_{self.state.direction_status}"][self.frame_index]
        self.rect = self.image.get_rect(topleft = self.pos)
        self.hitbox = self.rect.inflate(-6, -20)

        self.attacking = False

    def input(self):

        # Movement inputs
        if not self.attacking:
            if INPUTS["up"]:
                self.direction.y = -1
                self.state.set_state("run")
                self.state.direction_status = "up"
            
            elif INPUTS["down"]:
                self.direction.y = 1
                self.state.set_state("run")
                self.state.direction_status = "down"
            else:
                self.direction.y = 0
            
            if INPUTS["right"]:
                self.direction.x = 1
                self.state.set_state("run")
                self.state.direction_status = "right"
            
            elif INPUTS["left"]:
                self.direction.x = -1
                self.state.set_state("run")
                self.state.direction_status = "left"
            else:
                self.direction.x = 0

    def update(self, dt):
        self.input()
        self.state.animate(self)  