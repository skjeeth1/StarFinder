import pygame

from miscellaneous import Button
from planet_finder import Tiles
from setup import *
from stage import Stage


class Launch(Stage):
    def __init__(self, change_state, get_unlocked_planet_data):
        super().__init__(change_state)

        self.font_1 = pygame.font.Font(FONT, 45)
        self.font_2 = pygame.font.Font(FONT, 20)
        self.unlocked_planet_data = get_unlocked_planet_data
        self.check_game_win = None

        self.tile_size = (WINDOW_LENGTH // 2 - 100, 150)

        self.title = pygame.font.Font(TITLE_FONT, 50).render("LAUNCH THE VOYAGE", False, "white")

        self.locked_surf = pygame.Surface(self.tile_size, pygame.SRCALPHA)
        surf_1 = self.font_2.render("Find this", False, "#EEEEEE")
        surf_2 = self.font_1.render("Planet", False, "#EEEEEE")
        rect_1 = surf_1.get_rect(
            center=(self.locked_surf.get_width() // 2, self.locked_surf.get_height() // 2 - 25))
        rect_2 = surf_2.get_rect(
            center=(self.locked_surf.get_width() // 2, self.locked_surf.get_height() // 2 + 25))

        self.locked_surf.blit(surf_1, rect_1)
        self.locked_surf.blit(surf_2, rect_2)

        self.tiles = []

        self.create_tiles()
        self.selected_page = None
        self.selected_page_surf = self.font_2.render(f"Selected planet: {self.selected_page}", False, 'white')

        self.page = 0

        self.background = pygame.image.load("assets/images/night_sky.jpg")
        surf = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        surf.fill((50, 50, 50, 0))
        self.background.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.back_rect = self.background.get_rect(top=0, left=0)

        self.right_button = Button("assets/images/next.png", (1250, WINDOW_HEIGHT // 2 + 50), self.change_page, 1)
        self.left_button = Button("assets/images/previous.png", (30, WINDOW_HEIGHT // 2 + 50), self.change_page, 0)

        self.page_text = self.font_2.render(f"Page {self.page + 1} / {len(self.tiles) // 4 + 1}", False, 'white')
        self.helper_text = self.font_2.render("Press Enter to launch", False, 'white')

    def create_tiles(self):
        for ind, (disc, name, *data) in enumerate(PLANET_DATA.values()):
            if ind % 4 == 0:
                tile = Tiles(self.tile_size, (
                    WINDOW_LENGTH // 5 + 100, WINDOW_HEIGHT // 2 - 50), True, name,
                                   self.font_1, self.font_2, self.locked_surf, data)
            elif ind % 4 == 1:
                tile = Tiles(self.tile_size, (
                    (self.tile_size[0] + 50) + WINDOW_LENGTH // 5 + 100, WINDOW_HEIGHT // 2 - 50), True,
                                   name, self.font_1, self.font_2, self.locked_surf, data)
            elif ind % 4 == 2:
                tile = Tiles(self.tile_size, (
                    WINDOW_LENGTH // 5 + 100, (self.tile_size[1] + 50) + WINDOW_HEIGHT // 2 - 50), True, name,
                                   self.font_1, self.font_2, self.locked_surf, data)
            else:
                tile = Tiles(self.tile_size, (
                    (self.tile_size[0] + 50) + WINDOW_LENGTH // 5 + 100,
                    (self.tile_size[1] + 50) + WINDOW_HEIGHT // 2 - 50), True,
                                   name,
                                   self.font_1, self.font_2, self.locked_surf, data)

            self.tiles.append(tile)

    def on_hover(self):
        pos = pygame.mouse.get_pos()
        for ind, tile in enumerate(self.tiles[self.page * 4:(self.page + 1) * 4]):
            if not tile.lock:
                if tile.rect.collidepoint(pos):
                    rect_2 = pygame.Rect(tile.rect.left + 5, tile.rect.top + 5, tile.rect.width,
                                         tile.rect.height)
                    pygame.draw.rect(self.display, "#99ccff", rect_2, 7)

                    if pygame.mouse.get_pressed()[0]:
                        self.selected_page = tile.name
                        self.selected_page_surf = self.font_2.render(f"Selected planet: {self.selected_page}", False,
                                                                     'white')

    def get_tile_data(self):
        return self.tiles

    def unlock_tile(self, name):
        for tile in self.tiles:
            if tile.name == name:
                tile.lock = False

    def change_page(self, *args):
        if args[0]:
            self.page += 1
            if self.page >= len(self.tiles) // 4:
                self.page = len(self.tiles) // 4
        elif not args[0]:
            self.page -= 1
            if self.page <= 0:
                self.page = 0

        self.page_text = self.font_2.render(f"Page {self.page + 1} / {len(self.tiles) // 4 + 1}", False, 'white')

    def refresh(self):
        self.page = 0
        data = self.unlocked_planet_data()

        for tile in self.tiles:
            if tile.lock and tile.name in data:
                tile.lock = False

    def play(self, dt):
        self.display.blit(self.background, self.back_rect)

        self.on_hover()
        self.display.blit(self.title, (100, 70))
        self.right_button.draw()
        self.left_button.draw()
        self.display.blit(self.page_text, (1100, WINDOW_HEIGHT - 50))
        self.display.blit(self.selected_page_surf, (100, WINDOW_HEIGHT - 50))
        self.display.blit(self.helper_text, (100, 130))
        for tile in self.tiles[self.page * 4:(self.page + 1) * 4]:
            tile.render_tile()

        if self.selected_page:
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                self.check_game_win(self.selected_page)
