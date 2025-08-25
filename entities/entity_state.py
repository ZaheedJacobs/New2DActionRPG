import pygame
from util.settings import *

class EntityState:
    def __init__(self):
        self.state = "idle"
        self.states = {
            "idle": True,
            "attack": False,
            "run": False,
            "hit": False
        }

    def check_state(self):
        for state, is_in in self.states.items():
            if is_in:
                return state
            
    def state_actions(self):
        self.state = self.check_state()
        match self.state:
            case "idle":
                self.idle_actions()
            case "attack":
                self.attack_actions()
            case "run":
                self.run_actions()
            case "hit":
                self.hit_actions()

    def idle_actions(self):
        pass

    def attack_actions(self):
        pass

    def hit_actions(self):
        pass

    def run_actions(self):
        pass

    def set_state(self, new_state:str):
        for state in self.states.keys():
            if state != new_state:
                self.states[state] = False
        self.states[new_state] = True


class PlayerState(EntityState):
    def __init__(self):
        super().__init__()
        # I will add more states and actions for the player