import pygame

from stage import Stage
from setup import WINDOW_HEIGHT, WINDOW_LENGTH, FONT, TITLE_FONT


class PlanetFinder(Stage):
    def __init__(self, change_state):
        super().__init__(change_state)
        self.tiles = [
            [i, WINDOW_HEIGHT // 2 + 50, False] for i in
            range(WINDOW_LENGTH // 5 - 60, WINDOW_LENGTH, WINDOW_LENGTH // 5 + 40)
        ]

        self.tiles[0][2] = False
        self.tiles[1][2] = False

        self.background = pygame.image.load("assets/images/night_sky.jpg")
        surf = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        surf.fill((50, 50, 50, 0))
        self.background.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.back_rect = self.background.get_rect(top=0, left=0)

        self.create_rectangles()

        self.title = pygame.font.Font(TITLE_FONT, 50).render("WAYS TO FIND AN EXOPLANET", False, "white")

        self.cur_view = 'viewer'
        self.font_1 = pygame.font.Font(FONT, 45)
        self.font_2 = pygame.font.Font(FONT, 20)

        self.helper_text = self.font_2.render("Unlock Methods by playing Mini Games", False, 'white')

        self.locked_surf = self.tiles[0][0].copy()
        surf_1 = self.font_2.render("Unlock this", False, "#EEEEEE")
        surf_2 = self.font_1.render("Method", False, "#EEEEEE")
        rect_1 = surf_1.get_rect(
            center=(self.locked_surf.get_width() // 2, self.locked_surf.get_height() // 2 - 25))
        rect_2 = surf_2.get_rect(
            center=(self.locked_surf.get_width() // 2, self.locked_surf.get_height() // 2 + 25))

        self.locked_surf.blit(surf_1, rect_1)
        self.locked_surf.blit(surf_2, rect_2)

        self.data = [
            ["Reading the Wobble",
             "This method involves making precise measurements of a star's position to detect the tiny wobble caused by an orbiting planet."],
            ["Dips in Light",
             "When a planet passes in front of its star, it blocks some of the star's light, which creates a small decrease in the observed light. The depth of the decrease is proportional to the planet's cross-section"],
            ["Reading the Light",
             "It's a technique known as 'transit spectroscopy,' when light from a star travels through the atmosphere of an orbiting planet and reaches our telescopes – in space or on the ground – and tells about where it's been."],
            ["Direct Imaging",
             "This method captures pictures of exoplanets orbiting distant stars. It's very difficult to do, but it provides scientists with a lot of data about the planet, including its orbit and atmosphere."]
        ]

        self.render_text()

    def create_rectangles(self):
        for ind, cord in enumerate(self.tiles):
            surf = pygame.Surface((240, 400), pygame.SRCALPHA)
            rect = surf.get_rect(center=cord[:2])

            self.tiles[ind] = (surf, rect, cord[2])

    def on_hover(self):
        if self.cur_view == 'viewer':
            pos = pygame.mouse.get_pos()
            for ind, (surf, rect, lock) in enumerate(self.tiles):
                if not lock:
                    if rect.collidepoint(pos):
                        rect_2 = pygame.Rect(rect.left + 5, rect.top + 5, rect.width, rect.height)
                        pygame.draw.rect(self.display, "#99ccff", rect_2, 7)

                        if pygame.mouse.get_pressed()[0]:
                            self.cur_view = ind

    def render_text(self):
        for ind, i in enumerate(self.data):
            for indj, j in enumerate(i):
                if indj == 0:
                    surf_1 = self.font_2.render(' '.join(self.data[ind][indj].split()[:-1]), False, "#EEEEEE")
                    surf_2 = self.font_1.render(self.data[ind][indj].split()[-1], False, "#EEEEEE")
                    rect_1 = surf_1.get_rect(
                        center=(self.tiles[ind][0].get_width() // 2, self.tiles[ind][0].get_height() // 2 - 25))
                    rect_2 = surf_2.get_rect(
                        center=(self.tiles[ind][0].get_width() // 2, self.tiles[ind][0].get_height() // 2 + 25))

                    self.tiles[ind][0].blit(surf_1, rect_1)
                    self.tiles[ind][0].blit(surf_2, rect_2)

    def refresh(self):
        self.cur_view = "viewer"

    def play(self, dt):
        self.display.blit(self.background, self.back_rect)

        self.on_hover()

        if self.cur_view == 'viewer':
            self.display.blit(self.title, (100, 70))
            self.display.blit(self.helper_text, (800, WINDOW_HEIGHT - 50))
            for surf, rect, lock in self.tiles:
                if lock:
                    self.display.blit(self.locked_surf, rect.topleft)
                    pygame.draw.rect(self.display, "#EEEEEE", rect, 7)
                else:
                    self.display.blit(surf, rect)
                    pygame.draw.rect(self.display, "#ccffff", rect, 7)
        else:
            pass
