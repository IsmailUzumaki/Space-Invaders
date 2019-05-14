import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class that stores our ship"""

    def __init__(self, game_settings, screen):
        """Initalize the attributes of our ship"""
        super(Ship, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load the ships image get its rect.
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom



        # Store decimal value of the ship's center
        self.center = float(self.rect.centerx)
        # Store decimal value of the ship's ground position
        self.bottom = float(self.rect.bottom)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ships movement based on movement flag"""
        # Move to the right from the center
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor

        # Moving to the left from center
        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed_factor

        # Moving the ship down
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.game_settings.ship_speed_factor

        # Moving the ship up
        if self.moving_up and self.rect.top > 0:
            self.bottom -= self.game_settings.ship_speed_factor


        # Update rect object from self.center
        self.rect.centerx = self.center
        # Update rect object from self.bottom
        self.rect.bottom = self.bottom

    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx

    def ground_ship(self):
        """Place ship on the bottom of screen"""
        self.bottom = self.screen_rect.bottom



    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
