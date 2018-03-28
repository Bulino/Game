import game_functionsR as gf

class Settings():
    """存储《外星人入侵》中所有设置的类"""

    def __init__(self):
        """Initialnize the settings"""
        #Set up the screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230,230)

        # 飞船的设置
        # self.ship_speed_factor = 1.5
        self.ship_limit = 3

        #子弹的设置
        # self.bullet_speed_factor = 7
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3

        #外星人的设置
        # self.aliens_speed_factor = 5
        self.fleet_drop_speed = 20
        #用数字表示外星人移动方向更方便计算
        # self.fleet_direction = 1

        #设置加快游戏的节奏
        self.speed_scale = 1.1

        #设置外星人分数的增加
        self.score_scale = 1.5

        #设置存储最高分的文件名
        self.file_name = 'high_score.json'

        #设置起始音量
        self.volume = 30
        self.u_volume = False
        self.d_volume = False

        #音乐文件的设置
        self.fire_name = gf.load_file('fire.wav')
        self.colli_name = gf.load_file('collision.wav')

        self.initialize_dynamic_settings()  #勿忘用方法让属性返回

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的量"""
        self.ship_speed_factor = 3
        self.aliens_speed_factor = 5
        self.bullet_speed_factor = 15
        self.aliens_point = 50
        #设置移动标志
        self.fleet_direction = 1

    def increase_speed(self):
        """体高速度设置"""
        self.ship_speed_factor *= self.speed_scale
        self.aliens_speed_factor *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale
        self.aliens_point = int(self.score_scale * self.aliens_point)
        # print(self.aliens_point)
