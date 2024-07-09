class Settings:
    """A class to store all settings for Seacond Chance."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Diver settings
        self.diver_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Obstacle settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the obstacle point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.diver_speed = 1.5
        self.bullet_speed = 2.5
        self.obstacle_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring settings
        self.obstacle_points = 50

    def increase_speed(self):
        """Increase speed settings and obstacle point values."""
        self.diver_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.obstacle_speed *= self.speedup_scale

        self.obstacle_points = int(self.obstacle_points * self.score_scale)