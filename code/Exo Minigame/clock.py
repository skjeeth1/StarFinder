import pygame

class Timer:
    def __init__(self, duration, func = None, *args):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.func = func
        self.args = args

    def activate(self, func=None, *args):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        if func:
            self.func = func
        if args:
            self.args = args

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.func:
            if self.args:
                self.func(self.args[0])
                self.args = None
            self.func = None


    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                self.deactivate()