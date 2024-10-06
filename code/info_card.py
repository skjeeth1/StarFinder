import pygame

from setup import WINDOW_HEIGHT, WINDOW_LENGTH


class InfoCard:
    def __init__(self, img=None, pos=None, func=None, width=40, *args):
        self.display = pygame.display.get_surface()
        self.func = func
        self.data = args
        self.width = width

        self.img = pygame.image.load(img) if img else None
        self.img = pygame.transform.scale(self.img, (400, 400)) if img else None
        self.img_rect = self.img.get_rect(center=pos) if img else None

        self.back_icon = pygame.image.load("assets/images/back.png").convert_alpha()
        self.back_icon_rect = self.back_icon.get_rect(bottomright=(WINDOW_LENGTH - 40, WINDOW_HEIGHT - 40))

        self.rendered_texts = []
        self.render_text()

    def render_text(self):
        for font, size, data, pos in self.data:
            spc_ind = [ind for ind, i in enumerate(data) if i == " "]

            split_ind = []
            prev_ind = -1
            for i in spc_ind:
                if i - prev_ind >= self.width:
                    split_ind.append((prev_ind + 1, i))
                    prev_ind = i
            split_ind.append((prev_ind + 1, len(data)))

            font_r = pygame.font.Font(font, size)

            for ind, (st, ed) in enumerate(split_ind):
                surf = font_r.render(data[st:ed], False, "white")
                rect = surf.get_rect(topleft=(pos[0], pos[1] + (ind * 35)))

                self.rendered_texts.append((surf, rect))

    def check_collision(self):
        if self.back_icon_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.func()

    def draw(self):
        self.check_collision()
        for surf, rect in self.rendered_texts:
            self.display.blit(surf, rect)
        self.display.blit(self.back_icon, self.back_icon_rect)
