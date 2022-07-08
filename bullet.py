import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, bf_settings, screen, panda):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, bf_settings.bullet_width,
                              bf_settings.bullet_height)
        self.rect.centerx = panda.rect.centerx
        self.rect.top = panda.rect.top

        self.y = float(self.rect.y)

        self.color = bf_settings.bullet_color
        self.speed_factor = bf_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)