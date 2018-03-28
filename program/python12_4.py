import sys, pygame

#初始化游戏设置和屏幕，打印按键事件
def run_key():
    """主程序"""
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Test Printkey")

    #设置背景颜色
    bg_color = (230,230, 255)

    #响应用户输入
    while True:

        """监视键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                print(event.key)

        #循环时重绘屏幕
        screen.fill(bg_color)

        #让最近的屏幕可见
        pygame.display.flip()

run_key()