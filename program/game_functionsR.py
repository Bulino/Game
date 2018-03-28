import sys, pygame
from bullet import Bullet
from alien import Alien
from time import  sleep
import json
import os
from pygame.mixer import Sound
from pygame.mixer import music


def check_keydown(event, ai_settings, screen, ship, bullets,
                  aliens, stats, sb):
    """响应按键"""
    if event.key == pygame.K_p:
        # stats.game_active =True
        start_game(ai_settings, screen, stats, aliens, ship, bullets, sb)

    elif event.key == pygame.K_LEFT:
        ship.move_left = True

    elif event.key == pygame.K_RIGHT:
        ship.move_right = True

    elif event.key ==pygame.K_UP:
        ai_settings.u_volume = True

    elif event.key == pygame.K_DOWN:
        ai_settings.d_volume = True

    elif event.key == pygame.K_SPACE:
        #创建一颗子弹并将其加入编组中
        # if len(bullets) < ai_settings.bullet_allowed:
        #
        #     new_bullet = Bullet(ai_settings, screen, ship)
        #     bullets.add(new_bullet)##
        """响应按键"""
        if stats.game_active:  #修复游戏未开始时创建并发射子弹
            fire_bullet(ai_settings,screen,ship, bullets)

    elif event.key == pygame.K_q:
        #退出前写入当前最高分，以免丢失
        file_name = ai_settings.file_name
        with open(file_name, 'w') as f_obj:
            json.dump(str(stats.high_score) + '\n', f_obj) #txt格式，只能写入字符
        #停止背景音乐播放
        pygame.mixer.music.stop()

        sys.exit()



def check_keyup(event, ship, ai_settings):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.move_right = False

    elif event.key == pygame.K_LEFT:
        ship.move_left = False

    elif event.key == pygame.K_UP:
        ai_settings.u_volume = False

    elif event.key == pygame.K_DOWN:
        ai_settings.d_volume = False


def check_events(ai_settings, screen ,ship, bullets, stats, play_button,
                 aliens, sb):#重构时倒入变量ship
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#别忘了加冒号
            pygame.mixer.music.stop()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_RIGHT:
            #     ship.move_right = True
            # elif event.key == pygame.K_LEFT:
            #     ship.move_left = True
            check_keydown(event, ai_settings, screen, ship,
                          bullets, aliens, stats, sb)

        elif event.type == pygame.KEYUP:
            # if event.key == pygame.K_RIGHT:
            #     #ship.rect.centerx += 1
            #     ship.move_right = False
            # elif event.key == pygame.K_LEFT:
            #     ship.move_left = False
            check_keyup(event, ship, ai_settings)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,stats, play_button, mouse_x,
                              mouse_y, aliens, bullets, screen, ship, sb)


def start_game(ai_settings, screen, stats, aliens, ship, bullets, sb):
    """检查play按钮和q键时开始游戏"""
    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True

    # 清空外星人和子弹列表
    aliens.empty()
    bullets.empty()
    # #重置记分牌图像
    # sb.prep_score()
    # sb.prep_high_score()
    # sb.prep_level()
    # #描述飞船数
    # sb.prep_ships()

    # 创建一群新的外星人并将飞船居中
    sb.prep_images()

    creat_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()


def set_volume(ai_settings, sb):
    """音量设置"""
    if ai_settings.u_volume:
        ai_settings.volume += 10
        if ai_settings.volume > 100:
            ai_settings.volume = 30

    if ai_settings.d_volume:
        ai_settings.volume -= 10
        if ai_settings.volume < 0:
            ai_settings.volume = 30
    pygame.mixer.music.set_volume(ai_settings.volume/100.0)

    sb.prep_sound()

def check_play_button(ai_settings, stats, play_button, mouse_x, mouse_y,
                      aliens, bullets, screen, ship, sb):
    """单击play按钮时开始游戏"""
    #检查按钮动作
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_click and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #开始游戏
        start_game(ai_settings, screen, stats, aliens, ship, bullets, sb)
        #隐藏光标
        pygame.mouse.set_visible(False)


def noaliens_creat(ai_settings, screen, aliens,
                   bullets, stats, sb, ship):
    """外星人全被消灭时，创建新的外星人并增加等级"""
    # 外星人全被消灭时就创建外星人
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()

        creat_fleet(ai_settings, screen, aliens, ship)

