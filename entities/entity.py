import pygame
from util.settings import *
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, game, group, obstacle_sprites, layer):
        super().__init__(group)
        self.game = game
        self.obstacle_sprites = obstacle_sprites
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        self.vulnerable = True
        self._layer = layer
        self.state = "idle"
        self.direction_status = "right"
        self.vel = vec()
        self.acc = vec()
        self.force = 2000
        self.frict = -15

    def import_images(self, path:str):
        self.animations = self.game.get_animations(path)

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
    
    def animate(self):
        animation = self.animations[f"{self.state}_{self.direction_status}"]

        # Loop over frame index
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # Flicker
        if not self.vulnerable and self.hurt_time:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def set_state(self, new_state:str):
        self.state = new_state

    def set_direction(self, new_direction:str):
        self.direction_status = new_direction

    def get_status(self):
        pass

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # self.hitbox.x += self.direction.x * speed
        # self.collision("horizontal")

        # self.hitbox.y += self.direction.y * speed
        # self.collision("vertical")

        # self.rect.center = self.hitbox.center

    def physics(self, dt, frict, speed):
        # x-direction
        self.acc.x += self.vel.x * frict
        self.vel.x += self.acc.x * dt
        self.hitbox.centerx += self.vel.x * dt + (self.vel.x / 2)*dt
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # y-direction
        self.acc.y += self.vel.y * frict
        self.vel.y += self.acc.y * dt
        self.hitbox.centery += self.vel.y * dt + (self.vel.y / 2)*dt
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

        if self.vel.magnitude() >= speed:
            self.vel = self.vel.normalize() * speed

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