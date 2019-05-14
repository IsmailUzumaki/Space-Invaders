import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class that reports the scoring information"""

    def __init__(self, game_settings, screen, stats):
        """Intialize scorekeeping attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.game_settings = game_settings


        # Font settings for scoring info.
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        # Prepare the high score image
        self.prep_high_score()
        # Prepare the level image
        self.prep_level()
        # Prepare the ship/lives image
        self.prep_ship()
        # Prepare bullet image
        self.prep_bullet()


    def prep_score(self):
        """Turn the score into a rendered image"""
        score_format = int(self.stats.score)
        score_str = "{:,}".format(score_format)
        self.score_image = self.font.render(score_str, True,
                                            self.text_colour,
                                            self.game_settings.bg_colour)
        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        high_score_format = int(self.stats.high_score)
        high_score_str = "Highscore: "+"{:,}".format(high_score_format)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_colour,
                                                 self.game_settings.bg_colour)
        # Create the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        """Turn the level the game is on into a rendered image"""
        level_format = "Level: "+str(self.stats.level)
        self.level_image = self.font.render(level_format, True,
                                         self.text_colour,
                                         self.game_settings.bg_colour)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left
        self.level_rect.top = self.screen_rect.top

    def prep_ship(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game_settings, self.screen)
            ship.rect.x = 1130 + ship_number * ship.rect.width
            ship.rect.y = 90
            self.ships.add(ship)

    def prep_bullet(self):
        """Render an image of bullets left"""
        bullet_format = int(self.game_settings.amo)
        bullets_left = "Amo: ". format(bullet_format)
        self.bullet_image = self.font.render(bullets_left, True,
                                              self.text_colour,
                                              self.game_settings.bg_colour)

        # Display the bullets left at the top right of screen
        self.bullet_rect = self.bullet_image.get_rect()
        self.bullet_rect.right = self.bullet_rect.right + 1
        self.bullet_rect.top = 30



    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.bullet_image, self.bullet_rect)
        # Draw ship
        self.ships.draw(self.screen)