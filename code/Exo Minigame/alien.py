import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('graphics/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
    
    #Alien Movement
    def update(self, direction):
        self.rect.x += direction