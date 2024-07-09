import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from diver import Diver
from bullet import Bullet
from obstacle import Obstacle

import random
import math


class SeacondChance:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.settings.create_waves()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Seacond Chance")
        
    
        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.diver = Diver(self)
        self.bullets = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        self._create_fleet()

        # Start Seacond Chance in an inactive state.
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")

   
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.diver.update()
                self._update_bullets()
                self._update_obstacles()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_divers()
            self.game_active = True

            # Get rid of any remaining bullets and obstacles.
            self.bullets.empty()
            self.obstacles.empty()

            # Create a new fleet and center the diver.
            self._create_fleet()
            self.diver.center_diver()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.diver.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.diver.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.diver.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.diver.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_obstacle_collisions()

    def _check_bullet_obstacle_collisions(self):
        """Respond to bullet-obstacle collisions."""
        # Remove any bullets and obstacles that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.obstacles, True, True)

        if collisions:
            for obstacles in collisions.values():
                self.stats.score += self.settings.obstacle_points * len(obstacles)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.obstacles:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _diver_hit(self):
        """Respond to the diver being hit by an obstacle."""
        if self.stats.divers_left > 0:
            # Decrement divers_left, and update scoreboard.
            self.stats.divers_left -= 1
            self.sb.prep_divers()

            # Get rid of any remaining bullets and obstacles.
            self.bullets.empty()
            self.obstacles.empty()

            # Create a new fleet and center the diver.
            self._create_fleet()
            self.diver.center_diver()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_obstacles(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.obstacles.update()

        # Look for obstacle-diver collisions.
        if pygame.sprite.spritecollideany(self.diver, self.obstacles):
            self._diver_hit()

        # Look for obstacles hitting the bottom of the screen.
        self._check_obstacles_bottom()

    def _check_obstacles_bottom(self):
        """Check if any obstacles have reached the bottom of the screen."""
        for obstacle in self.obstacles.sprites():
            if obstacle.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the diver got hit.
                self._diver_hit()
                break

    def _create_fleet(self):
        """Create the fleet of obstacles."""
        # Create an obstacle and keep adding obstacles until there's no room left.
        # Spacing between obstacles is one obstacle width and one obstacle height.
        obstacle = Obstacle(self)
        
        obstacle_width, obstacle_height = obstacle.rect.size

        current_x, current_y = obstacle_width, obstacle_height
        while current_y < (self.settings.screen_height - 3 * obstacle_height):
            while current_x < (self.settings.screen_width - 2 * obstacle_width):
                self._create_obstacle(current_x, current_y)
                current_x += 2 * obstacle_width

            # Finished a row; reset x value, and increment y value.
            current_x = obstacle_width
            current_y += 2 * obstacle_height
        self.obstacles.add(obstacle)

    def _create_obstacle(self, x_position, y_position):
        """Create an obstacle and place it in the fleet."""
        new_obstacle = Obstacle(self)
        new_obstacle.x = x_position
        new_obstacle.rect.x = x_position
        new_obstacle.rect.y = y_position
        self.obstacles.add(new_obstacle)

    def _check_fleet_edges(self):
        """Respond appropriately if any obstacles have reached an edge."""
        for obstacle in self.obstacles.sprites():
            if obstacle.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for obstacle in self.obstacles.sprites():
            obstacle.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Draw wave pattern for background
        self.screen.fill(self.settings.bg_color)
        self.settings.draw_waves(self.screen)
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.diver.blitme()
        self.obstacles.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()
    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = SeacondChance()
    ai.run_game()