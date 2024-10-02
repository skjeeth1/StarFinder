import pygame

class Button:
    def __init__(self, font, text, font_size, pos, color, butt_color, click_func, *args) -> None:
        self.display = pygame.display.get_surface()

        self.font = pygame.font.Font(font, font_size)
        self.surf = self.font.render(text, False, color)
        self.rect = self.surf.get_rect(center=pos)
        self.but_rect = self.rect.inflate(40, 20)
        self.button_color = butt_color
        self.active = True

        self.click_func = click_func
        self.func_args = args
    
    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.active:
            if pygame.mouse.get_pressed()[0] and self.but_rect.collidepoint(mouse_pos):
                self.active = False
                self.click_func(*self.func_args)


    def draw(self):
        pygame.draw.rect(self.display, self.button_color, self.but_rect, border_radius=12, width=5)
        self.display.blit(self.surf, self.rect)
        self.on_click()

