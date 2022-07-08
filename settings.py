class Settings():

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        self.panda_limit = 0


        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.panda_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.bamboo_speed_factor = 0.5
        self.fleet_direction = 1
        self.bamboo_points = 50

    def increase_speed(self):
        self.panda_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.bamboo_speed_factor *= self.speedup_scale

        self.bamboo_points = int(self.bamboo_points * self.score_scale)
