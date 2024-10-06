import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    #Initialize Sprites for player model
    def __init__(self, pos, limit):
        super().__init__()
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 5
        self.max_x = limit
        self.cannon = True
        self.time = 0
        self.cooldown = 600
        self.laser = pygame.sprite.Group()
    
    #Get user input    
    def game_input(self):
        key = pygame.key.get_pressed()
        
        #Movement Mechanism
        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif key[pygame.K_LEFT]:
            self.rect.x -= self.speed
            
        #Shooting Mechanism
        if key[pygame.K_SPACE] and self.cannon:
            self.shoot()
            self.cannon = False
            self.time = pygame.time.get_ticks()
    
    #Laser Cooldown   
    def recharge(self):
        if not self.cannon:
            current_time = pygame.time.get_ticks()
            if current_time - self.time >= self.cooldown:
                self.cannon = True
    
    #Boundaries
    def limits(self):
        if self.rect.left <= 32:
            self.rect.left = 32
        
        if self.rect.right >= self.max_x:
            self.rect.right = self.max_x
    
    #Laser
    def shoot(self):
        self.laser.add(Laser(self.rect.center, -8, self.rect.bottom))
    
    #Updating mechanism    
    def update(self):
        self.game_input()
        self.limits()
        self.recharge()
        self.laser.update()