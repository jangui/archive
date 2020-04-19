import pygame

class Ship():

    def __init__(self, settings, screen):
        self.screen = screen
        self.settings = settings
        #load ship and get its 'rectangle' (hitbox / represenation of ship)
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        #Set ship position (x: middle of screen, y: bottom of screen)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #store decimal value for ship's center
        self.center = float(self.rect.centerx)
        #movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
    #update movement based on direction flags
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed_factor
        #update pos
        self.rect.centerx = self.center

    def blitme(self):
        #draws ship at current location
        self.screen.blit(self.image, self.rect)