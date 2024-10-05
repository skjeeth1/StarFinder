import pygame


class InfoCard:
    def __init__(self, img=None, pos=None, *args):
        self.display = pygame.display.get_surface()
        self.data = args
        self.img = pygame.image.load(img) if img else None
        self.img = pygame.transform.scale(self.img, (400, 400)) if img else None
        self.img_rect = self.img.get_rect(center=pos) if img else None

        self.rendered_texts = []
        self.render_text()

    def render_text(self):
        for font, size, data, pos in self.data:
            surf = pygame.font.Font(font, size).render(data, False, "white")
            rect = surf.get_rect(topleft=pos)

            self.rendered_texts.append((surf, rect))

    def draw(self):
        for surf, rect in self.rendered_texts:
            self.display.blit(surf, rect)
