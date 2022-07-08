class GameStats():

    def __init__(self, bf_settings):
        self.bf_settings = bf_settings
        self.reset_stats()

        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.panda_left = self.bf_settings.panda_limit
        self.score = 0
        self.game_active = False
        self.level = 1

