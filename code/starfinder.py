import pygame

from info_card import InfoCard
from miscellaneous import AnimatedText
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

    def unlock(self):
        self.lock = False

    def check_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.info_card(self.name, self.disc_data, self.unlock)

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

        font = pygame.font.Font(FONT, 17)
        self.text_lines = [
            [
                "Commander: Let's recap your mission one more time.",
                "Commander: Our AI is stolen because of those stupid multi-headed aliens.",
                "Commander: We need you sergeant to use this old piece of tech to find those multi-headed freaks' planet",
                "Commander: before they reach, and take back our precious AI before they do something with her ;(",
                "Commander: But how did our grandparents find these planets?     .    .    .",
                "Narrator: Find exoplanets in the night sky using the map. You have to unlock clues using mini games.",
                "Narrator: You can use Stellarium-web.org or the NASA website to get information.",
            ],
            [
                "Commander: Hmmm.. Looks likes this information is good! These aliens did us good by stealing some of ",
                "Commander: these old encyclopedias.",
                "Narrator: Goto the Exoplanet Finder page in the menu tab (top-left). Read about the information provided",
                "Narrator: and try to find exoplanets found using those methods in night sky map.",
                "Narrator: You can also view information about found exoplanets in the almanac tab of the menu."
            ],
            [
                "Commander: Looks like they are going back to their base, huh?",
                "Commander: Habitable planets, hmmm? Didn't hear a lot about them from my grandparents.",
                "Narrator: May be the almanac contains information about the planets you might've missed.",
            ]
        ]
        self.helper_texts = [
            [AnimatedText(i, font, "white", (50, 590), self.change_text) for i in self.text_lines[j]]
            for j in range(len(self.text_lines))
        ]
        self.helper_lines = 0

        self.helper_index = 0
        self.helper_texts[self.helper_lines][0].start_animation()

    def draw_lines(self, pos):
        pygame.draw.line(self.display, 'white', (pos[0], 0), (pos[0], WINDOW_HEIGHT))
        pygame.draw.line(self.display, 'white', (0, pos[1]), (WINDOW_LENGTH, pos[1]))

    def check_active(self, rect):
        mouse_pos = (pygame.mouse.get_pos())

        if rect.collidepoint(mouse_pos):
            self.draw_lines(mouse_pos)

    def invoke_info_card(self, name, planet_data, unlock_planet):
        tile_data = self.tile_data()

        for tile in tile_data:
            if tile.name == planet_data:
                if tile.lock:
                    pass
                else:
                    self.view = name
                    unlock_planet()

    def create_entities(self):
        for (x, y), (disc, name, *desc) in PLANET_DATA.items():
            Planet(self.entities, (x, y), name, True, disc, self.invoke_info_card)

            texts = [(FONT, 30, i, (100, ind * 75 + 250 )) for ind, i in enumerate(desc)]
            texts.append((FONT, 40, name, (100, 100)))

            texts = [(FONT, 25, desc[0], (100, 325))]

            self.info_cards[name] = InfoCard(None, None, self.refresh, *texts)

    def refresh(self):
        self.view = "viewer"

    def change_text(self):
        self.helper_index += 1
        if self.helper_index >= len(self.helper_texts[self.helper_lines]):
            self.helper_index = len(self.helper_texts[self.helper_lines]) - 1
        else:
            self.helper_texts[self.helper_lines][self.helper_index].start_animation()

    def unlocked_planet_data(self):
        planet_data = []
        for sprite in self.entities:
            if not sprite.lock:
                planet_data.append(sprite.name)

        return planet_data

    def info_card_data(self):
        return self.info_cards

    def clue_received(self, clue_num):
        self.helper_lines = clue_num if clue_num != -1 else -1
        self.helper_index = 0
        self.helper_texts[self.helper_lines][0].start_animation()

    def play(self, dt):
        self.display.blit(self.background, self.back_rect)

        if self.view == "viewer":
            self.entities.update()
            self.entities.draw(self.display)
            self.check_active(self.active_rect)
            self.helper_texts[self.helper_lines][self.helper_index].render(self.display)

        else:
            self.display.blit(self.dark_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            self.info_cards[self.view].draw()
