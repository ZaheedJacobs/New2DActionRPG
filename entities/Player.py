import pygame
from util.settings import *
from util.camera import Camera
from entity import Entity
from entity_state import PlayerState

class Player(Entity):
    def __init__(self, game, name, scene, groups):
        super().__init__(game, name, scene, groups)

        self.state = PlayerState()

        self.speed = 5

        self.x = 0
        self.y = 0

        self.image = self.import_images(f"assets/characters/{self.name}/")

    def update(self, dt):
        pass    