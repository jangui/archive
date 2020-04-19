import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        #create bullet hitbox at (0,0) and then change it to right position
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #store bullet position as decimal
        self.y = float(self.rect.y)
        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        #update decimal position of bullet
        self.y -= self.speed_factor
        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)