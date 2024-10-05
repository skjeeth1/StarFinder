import pygame

from setup import WINDOW_HEIGHT, FONT, WINDOW_LENGTH, TITLE_FONT
from planet_finder import PlanetFinder
from stage import Intro
from starfinder import StarFinderLevel
from miscellaneous import Timer


class StageManager:
    def __init__(self) -> None:
        self.stages = {
            'intro': Intro(self.change_stage),
            'finder': StarFinderLevel(self.change_stage),
            'planetfinder': PlanetFinder(self.change_stage)
        }

        self.cur_stage = 'intro'
        self.menu = Menu(self.change_stage, self.check_menu_active)
        self.menu_active = False

        self.timer = Timer(300)

        self.clock = pygame.time.Clock()

    def check_menu_active(self, state, *args):
        self.menu_active = state
        self.timer.activate(self.change_stage, *args)

    def change_stage(self, next_state):
        self.cur_stage = next_state
        self.stages[self.cur_stage].refresh()

    def play(self, dt):
        self.timer.update()
        if not self.menu_active:
            self.stages[self.cur_stage].play(dt)
        if self.cur_stage != "intro":
            self.menu.render()


class Menu:
    def __init__(self, change_state, menu_activate):
        self.change_state = change_state
        self.menu_activate = menu_activate
        self.right_side = 285

        self.icon = pygame.Surface((24, 24))
        self.icon.fill("white")
        self.icon_rect = self.icon.get_rect(topleft=(20, 20))
        self.display = pygame.display.get_surface()

        self.surf = pygame.Surface((self.right_side, WINDOW_HEIGHT))
        self.surf.fill("#000016")
        self.rect = self.surf.get_rect(topleft=(0, 0))

        self.back_icon = pygame.Surface((24, 24))
        self.back_icon.fill("white")
        self.back_icon_rect = self.icon.get_rect(bottomright=(self.right_side - 20, WINDOW_HEIGHT - 20))

        self.surf.blit(self.back_icon, self.back_icon_rect)

        self.surf.blit(pygame.font.Font(TITLE_FONT, 55).render("MENU", False, "white"), (30, 60))

        self.cur_view = "icon"
        self.font = pygame.font.Font(FONT, 20)

        self.menu_data = {
            "Night Sky Viewer": "finder",
            "Exoplanet Finder": "planetfinder",
            "Exoplanet Almanac": "blah",
            "Play a Mini Game": "blah",
        }

        self.rendered_text = []
        self.render_text()

    def check_collision(self):
        if self.cur_view == "icon":
            if self.icon_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.cur_view = "menu"
                self.menu_activate(True)

        elif self.cur_view == "menu":
            pos = pygame.mouse.get_pos()
            for ind, (surf, rect) in enumerate(self.rendered_text):
                if rect.collidepoint(pos):
                    pygame.draw.line(self.display, "white", rect.bottomleft, rect.bottomright)

                    if pygame.mouse.get_pressed()[0]:
                        self.cur_view = "icon"
                        self.menu_activate(False, list(self.menu_data.values())[ind])

            if self.back_icon_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    self.cur_view = "icon"
                    self.menu_activate(False)

    def render_text(self):
        for ind, i in enumerate(self.menu_data):
            surf = self.font.render(i, False, "white")
            rect = surf.get_rect(topleft=(35, 50 * ind + 200))

            self.surf.blit(surf, rect)
            self.rendered_text.append((surf, rect))

    def render(self):
        if self.cur_view == "icon":
            self.display.blit(self.icon, self.icon_rect)
        else:
            self.display.blit(self.surf, self.rect)
            pygame.draw.line(self.display, "white", (self.right_side, 0),
                             (self.right_side, WINDOW_HEIGHT), 3)
        self.check_collision()
