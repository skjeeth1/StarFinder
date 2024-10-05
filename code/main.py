from sys import exit

import pygame

from setup import *
from stage_manager import StageManager


class MainGame:
    def __init__(self) -> None:
        pygame.init()

        self.display = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))

        self.stage_manager = StageManager()
        pygame.display.set_caption("Web the Universe")

        self.font = pygame.font.SysFont('calibri', 30)
        self.clock = pygame.time.Clock()

    def run(self):

        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # self.display.fill("#1E1E1E")

            self.stage_manager.play(dt)
            surf = self.font.render(str(pygame.mouse.get_pos()), False, '#FFFFFF', "#000000")
            rect = surf.get_rect(topleft=(20, 20))

            # self.display.blit(surf, rect)
            pygame.display.flip()


if __name__ == "__main__":
    game = MainGame()
    game.run()
