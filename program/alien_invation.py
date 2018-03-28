# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, pygame

from setting import Settings
from ship import Ship

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    alien_settings = Settings()
    #screen = pygame.display.set_mode((1200, 800))
    screen = pygame.display.set_mode((alien_settings.screen_width,
                                     alien_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建一艘飞船
    ship = Ship(screen)

    #设置背景色
    #bg_color = (230, 230, 230)

    #开始游戏主循环
    while True:

        #监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #每次循环时都重绘屏幕
        #screen.fill(bg_color)
        screen.fill(alien_settings.bg_color)
        ship.blitme()               #注意位置

        #让最近绘制的屏幕可见
        pygame.display.flip()

run_game()