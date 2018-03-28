import pygame
from setting import Settings
from ship import Ship
import game_functionsR as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
from pygame.mixer import music


def run_game():
    """初始化游戏并创建一个屏幕对象"""
    #pygame.mixer.get_init()
    pygame.init()
    pygame.mixer.pre_init(22050, 16, 2, 4096)
    pygame.mixer.set_num_channels(5)
    pygame.mixer.music.load(gf.load_file("He's_a_Pirate.ogg"))
    pygame.mixer.music.play(-1)

    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    #创建一艘飞船
    ship = Ship(screen, ai_settings)
    #创建一个子弹编组
    bullets = Group()
    #创建外星人编组
    aliens = Group()
    gf.creat_fleet(ai_settings, screen, aliens, ship)
    #创建外星人实例
    #alien = Alien(ai_settings, screen)
    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    #创建按钮实例
    play_button = Button(ai_settings, screen, "Play")
    #创建计分牌
    sb = ScoreBoard(ai_settings, screen, stats)

    #开始游戏主循环
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats,
                        play_button, aliens, sb)
        # 游戏非活动状态时可以调节音量
        gf.set_volume(ai_settings, sb)

        if stats.game_active:
            ship.up_date()
            #每次循环都重绘屏幕
            # screen.fill(ai_settings.bg_color)
            # ship.blitme()

            #bullets.update()

            #删除以消失的子弹
            #for bullet in bullets.copy():
            #if bullet.rect.bottom <= 0:
            #bullets.remove(bullet)
            gf.update_bullet(ai_settings, screen, bullets, aliens, ship,
                             stats, sb)
            #print(len(bullets))
            #让最近绘制的屏幕可
            # pygame.display.flip()
            gf.update_aliens(ai_settings,screen, aliens, ship,
                             bullets, stats, sb)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens,
                         stats, play_button, sb)

run_game()
