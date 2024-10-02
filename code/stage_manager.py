import pygame
from setup import *
from button import Button
from stage import Intro
from starfinder import StarFinderLevel

class StageManager:
    def __init__(self) -> None:
        self.font = "assets/fonts/sterion-font/Sterion-BLLld.ttf"
        self.stages = {
            'intro': Intro(self.change_stage, self.font),
            'finder': StarFinderLevel(self.change_stage)
        }

        self.cur_stage = 'intro'
    
    def change_stage(self, next_state):
        self.cur_stage = next_state

    def play(self):
        self.stages[self.cur_stage].play()


