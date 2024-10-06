from math import sin

import pygame


class Button:
    def __init__(self, img, pos, func, *args):
        self.display = pygame.display.get_surface()

        if img:
            self.image = pygame.image.load(img).convert_alpha()
        else:
            self.image = pygame.Surface((24, 24))
            self.image.fill("white")
        self.rect = self.image.get_rect(center=pos)
        self.func = func
        self.func_args = args
        self.active = True

        self.timer = Timer(400)

    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.active:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(mouse_pos):
                self.active = False
                self.func(*self.func_args)
                self.timer.activate(self.change_state)
                return

    def change_state(self):
        self.active = True

    def draw(self):
        self.timer.update()
        self.display.blit(self.image, self.rect)
        self.on_click()


class PlayButton(Button):
    def __init__(self, font, text, font_size, pos, color, butt_color, func, *args):
        super().__init__(None, pos, func, args)
        self.display = pygame.display.get_surface()

        self.font = pygame.font.Font(font, font_size)
        self.surf = self.font.render(text, False, color)
        self.surf_rect = self.surf.get_rect(center=pos)
        self.rect = self.surf_rect.inflate(40, 20)
        self.but_rect_2 = self.rect.copy()
        self.button_color = butt_color
        self.active = True

        self.func = func
        self.func_args = args

    def draw(self):
        self.but_rect_2.topleft = self.rect.topleft + pygame.Vector2(0, sin(pygame.time.get_ticks() / 200)) * 5
        pygame.draw.rect(self.display, self.button_color, self.but_rect_2, border_radius=12, width=5)
        self.display.blit(self.surf, self.surf_rect.topleft + pygame.Vector2(0, sin(pygame.time.get_ticks() / 200)) * 5)
        self.on_click()


class Timer:
    def __init__(self, duration, func=None, *args):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.func = func
        self.args = args

    def activate(self, func=None, *args):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        if func:
            self.func = func
        if args:
            self.args = args

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.func:
            if self.args:
                self.func(*self.args)
                self.args = None
            else:
                self.func()
            self.func = None

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                self.deactivate()


class AnimatedText:
    def __init__(self, text, font: pygame.Font, color, pos, func):
        self.text = text
        self.surface = font.render("", False, color)
        self.rect = self.surface.get_rect(topleft=pos)
        self.font = font
        self.color = color
        self.func = func

        self.animate = False
        self.cur_index = 0
        self.key_press = False
        self.timer = Timer(25)

    def animate_text(self):
        if self.animate and not self.key_press:
            self.surface = self.font.render(self.text[:self.cur_index + 1], False, self.color)
            self.cur_index += 1

            if self.cur_index >= len(self.text):
                self.key_press = True
            else:
                self.animate = False
                self.timer.activate(self.wait_animate_text)

    def wait_animate_text(self):
        self.animate = True

    def wait_key_press(self):
        if self.key_press and self.animate:
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                self.key_press = False
                self.animate = False
                self.func()

    def start_animation(self):
        self.animate = True

    def render(self, surface):
        self.timer.update()
        self.animate_text()
        self.wait_key_press()
        surface.blit(self.surface, self.rect)
