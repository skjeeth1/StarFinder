import pygame

from info_card import InfoCard
from setup import *
from stage import Stage


class SpriteGroup(pygame.sprite.Group):
    def draw(self, surface):
        for sprite in self.sprites():
            if hasattr(sprite, "lock"):
                if not sprite.lock:
                    surface.blit(sprite.image, sprite.rect)
            else:
                surface.blit(sprite.image, sprite.rect)


class Entity(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)

        self.image = pygame.Surface((20, 20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=pos)


class Planet(Entity):
    def __init__(self, group, pos, name, lock, disc_data, info_card):
        super().__init__(group, pos)
        self.name = name
        self.disc_data = disc_data
        self.info_card = info_card
        self.lock = lock

    def check_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.info_card(self.name, self.disc_data)

    def update(self):
        self.check_collision()


class StarFinderLevel(Stage):
    def __init__(self, change_state, lock_data) -> None:
        super().__init__(change_state)

        self.tile_data = lock_data
        self.background = pygame.image.load("assets/images/night_sky.jpg")
        self.back_rect = self.background.get_rect(top=0, left=0)
        self.dark_surf = pygame.Surface((WINDOW_LENGTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.dark_surf.fill((50, 50, 50, 0))

        self.active_area = pygame.Surface((WINDOW_LENGTH - 100, WINDOW_HEIGHT - 100))
        self.active_rect = self.active_area.get_rect(center=self.back_rect.center)

        self.entities = SpriteGroup()
        self.info_cards = {}
        self.create_entities()
        self.cur_entity = ''

        self.view = "viewer"
        # print(self.info_cards)

    def draw_lines(self, pos):
        pygame.draw.line(self.display, 'white', (pos[0], 0), (pos[0], WINDOW_HEIGHT))
        pygame.draw.line(self.display, 'white', (0, pos[1]), (WINDOW_LENGTH, pos[1]))

    def check_active(self, rect):
        mouse_pos = (pygame.mouse.get_pos())

        if rect.collidepoint(mouse_pos):
            self.draw_lines(mouse_pos)

    def invoke_info_card(self, name, planet_data):
        tile_data = self.tile_data()

        for tile in tile_data:
            if tile.data == planet_data:
                if tile.lock:
                    pass
                else:
                    self.view = name

    def create_entities(self):
        for (x, y), (disc, name, *desc) in PLANET_DATA.items():
            Planet(self.entities, (x, y), name, False, disc, self.invoke_info_card)

            texts = [(FONT, 30, i, (100, ind * 75 + 250)) for ind, i in enumerate(desc)]
            texts.append((FONT, 40, name, (100, 100)))

            self.info_cards[name] = InfoCard(None, None, self.refresh, *texts)

    def refresh(self):
        self.view = "viewer"

    def play(self, dt):
        self.display.blit(self.background, self.back_rect)

        if self.view == "viewer":
            self.entities.update()
            self.entities.draw(self.display)
            self.check_active(self.active_rect)

        else:
            self.display.blit(self.dark_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            self.info_cards[self.view].draw()
