import pygame
from pygame.sprite import Sprite

class Aliens(Sprite):
    """This class will store our aliens"""
    def __init__(self, game_settings, screen):
        """Initialize our attributes"""
        super(Aliens, self).__init__()

        self.screen = screen
        self.game_settings = game_settings

        # Load the image for aliens
        self.image = pygame.image.load('ayy.gif')
        self.rect = self.image.get_rect()

        # Start each alien from top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self. rect.height


        # Store the aliens exact position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at the edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move alien to the right"""
        self.x += (self.game_settings.alien_speed_factor*self.game_settings
                   .fleet_direction)
        self.rect.x = self.x



    def blitme(self):
        """Draw the alien at its exact position"""
        self.screen.blit(self.image, self.rect)
