import pygame,sys
from util.settings import *
from state import *
import os

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen= pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
        self.running = True
        self.FPS = 60
        self.states = []
        self.splashScreen = MainMenu(self)
        self.states.append(self.splashScreen)
        self.font = pygame.font.Font(FONT, 15)

    def render_text(self, text, color, font, pos, centralised = True):
        surf = font.render(str(text), False, color)
        rect = surf.get_rect(center = pos) if centralised else surf.get_rect(topleft = pos)
        self.screen.blit(surf, rect)

    def get_animations(self, path:str):
        animations = {}
        for filename in os.listdir(path):
            animations.update({filename:[]})
        return animations
    
    def get_images(self, path:str):
        images = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            image = pygame.image.load(full_path).convert_alpha()
            images.append(image)
        return images

    def get_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    INPUTS["escape"] = True
                if event.key == pygame.K_SPACE:
                    INPUTS["space"] = True
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    INPUTS["right"] = True
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    INPUTS["left"] = True
                if event.key in (pygame.K_UP, pygame.K_w):
                    INPUTS["up"] = True
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    INPUTS["down"] = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    INPUTS["left_click"] = True
                if event.button == 3:
                    INPUTS["right_click"] = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    INPUTS["left_click"] = False
                if event.button == 3:
                    INPUTS["right_click"] = False
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    INPUTS["escape"] = False
                if event.key == pygame.K_SPACE:
                    INPUTS["space"] = False
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    INPUTS["right"] = False
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    INPUTS["left"] = False
                if event.key in (pygame.K_UP, pygame.K_w):
                    INPUTS["up"] = False
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    INPUTS["down"] = False
    
    def reset_inputs(self):
        for key in INPUTS:
            INPUTS[key] = False

    def loop(self):
        while self.running:
            dt = self.clock.tick(self.FPS)/1000
            self.get_inputs()
            self.states[-1].update(dt)
            self.states[-1].draw(self.screen)
            pygame.display.update()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.loop()