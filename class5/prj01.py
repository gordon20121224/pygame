######################載入套件######################
import pygame
import sys


######################物件類別######################
class Player:
    def __init__(self, x, y, width, height, color):
        """
        初始化主角物件
        x, y: 主角的左上角座標
        width, height: 主角的寬度和高度
        color: 主角的顏色
        """
        self.rect = pygame.Rect(x, y, width, height)  # 主角的矩形區域
        self.color = color  # 主角的顏色

    def draw(self, display_area):
        """
        繪製主角
        display_area: 要繪製的螢幕物件
        """
        pygame.draw.rect(display_area, self.color, self.rect)  # 繪製主角方塊


######################初始化設定######################
pygame.init()  # 初始化pygame
FPS = pygame.time.Clock()  # 設定FPS物件

######################遊戲視窗設定######################
bg_x = 400  # 視窗寬度
bg_y = 600  # 視窗高度
bg_size = (bg_x, bg_y)  # 視窗大小
pygame.display.set_caption("Doodle Jump")  # 設定視窗標題
screen = pygame.display.set_mode(bg_size)  # 設定視窗大小

######################主角設定######################
player_width = 30  # 主角寬度
player_height = 30  # 主角高度
player_color = (0, 255, 0)  # 主角顏色(綠色)
# 設定主角初始位置在畫面中央偏下
player = Player(
    (bg_x - player_width) // 2,  # X座標置中
    bg_y - 200,  # Y座標在下方200像素處
    player_width,
    player_height,
    player_color,
)

######################主程式######################
while True:  # 主程式迴圈
    FPS.tick(60)  # 設定FPS為60
    screen.fill((0, 0, 0))  # 清空畫面，設定為黑色背景

    for event in pygame.event.get():  # 事件處理
        if event.type == pygame.QUIT:  # 如果按下關閉視窗
            pygame.quit()  # 關閉pygame
            sys.exit()  # 結束程式

    player.draw(screen)  # 繪製主角
    pygame.display.update()  # 更新畫面
