import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from camera import *

class State():

    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def enter_state(self):
        if len(self.game.states) > 1:
            self.prev_state = self.game.states[-1]
        self.game.states.append(self)

    def exit_state(self):
        self.game.states.pop()

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

class SplashScreen(State):
    def __init__(self, game):
        super().__init__(game)

    def draw(self, screen):
        screen.fill(COLORS["blue"])

class MainMenu(SplashScreen):
    def __init__(self, game):
        super().__init__(game)

    def update(self, dt):
        if INPUTS["space"]:
            Scene(self.game).enter_state()
            self.game.reset_inputs()

    def draw(self, screen):
        screen.fill(COLORS["blue"])
        self.game.render_text("Menu", COLORS["white"], self.game.font, (640, 340))

    
class Scene(State):
    def __init__(self, game):
        super().__init__(game)

        # self.camera = Camera(self)

        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

    def draw(self, screen):
        screen.fill(COLORS["red"])
        # self.game.render_text("Scene", COLORS["white"], self.game.font, (640, 340))

    def update(self, dt):
        if INPUTS["space"]:
            MainMenu(self.game).enter_state()
            self.game.reset_inputs()
