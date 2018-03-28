import pygame
from pygame.sprite import Sprite
import game_functionsR as gf


class Ship(Sprite):  #记得继承父类
    """描述飞船"""
    def __init__(self, screen, ai_settings):
        """Initialnize the ship and give a default station."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        """加载飞船图像并获取外接矩形."""
        self.image = pygame.image.load(gf.load_file('ship.bmp'))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx      #把屏幕的值赋给图像
        self.rect.bottom = self.screen_rect.bottom

        #在飞船的属性中存储小数值
        self.center = float(self.rect.centerx)

        #移动标志
        self.move_right = False
        self.move_left = False

    def up_date(self):
        """根据标志移动飞船，调整位置"""
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.move_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        #根据self.center更新rect对象
        self.rect.centerx = self.center  # 只存储整数部分，但显示影响不大

    def blitme(self):
        """在制定位置绘制飞船."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship"""
        self.center = self.screen_rect.centerx
