import pygame
from util.settings import *
from pytmx.util_pygame import load_pygame
from util.camera import *
from objects.objects import Collider, Wall
from objects.tile import Tile
from entities.player import Player

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
        self.game.render_text("Menu", COLORS["white"], self.game.font, (WIDTH/2, HEIGHT/2))

    
class Scene(State):
    def __init__(self, game):
        super().__init__(game)

        self.camera = Camera(self)

        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.tmx_data = load_pygame(f"scenes/0/0.tmx")

        self.create_scene()

    def create_scene(self):
        layers = []

        for l in self.tmx_data.layers:
            layers.append(l.name)

            if "blocks" in layers:
                for x, y, surf in self.tmx_data.get_layer_by_name("blocks").tiles():
                    Wall([self.block_sprites, self.drawn_sprites], (x * TILESIZE, y * TILESIZE), "blocks", surf)
            
            if "tiles" in layers:
                for x, y, surf in self.tmx_data.get_layer_by_name("tiles").tiles():
                    Tile([self.block_sprites, self.drawn_sprites], (x * TILESIZE, y * TILESIZE), "background", surf)

            if "entries" in layers:
                for obj in self.tmx_data.get_layer_by_name("entries"):
                    if obj.name == "0":
                        self.pos = (obj.x, obj.y)

                        self.player = Player(self.game,
                                            [self.update_sprites,
                                            self.player_sprites,
                                            self.drawn_sprites
                                            ],
                                            "player", 
                                            self,
                                            self.pos,
                                            self.obstacle_sprites,
                                            "blocks"
                                            )
                        self.target = self.player

                        self.camera.offset = vec(self.player.rect.centerx - WIDTH/2, self.player.rect.centery - HEIGHT/2)

    def draw(self, screen):
        screen.fill(COLORS["red"])
        self.camera.draw(screen, self.drawn_sprites)
        self.debugger([f"Player state: {self.player.state}", f"Player direction axis: {self.player.direction}", f"Player direction: {self.player.direction_status}"])
    
    def debugger(self, debug_list):
        for index, name in enumerate(debug_list):
            self.game.render_text(name, COLORS["white"], self.game.font, (10, 15 * index), False)

    def update(self, dt):
        self.update_sprites.update(dt)
        self.camera.update(dt, self.target)
        if INPUTS["space"]:
            MainMenu(self.game).enter_state()
            self.game.reset_inputs()
