import pygame,sys
from settings import *
from state import *

class Game:

    def __init__(self):
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen= pygame.display.set_mode((WIDTH, HEIGHT))
        # self.font = pygame.font.Font()
        self.running = True
        self.FPS = 60
        self.states = []
        self.splashScreen = SplashScreen(self)
        self.states.append(self.splashScreen)

    def get_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

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