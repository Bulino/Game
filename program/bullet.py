import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """对飞船发射的子弹管理的类"""

    def __init__(self, ai_settings, screen, ship):
        """飞船的所处位置创建子弹"""
        super(Bullet, self).__init__()
        self.screen = screen

        #在（0，0）处先定义子弹，再匹配其位置
        self.rect = pygame.Rect(0 ,0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #存储用小数表示的子弹位置
        self.y = float(self.rect.y) #子弹向上的位置变动是连续的，位置数据

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        #更新表示子弹位置的小数值
        self.y -= self.speed
        #更新表示子弹的rect值
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)

