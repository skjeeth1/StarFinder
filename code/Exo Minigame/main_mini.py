import pygame,sys
from player import Player
from alien import Alien
from random import choice
from laser import Laser

class Game:
    
    #Initialize
    def __init__(self):
        player_sprite = Player((screen_width/2 - 32, screen_height - 50),screen_width - 32)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 2, cols = 2)
        self.alien_speed = 2
        
        #Health setup
        self.lives = 3
        self.life_surf = pygame.image.load('graphics/player.png').convert_alpha()
        self.life_x_start = screen_width - (self.life_surf.get_size()[0]*2 +20)
        self.font = pygame.font.Font('font/Pixeled.ttf',20)
        
    #Creating alien sprites
    def alien_setup(self, rows, cols, x_dist = 60, y_dist = 48, x_off = 32, y_off = 25):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_dist + x_off
                y = row_index * y_dist + y_off
                alien_sprite = Alien(x, y)
                self.aliens.add(alien_sprite)
                
    #Positioning the aliens
    def position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.left <= 32:
                self.alien_speed = 2
                if self.aliens:
                    for aliens in self.aliens.sprites():
                        aliens.rect.y += 3
                        
            elif alien.rect.right >= screen_width - 32:
                self.alien_speed = -2
                if self.aliens:
                    for aliens in self.aliens.sprites():
                        aliens.rect.y += 3
    
    #Aliens shooting mechanism
    def shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 5, screen_height)
            self.alien_lasers.add(laser_sprite)
    
    #Collision checker for player
    def collision_check(self):            
        if self.player.sprite.laser:
            for lasers in self.player.sprite.laser:
                if pygame.sprite.spritecollide(lasers, self.aliens, True):
                    lasers.kill()
                    
    #Collision checker for alien
    def alien_collision(self):
        if self.alien_lasers:
            for lasers in self.alien_lasers:
                if pygame.sprite.spritecollide(lasers, self.player, False):
                    lasers.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()
        if self.aliens:
            for alien in self.aliens:
                if pygame.sprite.spritecollide(alien, self.player, True):
                    pygame.quit()
                    sys.exit()
                
    def disp_life(self):
        for life in range(self.lives - 1):
            x = self.life_x_start + (life * (self.life_surf.get_size()[0]+10))
            screen.blit(self.life_surf, (x,8))
    
    #Victory message
    def victory(self):
        if not self.aliens.sprites():
            hint_surf = self.font.render('Hint: Visit The Night Sky page to view the locations of exoplanets!', False, 'white')
            hint_rect = hint_surf.get_rect(center = (screen_width/2 - 15, screen_height/2 + 35))
            victor_surf = self.font.render('You won!', False, 'white')
            victor_rect = victor_surf.get_rect(center = (screen_width/2, screen_height/2))
            screen.blit(victor_surf, victor_rect)
            screen.blit(hint_surf,hint_rect)
    
    #Main running method
    def run(self):
        self.aliens.update(self.alien_speed)
        self.player.update()
        self.alien_lasers.update()
        self.collision_check()
        self.alien_collision()
        self.position_checker()
        self.disp_life()
        self.victory()
        self.player.sprite.laser.draw(screen)
        self.player.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
            
if __name__ == '__main__':
    
    #Initialize pygame
    pygame.init()
    screen_width = 1280
    screen_height = 640
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    
    #Title and icon
    icon = pygame.image.load('graphics/icon.png').convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Space Invaders Minigame")
    
    #Slowing down alien laser
    alaser = pygame.USEREVENT + 1
    pygame.time.set_timer(alaser,800)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == alaser:
                game.shoot()
                
        screen.fill((30, 30, 30))
        game.run()
        pygame.display.update()
        clock.tick(60)