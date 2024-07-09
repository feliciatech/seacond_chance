import pygame
from pygame.sprite import Sprite


class Diver(Sprite):
    """A class to manage the diver."""

    def __init__(self, ai_game):
        """Initialize the diver and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the diver image and get its rect.
        self.image = pygame.image.load('images/diver.bmp')
        self.image = pygame.transform.smoothscale(self.image, (100, 80))

        self.rect = self.image.get_rect()

        # Start each new diver at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the diver's exact horizontal position.
        self.x = float(self.rect.x)

        # Movement flags; start with a diver that's not moving.
        self.moving_right = False
        self.moving_left = False

    def center_diver(self):
        """Center the diver on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Update the diver's position based on movement flags."""
        # Update the diver's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.diver_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.diver_speed
            
        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the diver at its current location."""
        self.screen.blit(self.image, self.rect)