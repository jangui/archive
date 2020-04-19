import sys
import pygame
from bullet import Bullet

def check_events(settings, screen, ship, bullets):
    #responds to key presses and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
           check_keyup_events(event, ship)

def update_screen(settings, screen, ship, bullets):
    #update images on screen
    screen.fill(settings.bg_color)
    #redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()

    #flush
    pygame.display.flip()

def check_keydown_events(event, settings, screen, ship, bullets):
    #responds to keypresses
    if event.key == pygame.K_RIGHT:
            ship.moving_right = True
    elif event.key == pygame.K_LEFT:
            ship.moving_left = True
    elif event.key == pygame.K_SPACE:
            if len(bullets) < settings.bullets_allowed:
                new_bullet = Bullet(settings, screen, ship)
                bullets.add(new_bullet)

def check_keyup_events(event, ship):
    #responds to keypresses
    if event.key == pygame.K_RIGHT:
            ship.moving_right = False
    elif event.key == pygame.K_LEFT:
            ship.moving_left = False