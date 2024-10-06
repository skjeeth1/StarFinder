import pygame

from setup import WINDOW_HEIGHT, WINDOW_LENGTH, FONT, TITLE_FONT, FINDER_DATA
from stage import Stage


class Tiles:
    def __init__(self, size, pos, lock, name, font_1, font_2=None, lock_surf=None, data=None):
        self.display = pygame.display.get_surface()

        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=pos)
        self.lock = lock
        self.lock_surf = lock_surf
        self.name = name

        self.font_1 = font_1
        self.font_2 = font_2
        self.data = data

        self.render_text()

    def render_text(self):
        surf_1 = self.font_2.render(' '.join(self.name.split()[:-1]), False, "#EEEEEE")
        surf_2 = self.font_1.render(self.name.split()[-1], False, "#EEEEEE")
        rect_1 = surf_1.get_rect(
            center=(self.surf.get_width() // 2, self.surf.get_height() // 2 - 25))
        rect_2 = surf_2.get_rect(
            center=(self.surf.get_width() // 2, self.surf.get_height() // 2 + 25))

        self.surf.blit(surf_1, rect_1)
        self.surf.blit(surf_2, rect_2)

    def render_tile(self):
        if self.lock_surf and self.lock:
            self.display.blit(self.lock_surf, self.rect.topleft)
            pygame.draw.rect(self.display, "#EEEEEE", self.rect, 7)
        else:
            self.display.blit(self.surf, self.rect)
            pygame.draw.rect(self.display, "#ccffff", self.rect, 7)


class PlanetFinder(Stage):
    def __init__(self, change_state):
        super().__init__(change_state)

        self.background = pygame.image.load("assets/images/night_sky.jpg")
        surf = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        surf.fill((50, 50, 50, 0))
        self.background.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.back_rect = self.background.get_rect(top=0, left=0)

        self.title = pygame.font.Font(TITLE_FONT, 50).render("WAYS TO FIND AN EXOPLANET", False, "white")

        self.view = 'viewer'
        self.font_1 = pygame.font.Font(FONT, 45)
        self.font_2 = pygame.font.Font(FONT, 20)

        self.data = FINDER_DATA

        self.locked_surf = pygame.Surface((240, 400), pygame.SRCALPHA)
        surf_1 = self.font_2.render("Unlock this", False, "#EEEEEE")
        surf_2 = self.font_1.render("Method", False, "#EEEEEE")
        rect_1 = surf_1.get_rect(
            center=(self.locked_surf.get_width() // 2, self.locked_surf.get_height() // 2 - 25))
        rect_2 = surf_2.get_rect(
            center=(self.locked_surf.get_width() // 2, self.locked_surf.get_height() // 2 + 25))

        self.locked_surf.blit(surf_1, rect_1)
        self.locked_surf.blit(surf_2, rect_2)

        self.tiles = [
            Tiles((240, 400), (i * (WINDOW_LENGTH // 5 + 40) + WINDOW_LENGTH // 5 - 60, WINDOW_HEIGHT // 2 + 50), True,
                  list(self.data.keys())[i], self.font_1, self.font_2, self.locked_surf) for i in range(4)
        ]

        # self.tiles[0].lock = False
        self.tiles[1].lock = False

        self.helper_text = self.font_2.render("Unlock Methods by playing Mini Games", False, 'white')

    def on_hover(self):
        if self.view == 'viewer':
            pos = pygame.mouse.get_pos()
            for ind, tile in enumerate(self.tiles):
                if not tile.lock:
                    if tile.rect.collidepoint(pos):
                        rect_2 = pygame.Rect(tile.rect.left + 5, tile.rect.top + 5, tile.rect.width, tile.rect.height)
                        pygame.draw.rect(self.display, "#99ccff", rect_2, 7)

                        if pygame.mouse.get_pressed()[0]:
                            self.view = ind

    def get_tile_data(self):
        return self.tiles

    def refresh(self):
        self.view = "viewer"

    def unlock_tile(self, name):
        for tile in self.tiles:
            if tile.name == name:
                tile.lock = False

    def play(self, dt):
        self.display.blit(self.background, self.back_rect)

        self.on_hover()

        if self.view == 'viewer':
            self.display.blit(self.title, (100, 70))
            self.display.blit(self.helper_text, (800, WINDOW_HEIGHT - 50))
            for tile in self.tiles:
                tile.render_tile()
        else:
            pass
