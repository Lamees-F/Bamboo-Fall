#from pygame.sprite import Group
import pygame.font

#from panda import Panda


class ScoreBoard():

    def __init__(self, bf_settings, screen, stats):

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bf_settings = bf_settings
        self.stats = stats

        self.text_color = 30, 30, 30
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        #self.prep_pandas()

    """def prep_pandas(self):
        self.pandas = Group()
        for panda_number in range(self.stats.panda_left):
            panda = Panda(self.bf_settings, self.screen)
            panda.rect.x = 10 + panda_number * panda.rect.width
            panda.rect.y = 10
            self.pandas.add(panda)"""

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level),
                              True, self.text_color,self.bf_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                    self.text_color, self.bf_settings.bg_color)
        self.high_score_rect =self.high_score_image.get_rect()
        self.high_score_rect.centerx =self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self):
        round_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(round_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.bf_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #self.pandas.draw(self.screen)
