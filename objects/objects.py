import pygame
from util.settings import *

class Collider(pygame.sprite.Sprite):
    def __init__(self, groups, pos, size, number):
        super().__init__(groups)
        self.pos = pos
        self.size = size
        self.number = number
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft = self.pos)

class Object(pygame.sprite.Sprite):
    def __init__(self, groups, pos, layer = "blocks", surf = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)

        self.pos = pos
        self._layer = layer
        self.image = surf
        self.rect = self.image.get_rect(topleft = self.pos)
        self.hitbox = self.rect.copy().inflate(0, 0)

class Wall(Object):
    def __init__(self, groups, pos, layer="blocks", surf=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups, pos, layer, surf)

        self.hitbox = self.rect.copy().inflate(0, self.rect.height/2)
