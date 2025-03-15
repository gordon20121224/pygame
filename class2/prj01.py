######################載入套件######################
import pygame
import sys


######################物件類別######################
class Brick:
    def __init__(self, x, y, width, height, color):
        """
        初始化磚塊物件\n
        x, y: 磚塊的左上角座標\n
        width, height: 磚塊的寬度和高度\n
        color: 磚塊的顏色\n
        """
        self.rect = pygame.Rect(x, y, width, height)  # 磚塊的矩形區域
        self.color = color  # 磚塊的顏色
        self.hit = False  # 磚塊是否被擊中

    def draw(self, display_area):
        """
        繪製磚塊\n
        display_area: 要繪製的螢幕物件\n
        """
        if not self.hit:  # 如果磚塊沒有被擊中
            pygame.draw.rect(display_area, self.color, self.rect)


######################定義函式區######################

######################初始化設定######################
pygame.init()  # 初始化pygame
######################載入圖片######################

######################遊戲視窗設定######################
bg_x = 800  # 視窗寬度
bg_y = 600  # 視窗高度
bg_size = (bg_x, bg_y)  # 視窗大小
pygame.display.set_caption("打磚塊")  # 設定視窗標題
screen = pygame.display.set_mode(bg_size)  # 設定視窗大小
######################磚塊######################
brickA = Brick(100, 100, 50, 20, (255, 0, 0))  # 磚塊A
brickB = Brick(200, 100, 50, 20, (0, 255, 0))  # 磚塊B
######################顯示文字設定######################

######################底板設定######################

######################球設定######################

######################遊戲結束設定######################

######################主程式######################
while True:  # 主程式迴圈
    for event in pygame.event.get():  # 事件處理
        if event.type == pygame.QUIT:  # 如果按下關閉視窗
            pygame.quit()  # 關閉pygame
            sys.exit()  # 結束程式

    brickA.rect.width = 100  # 修改磚塊A的寬度
    brickA.rect.height = 100  # 修改磚塊A的高度
    brickA.draw(screen)  # 繪製磚塊A
    brickB.draw(screen)  # 繪製磚塊B
    pygame.display.update()  # 更新畫面
