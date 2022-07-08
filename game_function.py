import sys
from time import sleep
from pygame import mixer
import pygame
from bullet import Bullet
from bamboo import Bamboo


def check_keydown_events(event, bf_settings, screen, panda, bullets):
    if event.key == pygame.K_RIGHT:
        panda.moving_right = True
    elif event.key == pygame.K_LEFT:
        panda.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bf_settings, screen, panda, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(bf_settings, screen, panda, bullets):
    if len(bullets) < bf_settings.bullets_allowed:
            new_bullet = Bullet(bf_settings, screen, panda)
            bullets.add(new_bullet)

def check_keyup_events(event,panda):
    if event.key == pygame.K_RIGHT:
        panda.moving_right = False
    elif event.key == pygame.K_LEFT:
        panda.moving_left = False

def check_events(bf_settings,screen, stats, sb, play_button, panda, bamboos,
                 bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, bf_settings, screen, panda, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, panda)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(bf_settings, screen, stats, sb, play_button, panda,
                              bamboos, bullets, mouse_x, mouse_y)

def check_play_button(bf_settings, screen, stats, sb,  play_button, panda,
                      bamboos, bullets, mouse_x, mouse_y):
    play_sound = mixer.Sound('start-13691.mp3')
    play_sound.play()
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        bf_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        bamboos.empty()
        bullets.empty()

        create_fleet(bf_settings, screen, panda, bamboos)
        panda.center_panda()

def update_screen(bf_settings, screen, stats, sb, panda, bamboos, bullets,
                  play_button):
    screen.fill(bf_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    panda.blitme()
    bamboos.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(bf_settings, screen, stats, sb, panda, bamboos, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_bamboo_collisons(bf_settings, screen, stats, sb, panda,
                                  bamboos, bullets)

def check_bullet_bamboo_collisons(bf_settings, screen, stats, sb, panda,
                                  bamboos, bullets):
    collisions = pygame.sprite.groupcollide(bullets, bamboos, True, True)
    if collisions:
        for bamboos in collisions.values():
            shot_sound=mixer.Sound('shot.mp3')
            shot_sound.play()
            stats.score += bf_settings.bamboo_points * len(bamboos)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(bamboos) == 0:
        bullets.empty()
        bf_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(bf_settings, screen, panda, bamboos)

def get_number_bamboos_x(bf_settings, bamboo_width):
    """Determine the # of bamboos in the first row"""
    avail_space_x = bf_settings.screen_width - 4 * bamboo_width
    number_bamboos_x = int(avail_space_x / bamboo_width)
    return number_bamboos_x

def get_number_row(bf_settings, panda_height, bamboo_height):
    avail_space_y = (bf_settings.screen_height -
                     ( bamboo_height)-panda_height)
    number_rows = int(avail_space_y / (2*bamboo_height))
    return number_rows

def create_bamboo(bf_settings, screen, bamboos, bamboo_number,
                  row_number):
    bamboo = Bamboo(bf_settings, screen)
    bamboo_width = bamboo.rect.width
    bamboo.x = bamboo_width + bamboo_width * bamboo_number  # times 1.25 for spacing
    bamboo.rect.x = bamboo.x
    bamboo.rect.y = bamboo.rect.height + 2 * bamboo.rect.height * row_number
    bamboos.add(bamboo)

def create_fleet(bf_settings, screen, panda,  bamboos):
    bamboo = Bamboo(bf_settings, screen)
    number_bamboos_x = get_number_bamboos_x(bf_settings, bamboo.rect.width)
    number_row = get_number_row(bf_settings, panda.rect.height,
                              bamboo.rect.height)
    for row_number in range(number_row):
        for bamboo_number in range(number_bamboos_x):
            create_bamboo(bf_settings, screen, bamboos, bamboo_number,
                          row_number)

def check_fleet_edges(bf_settings, bamboos):
    for bamboo in bamboos.sprites():
        if bamboo.check_edges():
            change_fleet_direction(bf_settings, bamboos)
            break

def change_fleet_direction(bf_settings, bamboos):
    for bamboo in bamboos.sprites():
        bamboo.rect.y += bf_settings.fleet_drop_speed
    bf_settings.fleet_direction *= -1

def panda_hit(bf_settings,stats, screen, panda, bamboos, bullets):
    if stats.panda_left > 0 :
        stats.panda_left -= 1

        bamboos.empty()
        bullets.empty()

        create_fleet(bf_settings, screen, panda, bamboos)
        panda.center_panda()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_bamboo_bottom(bf_settings, stats, screen, panda, bamboos, bullets):
    screen_rect = screen.get_rect()
    for bamboo in bamboos.sprites():
        if bamboo.rect.bottom >= screen_rect.bottom:
            panda_hit(bf_settings, stats, screen, panda, bamboos, bullets)
            break

def update_bamboos(bf_settings, stats,screen, panda, bamboos, bullets):
    check_fleet_edges(bf_settings,bamboos)
    bamboos.update()

    if pygame.sprite.spritecollideany(panda, bamboos):
        panda_hit(bf_settings, stats, screen, panda, bamboos, bullets)

    check_bamboo_bottom(bf_settings, stats, screen, panda, bamboos, bullets)

def check_high_score(stats, sb):
    if stats.score > stats.high_score :
        stats.high_score = stats.score
        sb.prep_high_score()
