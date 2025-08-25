from pygame.math import Vector2 as vec

WIDTH = 1280
HEIGHT = 720
TILESIZE = 16
FONT = "assets/fonts/LexendExa-Regular.ttf"
BUTTON_FONT = "assets/fonts/Almendra-Regular.ttf"
BUTTON_SIZE = 16

INPUTS = {
        'escape': False,
        'space': False,
        'up': False,
        'down': False,
        'left': False,
        'right': False,
        'left_click': False,
        'right_click': False,
        'scroll_up': False,
        'scroll_down': False,
        'q_press': False,
        'e_press': False,
        'r_press': False,
        'm_press': False,
        'c_press': False,
        'i_press': False
        }

COLORS = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "red": (255, 100, 100),
        "green": (0, 255, 0),
        "blue": (100, 100, 255),
        "orange": (230, 150, 0),
        "yellow": (255, 255, 0)
        }

LAYERS = ["background",
          "objects",
          "blocks",
          "characters",
          "particles",
          "foreground"]

SCENE_DATA = {
                0: {1: 1, 3: 2},
                1: {1: 0, 2: 2},
                2: {2: 1, 3: 0}
                }