def collision(ai_settings, screen, ship, bullets, aliens, stats, sb):
    """检查碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    #碰撞后记分
    if collisions:
        #发出声音
        play_sound(ai_settings.colli_name, 1500)

        for alien in collisions.values():
            #记分
            stats.score += ai_settings.aliens_point * len(alien)
            #显示记分牌
            sb.prep_score()
        #检查最高得分
        check_high_score(stats, sb)

    noaliens_creat(ai_settings,screen, aliens, bullets, stats, sb, ship)


def update_bullet(ai_setings, screen, bullets, aliens, ship, stats, sb):
    """更新子弹位置并消除以消失的子弹"""
    #更新子弹位置
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullet.remove(bullets)
    #检查是否有子弹击中外形人
    #如果是这样，就删除相应的子弹和外星人
    # collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # if len(aliens) == 0:
    #     bullets.empty()
    #     creat_fleet(ai_settings, screen, aliens, ship)
    collision(ai_setings, screen, ship, bullets, aliens, stats, sb)


def fire_bullet(ai_settings, screen, ship, bullets):
    """若果没有到达限制就发射一颗子弹"""
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        #子弹发射的声音
        play_sound(ai_settings.fire_name, 1000)

def get_aliens_num_x(ai_settings, alien_width):
    """计算每行可容纳多少外星人"""
    available_aliens_x = ai_settings.screen_width - 2 * alien_width
    num_aliens = int(available_aliens_x / (2 * alien_width))
    return num_aliens


def get_aliens_num_y(ai_settings, ship_height, alien_height):
    """屏幕可容纳多少行外星人"""
    available_aliens_y = (ai_settings.screen_height -
                          ship_height - 3 * alien_height)
    num_aliens_row = int(available_aliens_y / (2 * alien_height))
    return num_aliens_row


def creat_alien(ai_settings, screen, aliens, alien_num, row_num):
    """创建一个外形人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_num #隔一个外星人宽度
    alien.y = alien_height + 2 * alien_height * row_num #隔一个外星人高度
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)


def creat_fleet(ai_settings, screen, aliens, ship):
    """创建多个外星人"""
    #创建一个外星人，并计算一行能容纳多少外形人
    #外星人间距为外星人宽度
    # available_space_x = ai_settings.screen_width - 2 * alien_width
    # alien_width = alien.rect.width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_aliens_num_x(ai_settings, alien.rect.width)
    number_aliens_y = get_aliens_num_y(ai_settings, ship.rect.height,
                                       alien.rect.height)
    #创建第一行外星人
    # for alien_num in range(number_aliens_x):
    #     #创建一个外星人并将其加入当前行
    #     # alien = Alien(ai_settings, screen)
    #     # alien.x = alien_width + 2 * alien_width * alien_num
    #     # alien.rect.x = alien.x
    #     # aliens.add(alien)
    #     creat_alien(ai_settings, screen, aliens, alien_num)
    #创建满屏外星人群
    for row_num in range(number_aliens_y):
        for alien_num in range(number_aliens_x):
            creat_alien(ai_settings, screen, aliens, alien_num, row_num)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达屏幕边缘时采取响应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break  #跳出循环不再检查


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人向下移并改变移动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, screen, aliens,
                        stats, bullets, ship, sb):
    """检查是否有外星人到达屏幕低端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, ship,
                     aliens, bullets, stats, sb)
            break


def update_aliens(ai_settings, screen, aliens,
                  ship, bullets, stats, sb):
    # """更新外星人群中所有外星人的位置"""
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        # print("Ship hit1")
        ship_hit(ai_settings, screen, ship, aliens,
                 bullets, stats, sb)

    check_aliens_bottom(ai_settings, screen, aliens,
                        stats, bullets, ship, sb)


def ship_hit(ai_settings, screen, ship,  aliens,
             bullets, stats, sb):
    """外星人碰到飞船时采取行动"""
    if stats.ship_left > 0:
        #飞船数减1
        stats.ship_left -= 1
        #更新飞船显示数
        sb.prep_ships()

        #清空外星人和子弹
        bullets.empty()
        aliens.empty()

        #创建一群新的外星人，并将飞船居中
        creat_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        #Stop for a moment
        sleep(1.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """检查是否诞生了最高得分"""
    if stats.high_score < stats.score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, ship, bullets,
                  aliens, stats, play_button, sb):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # alien.blitme()
    aliens.draw(screen)
    #显示得分
    sb.show_score()
    #游戏处于非活动状态，绘制按钮
    if not stats.game_active:
        play_button.draw_button()
    #让最近的屏幕可见
    pygame.display.flip()


def load_file(filename):
    """加载图像和音乐文件路劲"""
    curren_dir = os.getcwd()
    current_path = os.path.dirname(curren_dir)
    name = filename.split()[-1]
    if name == 'bmp':
        path = os.path.join(current_path, 'images', filename)
    else:
        path = os.path.join(current_path, 'sound', filename)
    return path


def play_sound(soundfile_name, maxtime):
    """加载发射子弹和碰撞的声音"""
    path = load_file(filename)
    sound = pygame.mixer.Sound(path)
    sound.play(maxtime = maxtime)

