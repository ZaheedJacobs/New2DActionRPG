import pygame
from util.settings import *
from entities.entity import Entity

class EntityState:
    def __init__(self):
        self.state = "idle"
        self.states = {
            "idle": True,
            "attack": False,
            "run": False,
            "hit": False
        }
        self.direction_status = "right"

    def check_state(self):
        for state, is_in in self.states.items():
            if is_in:
                return state
            
    # def state_actions(self, character:Entity):
    #     self.state = self.check_state()
    #     match self.state:
    #         case "idle":
    #             self.idle_actions()
    #         case "attack":
    #             self.attack_actions()
    #         case "run":
    #             self.run_actions()
    #         case "hit":
    #             self.hit_actions()

    # def idle_actions(self, character:Entity):
    #     character.frame_index = 0


    # def attack_actions(self, character:Entity):
    #     pass

    # def hit_actions(self, character:Entity):
    #     pass

    # def run_actions(self, character: Entity):
    #     pass

    def animate(self, character:Entity):
        animation = character.animations[f"{self.state}_{self.direction_status}"]

        # Loop over frame index
        character.frame_index += character.animation_speed

        if character.frame_index >= len(animation):
            character.frame_index = 0

        # Set the image
        character.image = animation[int(character.frame_index)]
        character.rect = character.image.get_rect(center = character.hitbox.center)

        # Flicker
        if not character.vulnerable:
            alpha = character.wave_value()
            character.image.set_alpha(alpha)
        else:
            character.image.set_alpha(255)

    def set_state(self, new_state:str):
        for state in self.states.keys():
            if state != new_state:
                self.states[state] = False
        self.states[new_state] = True


class PlayerState(EntityState):
    def __init__(self):
        super().__init__()
        # I will add more states and actions for the player