import pygame,sys
from settings import *
from state import *

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
        self.font = pygame.font.Font(FONT, 50)

    def render_text(self, text, color, font, pos, centralised = True):
        surf = font.render(str(text), False, color)
        rect = surf.get_rect(center = pos) if centralised else surf.get_rect(topleft = pos)
        self.screen.blit(surf, rect)

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
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    INPUTS["escape"] = False
                if event.key == pygame.K_SPACE:
                    INPUTS["space"] = False
    
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