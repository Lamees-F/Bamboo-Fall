import pygame

from pygame.sprite import Group
from settings import Settings
from game_stat import GameStats
from button import Button
from panda import Panda
from scoreboard import ScoreBoard
import game_function as gf
from pygame import mixer

def run_game():
    pygame.init()
    bf_settings = Settings()
    screen = pygame.display.set_mode(
        (bf_settings.screen_width, bf_settings.screen_height))
    pygame.display.set_caption("Bamboo Fall")

    mixer.music.load('happy-cave-6095.mp3')
    mixer.music.play(-1)
    image = pygame.image.load('image/panda0.jpg')
    pygame.display.set_icon(image)
    play_button = Button(bf_settings, screen, "play")

    stats = GameStats(bf_settings)
    sb = ScoreBoard(bf_settings, screen, stats)
    panda = Panda(bf_settings, screen)

    bullets = Group()
    bamboos = Group()

    gf.create_fleet(bf_settings, screen, panda, bamboos)


    while True:
        gf.check_events(bf_settings, screen, stats, sb, play_button, panda,
                        bamboos, bullets)
        if stats.game_active:
            panda.update()
            gf.update_bullets(bf_settings, screen, stats, sb, panda, bamboos, bullets)
            gf.update_bamboos(bf_settings, stats, screen, panda, bamboos, bullets)
        gf.update_screen(bf_settings, screen, stats, sb, panda, bamboos,
                         bullets, play_button)


run_game()