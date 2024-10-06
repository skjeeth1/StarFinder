import pygame

from miscellaneous import Button
from planet_finder import Tiles
from setup import *
from stage import Stage


class NewTiles(Tiles):
    def render_text(self):
        surf_1 = self.font_2.render(' '.join(self.name.split()[0]), False, "#EEEEEE")
        surf_2 = self.font_1.render(self.name.split()[-1], False, "#EEEEEE")
        rect_1 = surf_1.get_rect(
            midleft=(50, 60))
        rect_2 = surf_2.get_rect(
            midleft=(50, 120))

        self.surf.blit(surf_1, rect_1)
        self.surf.blit(surf_2, rect_2)

        for ind, i in enumerate(self.data[-3:]):
            surf = self.font_2.render(i, False, "#EEEEEE")
            rect = surf.get_rect(midleft=(50, ind * 40 + 270))

            self.surf.blit(surf, rect)


class Almanac(Stage):
    def __init__(self, change_state, get_unlocked_planet_data):
        super().__init__(change_state)

        self.font_1 = pygame.font.Font(FONT, 45)
        self.font_2 = pygame.font.Font(FONT, 20)
        self.unlocked_planet_data = get_unlocked_planet_data
        self.info_cards = None

        self.tile_size = (WINDOW_LENGTH // 2 - 100, 400)

        self.title = pygame.font.Font(TITLE_FONT, 50).render("EXOPLANET ALMANAC", False, "white")

        self.locked_surf = pygame.Surface(self.tile_size, pygame.SRCALPHA)
        surf_1 = self.font_2.render("Unlock this", False, "#EEEEEE")
        surf_2 = self.font_1.render("Planet", False, "#EEEEEE")
        rect_1 = surf_1.get_rect(
            center=(self.locked_surf.get_width() // 2, self.locked_surf.get_height() // 2 - 25))
        rect_2 = surf_2.get_rect(
            center=(self.locked_surf.get_width() // 2, self.locked_surf.get_height() // 2 + 25))

        self.locked_surf.blit(surf_1, rect_1)
        self.locked_surf.blit(surf_2, rect_2)

        self.tiles = []

        self.create_tiles()

        self.view = 'viewer'
        self.page = 0

        self.background = pygame.image.load("assets/images/night_sky.jpg")
        surf = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        surf.fill((50, 50, 50, 0))
        self.background.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.back_rect = self.background.get_rect(top=0, left=0)

        self.right_button = Button((1250, WINDOW_HEIGHT // 2 + 50), self.change_page, 1)
        self.left_button = Button((30, WINDOW_HEIGHT // 2 + 50), self.change_page, 0)

    def create_tiles(self):
        for ind, (disc, name, *data) in enumerate(PLANET_DATA.values()):
            self.tiles.append(
                NewTiles(self.tile_size,
                         ((ind % 2) * (self.tile_size[0] + 50) + WINDOW_LENGTH // 5 + 100, WINDOW_HEIGHT // 2 + 50),
                         True, name, self.font_1, self.font_2, self.locked_surf, data)
            )

    def on_hover(self):
        if self.view == 'viewer':
            pos = pygame.mouse.get_pos()
            for ind, tile in enumerate(self.tiles[self.page * 2:(self.page + 1) * 2]):
                if not tile.lock:
                    if tile.rect.collidepoint(pos):
                        rect_2 = pygame.Rect(tile.rect.left + 5, tile.rect.top + 5, tile.rect.width,
                                             tile.rect.height)
                        pygame.draw.rect(self.display, "#99ccff", rect_2, 7)

                        if pygame.mouse.get_pressed()[0]:
                            self.view = tile.name

    def get_tile_data(self):
        return self.tiles

    def unlock_tile(self, name):
        for tile in self.tiles:
            if tile.name == name:
                tile.lock = False

    def change_page(self, *args):
        if args[0]:
            self.page += 1
            if self.page >= len(self.tiles) // 2:
                self.page = len(self.tiles) // 2
        elif not args[0]:
            self.page -= 1
            if self.page <= 0:
                self.page = 0

    def refresh(self):
        self.view = "viewer"
        self.page = 0
        data = self.unlocked_planet_data()

        for tile in self.tiles:
            if tile.lock and tile.name in data:
                tile.lock = False

    def play(self, dt):
        self.display.blit(self.background, self.back_rect)

        self.on_hover()

        if self.view == 'viewer':
            self.display.blit(self.title, (100, 70))
            self.right_button.draw()
            self.left_button.draw()
            # self.display.blit(self.helper_text, (800, WINDOW_HEIGHT - 50))
            for tile in self.tiles[self.page * 2:(self.page + 1) * 2]:
                tile.render_tile()
        else:
            self.info_cards[self.view].draw()
