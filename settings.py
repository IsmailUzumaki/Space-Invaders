import pygame
class Settings:
    """A class that stores all settings for Alien Invasion"""
    def __init__(self):
        """Initialize the games settings"""
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_colour = (20, 20, 20)


        # Ship settings
        self.ship_speed_factor = 5.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 2
        self.bullet_height = 10
        self.bullet_colour = (255, 255, 255)
        self.amo = 5

        # Alien settings
        self.alien_speed_factor = 5.5
        self.fleet_drop_speed = 5.5
        # fleet direction 1 rep. right, and -1 rep. left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 2

        self.intialize_dynamic_settings()

    def intialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet direction 1 rep. right, and -1 rep. left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings alien points"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points*self.score_scale)
