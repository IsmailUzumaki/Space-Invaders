class GameStats:
    """Tracks statistics for Alien Invasion"""

    def __init__(self, game_settings):
        """Initialize statistics."""
        self.game_settings = game_settings
        self.reset_stats()
        # Start Alien Invasion in an active state
        self.game_active = False
        # High Score shouldnt be reset just updated
        self.high_score = 0



    def reset_stats(self):
        """Initialze statistics that can change during the game"""
        self.ships_left = self.game_settings.ship_limit
        self.score = 0
        self.level = 1
