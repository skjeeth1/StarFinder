from sys import exit

import pygame

from setup import *
from stage_manager import StageManager
from main_mini import Game


class MainGame:
    def __init__(self) -> None:
        pygame.init()

        self.display = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))

        self.stage_manager = StageManager(self.invoke_mini_game)
        pygame.display.set_caption("Web the Universe")

        self.font = pygame.font.SysFont('calibri', 30)
        self.clock = pygame.time.Clock()

        self.game = None
        self.run_game = False

        self.clue = 0
        self.total_clues = 3

        # self.invoke_mini_game()

    def invoke_mini_game(self):
        self.game = Game(self.quit_mini_game, self.clue)
        self.run_game = True

    def quit_mini_game(self, status):
        self.game = None
        self.run_game = False
        if status:
            self.clue += 1
        self.stage_manager.get_mini_game_status(status, self.clue)

    def run(self):

        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # self.display.fill("#1E1E1E")

            if self.run_game:
                self.game.run(self.display)
            else:
                self.stage_manager.play(dt)

            surf = self.font.render(str(pygame.mouse.get_pos()), False, '#FFFFFF', "#000000")
            rect = surf.get_rect(topleft=(20, 20))

            self.display.blit(surf, rect)

            pygame.display.flip()


if __name__ == "__main__":
    game = MainGame()
    game.run()
