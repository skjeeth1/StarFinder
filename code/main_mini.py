from random import choice

import pygame

from miscellaneous import Timer
from setup import *


class GameTimer(Timer):
    def deactivate(self):
        self.start_time = pygame.time.get_ticks()
        if self.func:
            if self.args:
                self.func(*self.args)
            else:
                self.func()


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.max_y = screen_height

    # Remove the lasers
    def remove(self):
        if self.rect.y <= -50 or self.rect.y >= self.max_y + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.remove()


class Player(pygame.sprite.Sprite):
    # Initialize Sprites for player model
    def __init__(self, pos, limit):
        super().__init__()
        self.image = pygame.image.load('assets/images/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = 5
        self.max_x = limit
        self.cannon = True
        self.time = 0
        self.cooldown = 600
        self.laser = pygame.sprite.Group()

    # Get user input
    def game_input(self):
        key = pygame.key.get_pressed()

        # Movement Mechanism
        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif key[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Shooting Mechanism
        if key[pygame.K_SPACE] and self.cannon:
            self.shoot()
            self.cannon = False
            self.time = pygame.time.get_ticks()

    # Laser Cooldown
    def recharge(self):
        if not self.cannon:
            current_time = pygame.time.get_ticks()
            if current_time - self.time >= self.cooldown:
                self.cannon = True

    # Boundaries
    def limits(self):
        if self.rect.left <= 32:
            self.rect.left = 32

        if self.rect.right >= self.max_x:
            self.rect.right = self.max_x

    # Laser
    def shoot(self):
        self.laser.add(Laser(self.rect.center, -8, self.rect.bottom))

    # Updating mechanism
    def update(self):
        self.game_input()
        self.limits()
        self.recharge()
        self.laser.update()


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    # Alien Movement
    def update(self, direction):
        self.rect.x += direction


class Game:

    # Initialize
    def __init__(self, quit_game, clue_num):
        self.clock = pygame.time.Clock()
        player_sprite = Player((WINDOW_LENGTH / 2 - 32, WINDOW_HEIGHT - 50), WINDOW_LENGTH - 32)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=10)
        self.alien_speed = 2

        self.quit_game = quit_game
        self.clue_num = clue_num

        # Health setup
        self.lives = 3
        self.life_surf = pygame.image.load('assets/images/player.png').convert_alpha()
        self.life_x_start = WINDOW_LENGTH - (self.life_surf.get_size()[0] * 2 + 20)
        self.font = pygame.font.Font('assets/fonts/pixeled-font/Pixeled.ttf', 20)

        self.shoot_timer = GameTimer(800)
        self.shoot_timer.activate(self.shoot)
        self.victory = False
        self.end_timer = GameTimer(8000)

        self.clues = [
            ["They seem to have stolen an encyclopedia from the mid Twenties",
             "The book might provide more information"],
            ["Congratulations!!", "You have successfully captured some aliens."],

        ]

    # Creating alien sprites
    def alien_setup(self, rows, cols, x_dist=60, y_dist=48, x_off=32, y_off=25):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_dist + x_off
                y = row_index * y_dist + y_off
                alien_sprite = Alien(x, y)
                self.aliens.add(alien_sprite)

    # Positioning the aliens
    def position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.left <= 32:
                self.alien_speed = 2
                if self.aliens:
                    for aliens in self.aliens.sprites():
                        aliens.rect.y += 3

            elif alien.rect.right >= WINDOW_LENGTH - 32:
                self.alien_speed = -2
                if self.aliens:
                    for aliens in self.aliens.sprites():
                        aliens.rect.y += 3

    # Aliens shooting mechanism
    def shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 5, WINDOW_HEIGHT)
            self.alien_lasers.add(laser_sprite)

    # Collision checker for player
    def collision_check(self):
        if self.player.sprite.laser:
            for lasers in self.player.sprite.laser:
                if pygame.sprite.spritecollide(lasers, self.aliens, True):
                    lasers.kill()

    # Collision checker for alien
    def alien_collision(self):
        if self.alien_lasers:
            for lasers in self.alien_lasers:
                if pygame.sprite.spritecollide(lasers, self.player, False):
                    lasers.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.quit_game(False)
        if self.aliens:
            for alien in self.aliens:
                if pygame.sprite.spritecollide(alien, self.player, True):
                    self.quit_game(False)

    def disp_life(self, screen):
        for life in range(self.lives - 1):
            x = self.life_x_start + (life * (self.life_surf.get_size()[0] + 10))
            screen.blit(self.life_surf, (x, 8))

    # Victory message
    def check_victory(self, screen):
        if not self.aliens.sprites() and not self.victory:
            self.victory = True
            self.end_timer.activate(self.quit_game, True)

        if self.victory:
            victor_surf = self.font.render('You have defeated the raid!', False, 'white')
            victor_rect = victor_surf.get_rect(center=(WINDOW_LENGTH / 2, WINDOW_HEIGHT / 2 - 40))
            screen.blit(victor_surf, victor_rect)

            if self.clue_num < len(self.clues):
                for ind, i in enumerate(self.clues[self.clue_num]):
                    surf = self.font.render(i, False, 'white')
                    rect = surf.get_rect(center=(WINDOW_LENGTH / 2, WINDOW_HEIGHT / 2 + ind * 40 + 20))

                    screen.blit(surf, rect)

    # Main running method
    def run(self, screen):
        screen.fill((30, 30, 30))
        self.shoot_timer.update()
        self.end_timer.update()
        self.clock.tick(60)
        self.check_victory(screen)

        if not self.victory:
            self.aliens.update(self.alien_speed)
            self.player.update()
            self.alien_lasers.update()
            self.collision_check()
            self.alien_collision()
            self.position_checker()
            self.disp_life(screen)

            self.player.sprite.laser.draw(screen)
            self.player.draw(screen)
            self.aliens.draw(screen)
            self.alien_lasers.draw(screen)

        # if pygame.key.get_pressed()[pygame.K_k]:
        #     self.aliens.empty()
