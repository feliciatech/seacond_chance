import pygame

from pygame.sprite import Sprite


class Obstacle(Sprite):
    """A class to represent a single obstacle in the fleet."""

    def __init__(self, ai_game):
        """Initialize the obstacle and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the obstacle image and set its rect attribute.
        self.image = pygame.image.load('images/obstacle.bmp')
        self.rect = self.image.get_rect()

        # Start each new obstacle near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the obstacle's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if obstacle is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the obstacle right or left."""
        self.x += self.settings.obstacle_speed * self.settings.fleet_direction
        self.rect.x = self.x