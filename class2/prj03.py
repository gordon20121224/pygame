######################載入套件######################
import pygame
import sys
import random


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
bricks_row = 9
bricks_column = 11  # 磚塊行數
bricks = []  # 磚塊列表
brick_w = 58
brick_h = 16  # 磚塊寬高
bricks_gap = 2  # 磚塊間距
for col in range(bricks_column):  # 磚塊行數
    for row in range(bricks_row):  # 磚塊列數
        x = col * (brick_w + bricks_gap) + 70  # 磚塊X座標
        y = row * (brick_h + bricks_gap) + 60  # 磚塊Y座標
        color = (
            random.randint(30, 255),
            random.randint(30, 255),
            random.randint(30, 255),
        )  # 隨機顏色
        brick = Brick(x, y, brick_w, brick_h, color)  # 磚塊物件
        bricks.append(brick)  # 將磚塊加入列表
######################顯示文字設定######################

######################底板設定######################
paddle_width = 100  # 底板寬度
paddle_height = 15  # 底板高度
paddle_color = (255, 255, 255)  # 底板顏色(白色)
paddle = Brick(
    (bg_x - paddle_width) // 2, bg_y - 48, paddle_width, paddle_height, paddle_color
)  # 建立底板物件

######################滑鼠設定######################
pygame.mouse.set_visible(False)  # 隱藏滑鼠

######################球設定######################

######################遊戲結束設定######################

######################主程式######################
while True:  # 主程式迴圈
    for event in pygame.event.get():  # 事件處理
        if event.type == pygame.QUIT:  # 如果按下關閉視窗
            pygame.quit()  # 關閉pygame
            sys.exit()  # 結束程式

    # 取得滑鼠位置
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # 計算paddle位置
    mouse_x = mouse_x - paddle_width // 2
    # 確保paddle不會超出視窗範圍
    if mouse_x > bg_x - paddle_width:
        mouse_x = bg_x - paddle_width
    elif mouse_x < 0:
        mouse_x = 0
    paddle.rect.x = mouse_x

    screen.fill((0, 0, 0))  # 清空畫面
    for brick in bricks:  # 繪製所有磚塊
        brick.draw(screen)  # 繪製磚塊
    paddle.draw(screen)  # 繪製底板
    pygame.display.update()  # 更新畫面
