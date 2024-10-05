import pygame

from setup import *
from stage import Stage


class StarFinderLevel(Stage):
    def __init__(self, change_state) -> None:
        super().__init__(change_state)

        self.background = pygame.image.load("assets/images/night_sky.jpg")
        self.back_rect = self.background.get_rect(top=0, left=0)

        self.active_area = pygame.Surface((WINDOW_LENGTH - 100, WINDOW_HEIGHT - 100))
        self.active_rect = self.active_area.get_rect(center=self.back_rect.center)

        self.entities = pygame.sprite.Group()

    def draw_lines(self, pos):
        pygame.draw.line(self.display, 'white', (pos[0], 0), (pos[0], WINDOW_HEIGHT))
        pygame.draw.line(self.display, 'white', (0, pos[1]), (WINDOW_LENGTH, pos[1]))

    def check_active(self, rect):
        mouse_pos = (pygame.mouse.get_pos())

        if rect.collidepoint(mouse_pos):
            self.draw_lines(mouse_pos)

    def play(self):
        self.display.blit(self.background, self.back_rect)
        self.check_active(self.active_rect)
