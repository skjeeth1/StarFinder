import pygame

from button import Button
from setup import *


class Stage:
    def __init__(self, change_state) -> None:
        self.change_state = change_state
        self.display = pygame.display.get_surface()

    def quit_state(self, next_state):
        self.change_state(next_state)

    def play(self):
        self.display.fill("#FFFFFF")


class Intro(Stage):
    def __init__(self, change_state, font) -> None:
        super().__init__(change_state)

        self.texts = {
            1: ("Welcome to", 32, pygame.Vector2((900, 270)), True),
            2: ("PlanetFinder", 64, pygame.Vector2((900, 350)), True),
        }

        self.fonts = {
            i[1]: pygame.font.Font(font, i[1]) for i in self.texts.values()
        }

        self.rendered_text = []

        self.background = pygame.image.load("assets/images/night_sky.jpg")
        self.back_rect = self.background.get_rect(top=0, left=0)

        self.tel_img = pygame.image.load("assets/images/telescope.png")
        self.tel_rect = self.tel_img.get_rect(midleft=(100, WINDOW_HEIGHT // 2))

        self.play_button = Button(font, "PLAY", 25, (900, 450), "#EEEEEE", "#EEEEEE", self.quit_state, 'finder')

        self.render_text()

    def render_text(self):
        for ind, item in self.texts.items():
            if item[3]:
                surf = self.fonts[item[1]].render(item[0], False, "#000000")
                rect = surf.get_rect(center=item[2] + (5, 5))
                self.rendered_text.append((surf, rect))

            surf = self.fonts[item[1]].render(item[0], False, "#EEEEEE")
            rect = surf.get_rect(center=item[2])

            self.rendered_text.append((surf, rect))

    def play(self):
        self.display.blit(self.background, self.back_rect)
        self.display.blit(self.tel_img, self.tel_rect)
        self.play_button.draw()
        for surf, rect in self.rendered_text:
            self.display.blit(surf, rect)
