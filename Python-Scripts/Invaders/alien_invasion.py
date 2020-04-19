import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    #initialize game, settings and create screen object
    pygame.init()
    #initailize settings
    settings = Settings()
    #create screen
    screen = pygame.display.set_mode(
            (settings.screen_width, settings.screen_height))
    #set caption for screen
    pygame.display.set_caption("Alien Invasion")

    #make a ship
    ship = Ship(settings, screen)

    #make a group to store bullets in
    bullets = Group()

    #main loop
    while True:
        gf.check_events(settings, screen, ship, bullets)
        ship.update()
        bullets.update()

        #get rid of bullets that leave screen
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)


        gf.update_screen(settings, screen, ship, bullets)

run_game()