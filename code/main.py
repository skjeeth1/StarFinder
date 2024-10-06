from sys import exit

import pygame

from setup import *
from stage_manager import StageManager
from main_mini import Game


class MainGame:
    def __init__(self) -> None:
        pygame.init()

        self.display = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))

        self.stage_manager = StageManager(self.invoke_mini_game, self.game_over, self.game_win)
        pygame.display.set_caption("Mission StarFinder")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))

        self.font = pygame.font.SysFont('calibri', 30)
        self.clock = pygame.time.Clock()

        self.game = None
        self.run_game = False

        self.clue = 0
        self.total_clues = 2

        self.game_over_state = False
        self.game_over_surf = pygame.font.Font(FONT, 65).render("GAME OVER!", False, "white")
        self.game_over_rect = self.game_over_surf.get_rect(center=(WINDOW_LENGTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.game_over_surf_2 = pygame.font.Font(FONT, 50).render("THE ALIENS HAVE ESCAPED!", False, "white")
        self.game_over_rect_2 = self.game_over_surf_2.get_rect(center=(WINDOW_LENGTH // 2, WINDOW_HEIGHT // 2 + 40))

        self.game_win_state = False
        self.game_win_surf = pygame.font.Font(FONT, 65).render("GAME WON!", False, "white")
        self.game_win_rect = self.game_over_surf.get_rect(center=(WINDOW_LENGTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.game_win_surf_2 = pygame.font.Font(FONT, 50).render("YOU HAVE RETRIEVED THE AI!", False, "white")
        self.game_win_rect_2 = self.game_over_surf_2.get_rect(center=(WINDOW_LENGTH // 2, WINDOW_HEIGHT // 2 + 40))

        # self.invoke_mini_game()

    def invoke_mini_game(self):
        self.game = Game(self.quit_mini_game, self.clue)
        self.run_game = True

    def quit_mini_game(self, status):
        self.game = None
        self.run_game = False
        if status:
            self.clue += 1
        if self.clue >= self.total_clues:
            self.clue = self.total_clues

        self.stage_manager.get_mini_game_status(status, self.clue)

    def game_over(self):
        self.game_over_state = True

    def game_win(self):
        self.game_win_state = True

    def run(self):

        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # self.display.fill("#1E1E1E")

            if self.game_over_state:
                self.display.fill("#1E1E1E")
                self.display.blit(self.game_over_surf, self.game_over_rect)
                self.display.blit(self.game_over_surf_2, self.game_over_rect_2)
            elif self.game_win_state:
                self.display.fill("#1E1E1E")
                self.display.blit(self.game_win_surf, self.game_win_rect)
                self.display.blit(self.game_win_surf_2, self.game_win_rect_2)
            elif self.run_game:
                self.game.run(self.display)
            else:
                self.stage_manager.play(dt)

            # surf = self.font.render(str(pygame.mouse.get_pos()), False, '#FFFFFF', "#000000")
            # rect = surf.get_rect(topleft=(20, 20))
            #
            # self.display.blit(surf, rect)

            pygame.display.flip()


if __name__ == "__main__":
    game = MainGame()
    game.run()
