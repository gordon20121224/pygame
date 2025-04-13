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
        # 加入移動相關的屬性
        self.velocity_y = 10  # 垂直速度，初始向上速度10像素
        self.gravity = 0.5  # 重力加速度，每幀增加0.5像素的下降速度

    def draw(self, display_area):
        """
        繪製主角
        display_area: 要繪製的螢幕物件
        """
        pygame.draw.rect(display_area, self.color, self.rect)  # 繪製主角方塊

    def move(self, bg_x):
        """
        處理主角的移動
        bg_x: 遊戲視窗寬度，用於處理穿牆效果
        """
        # 更新垂直位置
        self.rect.y -= self.velocity_y  # 根據速度更新Y座標
        self.velocity_y -= self.gravity  # 施加重力效果

        # 處理左右移動
        keys = pygame.key.get_pressed()  # 獲取鍵盤輸入狀態
        if keys[pygame.K_LEFT]:  # 按下左方向鍵
            self.rect.x -= 5  # 向左移動5像素
        if keys[pygame.K_RIGHT]:  # 按下右方向鍵
            self.rect.x += 5  # 向右移動5像素

        # 處理穿牆效果
        if self.rect.left > bg_x:  # 如果從右邊出去
            self.rect.right = 0  # 從左邊出現
        elif self.rect.right < 0:  # 如果從左邊出去
            self.rect.left = bg_x  # 從右邊出現


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

    # 更新主角位置
    player.move(bg_x)  # 處理主角的移動
    player.draw(screen)  # 繪製主角
    pygame.display.update()  # 更新畫面
