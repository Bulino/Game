import pygame.font


class Button():
    """表示按钮的类"""
    def __init__(self, ai_settings, screen, msg):
        """Initialnize the button attributes"""
        self.ai_settings = ai_settings
        self.screen = screen
        #self.msg = msg
        self.screen_rect = screen.get_rect()

        #设置按钮属性
        self.width, self.height = 200, 50
        self.button_color = (60, 60, 60)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #创建按钮的rect对象并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #按钮的标签只需创建一次
        self.prep_msg(msg)


    def prep_msg(self, msg):
        """将msg渲染为图像并将其居中"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        """绘制按钮及文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)