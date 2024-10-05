import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, size, color, x, y):
        super().__init__()
        self.image = pygame.image.load('graphics/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        
shape=[
'x']

 

               
