import sys
from time import sleep
import pygame
from bullets import Bullets
from aliens import Aliens
from button import Button


def check_keydown_events(event, ship, game_settings, screen, bullets):
    """Respond to key being pressed down"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # Left key is pressed
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # Up Key is pressed
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    # Down key is pressed
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    # Space bar is pressed
    elif event.key == pygame.K_SPACE:
        fire_bullets(bullets, game_settings, screen, ship)
    # Exit the game
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond if the keys are let go"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # Left key is let go
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    # Right Key let go
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_continuous_right(event, ship):
    """Respond if the right key is held down"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False


def check_continous_left(event, ship):
    """Respond if the left key is contiously pressed"""
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_move_up(event, ship):
    """Responds if the up button is pressed"""
    if event.key == pygame.K_UP:
        ship.moving_up = True


def events(game_settings, ship, screen, bullets, stats, play_button, aliens,
           scoreboard):
    """Watch for Keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
         # Moving the ship to the right
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, game_settings, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        # Holding down a key for continuous movement
        elif event.type == pygame.KEYUP:
            # Continuous movement to the right
            check_continuous_right(event, ship)
            # Moving the ship continously to the left
            check_continous_left(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, ship, screen, bullets, stats,
                              play_button, aliens,
                              scoreboard, mouse_x, mouse_y)


def check_play_button(game_settings, ship, screen, bullets, stats, play_button, aliens,
           scoreboard, mouse_x, mouse_y):
    """Start a new game when player clicks button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        game_settings.intialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ship()
        scoreboard.prep_bullet()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(game_settings, screen, aliens, ship)
        ship.center_ship()


def update_screen(game_settings, screen, my_ship, aliens, bullets,
                  play_button, stats, score):
    """Updated the screen"""
    screen.fill(game_settings.bg_colour)
    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # My ship and alien on screen
    my_ship.blitme()
    aliens.draw(screen)
    # Draw the score
    score.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()
    # Make the most recently drawn screen visible
    pygame.display.flip()


def fire_bullets(bullets, game_settings, screen, ship):
    """Fire shells when spacebar is pressed """
    if len(bullets) < game_settings.amo:
        new_bullet = Bullets(game_settings, screen, ship)
        bullets.add(new_bullet)


def used_bullets(bullet, bullets):
    """Get rid of bullets that have dissapeared from screen"""
    if bullet.rect.bottom <= 0:
        bullets.remove()


def remove_aliens_and_bullets(bullets, aliens, stats, game_settings,
                              scoreboard):
    """
    Check for any bullets that have hit aliens.
    If yes then get rid of both alien and bullet
    """
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points*len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)


def repopulate(aliens, bullets, game_settings, screen, ship, scoreboard, stats):
    """ If the entire fleet is destroyed start new level and re-populate"""
    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, create new fleet
        bullets.empty()
        game_settings.increase_speed()

        # Increase level
        stats.level += 1
        scoreboard.prep_level()


        create_fleet(game_settings, screen, aliens, ship)


def update_bullets(bullets, aliens, game_settings, screen, ship, stats,
                   scoreboard):
    """
    Update the position of bullets and get rid old ones
    Repopulate alien fleet
    """
    for bullet in bullets.copy():
        used_bullets(bullet, bullets)
    remove_aliens_and_bullets(bullets, aliens, stats, game_settings, scoreboard)
    repopulate(aliens, bullets, game_settings, screen, ship, scoreboard, stats)



def get_number_of_aliens(game_settings, alien_width):
    """Total number of aliens we can fit across screen"""
    available_space = game_settings.screen_width - 2 * alien_width
    number_of_aliens = int(available_space / (2 * alien_width))
    return number_of_aliens


def available_space_x(game_settings, alien_height, ship_height):
    """The amount of  free screen space along the x-axis"""
    available_space = (game_settings.screen_height - (3 * alien_height) -
                       ship_height)
    return available_space


def rows_number(available_space, alien_height):
    """How many rows we want a fleet of aliens to take up"""
    number_of_rows = int(available_space / (2 * alien_height))
    return number_of_rows


def get_number_of_rows(game_settings, alien_height, ship_height):
    """Determine the number of rows aliens can take up"""
    available_space = available_space_x(game_settings, alien_height,
                                        ship_height)
    number_of_rows = rows_number(available_space, alien_height)
    return number_of_rows


def alien_x(alien, alien_number):
    """Creates a fleet of aliens across the screen"""
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x


def alien_y(alien, row_number):
    """Creates a fleet of aliens along the y-axis/ column"""
    alien.rect.y = alien.rect.height + alien.rect.height*row_number


def create_aliens(game_settings, screen, aliens, alien_number, row_number):
    """Create row and column of a fleet of aliens """
    # Create an alien and place it in a row
    alien = Aliens(game_settings, screen)
    alien_x(alien, alien_number)
    alien_y(alien, row_number)
    aliens.add(alien)


def create_fleet(game_settings, screen, aliens,  ship):
    """Create a fleet of aliens on the screen"""
    alien = Aliens(game_settings, screen)
    number_of_aliens_x = get_number_of_aliens(game_settings, alien.rect.width)
    number_of_rows = get_number_of_rows(game_settings, ship.rect.height,
                                        alien.rect.height)

    # Create the first row of aliens
    for row_number in range(number_of_rows):
        for alien_number in range(number_of_aliens_x):
            create_aliens(game_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(game_settings, aliens):
    """Respond if aliens have reached the edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    """Drop entire fleet and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def ship_hit(stats, aliens, bullets, game_settings, screen, ship, scoreboard):
    """Respond to ship being hit"""
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1
        # Update scoreboard
        scoreboard.prep_ship()
        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        # create a new fleet and center the ship
        create_fleet(game_settings, screen, aliens, ship)
        ship.center_ship()
        ship.ground_ship()
        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(stats, aliens, bullets, game_settings, screen, ship,
                        scoreboard):
    """Check if any aliens have hit the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat the same way as if a ship got hit
            ship_hit(stats, aliens, bullets, game_settings, screen, ship,
                     scoreboard)
            break


def update_aliens(game_settings, aliens, ship, stats, bullets, screen,
                  scoreboard):
    """Update alien position"""
    check_fleet_edges(game_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, aliens, bullets, game_settings, screen, ship,
                 scoreboard)
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(stats, aliens, bullets, game_settings, screen, ship,
                        scoreboard)


def check_high_score(stats, scoreboard):
    """Check to see if theres a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


