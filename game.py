import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf



def run_game():
    """Initalize game and create a screen object."""
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width,
                                      game_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")
    # Create an instance of to store game stats
    stats = GameStats(game_settings)
    score = Scoreboard(game_settings, screen, stats)

    # Make the play button
    play_button = Button(game_settings, screen, "Play")

    # create a ship
    my_ship = Ship(game_settings, screen)

    # Make a group to store bullets
    shellings = Group()
    roadman = Group()

    # Create alien fleet
    gf.create_fleet(game_settings, screen, roadman, my_ship)

    #Start the main loop for the game
    while True:
        gf.events(game_settings, my_ship, screen, shellings, stats,
                  play_button, roadman, score)
        if stats.game_active:
            my_ship.update()

            gf.update_bullets(shellings, roadman, game_settings, screen,
                              my_ship, stats, score)
            gf.update_aliens(game_settings, roadman, my_ship, stats,
                             shellings, screen, score)

        gf.update_screen(game_settings, screen, my_ship, roadman, shellings,
                             play_button, stats, score)
        shellings.update()

run_game()
