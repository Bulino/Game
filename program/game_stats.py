import json


class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # #游戏刚启动时处于活动状态
        # self.game_avtive = True
        #让游戏一直处于非活动状态
        self.game_active = False
        #最高得分不能被重置
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        #读取最高分
        try:
            with open(self.ai_settings.file_name) as f_obj:
                self.high_score = int(json.load(f_obj))
        except FileNotFoundError:
            print("This file dosen't exit.")
