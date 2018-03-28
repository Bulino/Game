import pygame.font
from pygame.sprite import Group

from ship import Ship

class ScoreBoard():
    """创建计分牌"""

    def __init__(self, ai_settings, screen, stats):
        """初始化计分牌属性"""
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        #最高得分不能重置

        #显示得分信息时的字体设置
        self.score_color = (30, 30, 30)
        self.sound_color = (60, 210 , 232)
        self.font = pygame.font.SysFont(None, 48)

        # #准备初始得分图像
        # self.prep_score()
        #
        # #准备初始最高得分图像
        # self.prep_high_score()
        #
        # #准备等级图像
        # self.prep_level()
        #
        # #显示剩余飞船
        # self.prep_ships()
        self.prep_images()

    def prep_score(self):
        """渲染得分图像并设置其位置于右上角"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = 'Score: ' + "{:,}".format(rounded_score)  #转换成字符
        self.score_image = self.font.render(score_str, True,
                                               self.score_color,
                                               self.ai_settings.bg_color)

        #得分放在右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """渲染最高得分图像并将其置于屏幕顶端居中"""
        #格式化最高得分
        rounded_high_score = int(round(self.stats.high_score, -1))
        high_score_str = 'High: ' + "{:,}".format(rounded_high_score)
        #渲染最高得分图像
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.score_color,
                                                 self.ai_settings.bg_color)

        #将得分放置于屏幕顶端居中
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.top = self.score_rect.top
        self.high_score_image_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        """渲染等级并置于得分信息之下"""
        #渲染等级信息
        level_str = 'Le: ' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.score_color,
                                            self.ai_settings.bg_color)
        #位于得分信息之下
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_rect.right
        self.level_image_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还剩多少飞船"""
        self.ships = Group()
        for ship_num in range(self.stats.ship_left):
            ship = Ship(self.screen, self.ai_settings)
            ship.rect.x = 10 + ship.rect.width * ship_num
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_sound(self):
        """显示音量设置"""
        #渲染音量显示标志
        sound_str = 'SV: ' + str(self.ai_settings.volume)
        self.sound_image = self.font.render(sound_str, True,
                                            self.sound_color,
                                            self.ai_settings.bg_color)
        #将其放置于等级标签之下
        self.sound_rect = self.sound_image.get_rect()
        self.sound_rect.right = self.score_rect.right
        self.sound_rect.top = self.level_image_rect.bottom + 10

    def prep_images(self):
        """绘制所有状态栏"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_sound()

    def show_score(self):
        """显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.screen.blit(self.sound_image, self.sound_rect)
        self.ships.draw(self.screen)
