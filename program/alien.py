import  pygame
from pygame.sprite import Sprite
import game_functionsR as gf


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其属性"""
        super(Alien,self ).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人图像并设置其位置
        self.image = pygame.image.load(gf.load_file('alien.bmp'))
        self.rect = self.image.get_rect()

        #在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人准确位置
        self.x = float(self.rect.x)   #外星人的水平刻度

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """向右移动外星人"""
        self.x += (self.ai_settings.aliens_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人到屏幕边缘就反回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= screen_rect.left:
            return True
