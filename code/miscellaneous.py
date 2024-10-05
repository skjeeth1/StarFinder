import pygame
from math import sin

class Button:
    def __init__(self, font, text, font_size, pos, color, butt_color, click_func, *args) -> None:
        self.display = pygame.display.get_surface()

        self.font = pygame.font.Font(font, font_size)
        self.surf = self.font.render(text, False, color)
        self.rect = self.surf.get_rect(center=pos)
        self.but_rect = self.rect.inflate(40, 20)
        self.but_rect_2 = self.but_rect.copy()
        self.button_color = butt_color
        self.active = True

        self.click_func = click_func
        self.func_args = args

    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.active:
            if pygame.mouse.get_pressed()[0] and self.but_rect.collidepoint(mouse_pos):
                self.active = False
                self.click_func(*self.func_args)

    def draw(self):
        self.but_rect_2.topleft = self.but_rect.topleft + pygame.Vector2(0, sin(pygame.time.get_ticks() / 200)) * 5
        pygame.draw.rect(self.display, self.button_color, self.but_rect_2, border_radius=12, width=5)
        self.display.blit(self.surf, self.rect.topleft + pygame.Vector2(0, sin(pygame.time.get_ticks() / 200)) * 5)
        self.on_click()


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
