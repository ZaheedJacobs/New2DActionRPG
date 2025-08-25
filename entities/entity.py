import pygame
from util.settings import *
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, game, name, groups):
        super.__init__(groups)
        self.name = name
        self.game = game
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def import_images(self, path:str):
        self.animations = self.game.get_animations()

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = self.game.get_images(full_path)

    def collision(self, direction: str):
        match direction:
            case "horizontal":
                self.horizontal_collision()
            case "vertical":
                self.vertical_collision()

    def horizontal_collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.x > 0: # Moving right
                    self.hitbox.right = sprite.hitbox.left
                elif self.direction.x < 0: # Moving left
                    self.hitbox.left = sprite.hitbox.right

    def vertical_collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0: # Moving down
                    self.hitbox.bottom = sprite.hitbox.top
                elif self.direction.y < 0: # Moving up
                    self.hitbox.top = sprite.hitbox.bottom
    
    def move(self, speed):
        if self.direction.magnitude != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")

        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")

        self.rect.center = self.hitbox.center

    def wave_value(self):
        """Handles flashing effect when player or enemy gets hit"""
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
        
    def update(self, dt):
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def __init__(self, *components, x=0, y=0):
    #     self.components = []
    #     self.x = x
    #     self.y = y

    #     for component in components:
    #         self.add(component, False)
    #     for component in components:
    #         setup = getattr(component, "setup", None)
    #         if callable(setup):
    #             component.setup()

    # def add(self, component, perform_setup=True):
    #     component.entity = self
    #     self.components.append(component)
    #     if perform_setup:
    #         setup = getattr(component, "setup", None)
    #         if callable(setup):
    #             component.setup()

    # def delete_self(self):
    #     pass
    #     # from core.area import area
    #     # if self in area.entities:
    #     #   area.entities.remove(self)
    #     # for component in self.components:
    #     #   breakdown = getattr(component, "breakdown", None)
    #     #   if callable(breakdown):
    #     #       component.breakdown()
    #     # self.components.clear()

    # def remove(self, kind):
    #     component = self.get(kind)
    #     self.remove_component(component)

    # def remove_component(self, component):
    #     if component is not None:
    #         breakdown = getattr(component, "breakdown", None)
    #         if callable(breakdown):
    #             component.breakdown()
    #         component.entity = None
    #         self.components.remove(component)

    # def has(self, kind):
    #     for component in self.components:
    #         if isinstance(component, kind):
    #             return True
    #     return None
    
    # def get(self, kind):
    #     for component in self.components:
    #         if isinstance(component, kind):
    #             return component
    #     return None