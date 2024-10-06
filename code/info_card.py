import pygame

from setup import WINDOW_HEIGHT, WINDOW_LENGTH


class InfoCard:
    def __init__(self, img=None, pos=None, func=None, *args):
        self.display = pygame.display.get_surface()
        self.func = func
        self.data = args

        self.img = pygame.image.load(img) if img else None
        self.img = pygame.transform.scale(self.img, (400, 400)) if img else None
        self.img_rect = self.img.get_rect(center=pos) if img else None

        self.back_icon = pygame.Surface((24, 24))
        self.back_icon.fill("white")
        self.back_icon_rect = self.back_icon.get_rect(bottomright=(WINDOW_LENGTH - 40, WINDOW_HEIGHT - 40))

        self.rendered_texts = []
        self.render_text()

    def render_text(self):
        for font, size, data, pos in self.data:
            data = data.split()
            spc_ind = [ind for ind, i in enumerate(data) if i == " "]

            split_ind = []
            prev_ind = 0
            for i in spc_ind:
                if i - prev_ind >= 25:
                    split_ind.append((prev_ind, i))
                    prev_ind = 0

            for i in range(0, len(data), 5):
                surf = pygame.font.Font(font, size).render(" ".join(data[i:min(i + 5, len(data))]), False, "white")
                rect = surf.get_rect(topleft=(pos[0], pos[1] + (i // 5 * 35)))

                self.rendered_texts.append((surf, rect))

    def check_collision(self):
        if self.back_icon_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.func()

    def draw(self):
        self.check_collision()
        for surf, rect in self.rendered_texts:
            self.display.blit(surf, rect)
        self.display.blit(self.back_icon, self.back_icon_rect)
