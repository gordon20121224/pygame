######################載入必要的套件######################
import pygame  # 載入 pygame 套件，用於遊戲開發
import sys  # 載入 sys 套件，用於系統相關功能


######################定義遊戲物件類別######################
class Platform:
    def __init__(self, x, y, width, height, color):
        """
        平台物件初始化
        參數說明：
        x, y: 平台的左上角座標位置
        width, height: 平台的寬度和高度
        color: 平台的顏色（RGB格式）
        """
        self.rect = pygame.Rect(x, y, width, height)  # 建立平台的碰撞範圍
        self.color = color  # 設定平台顏色

    def draw(self, display_area):
        """
        繪製平台到指定的顯示區域
        參數說明：
        display_area: pygame的顯示區域物件
        """
        pygame.draw.rect(display_area, self.color, self.rect)  # 繪製矩形平台


class Player:
    def __init__(self, x, y, width, height, color):
        """
        主角物件初始化
        參數說明：
        x, y: 主角的初始位置（左上角座標）
        width, height: 主角的寬度和高度
        color: 主角的顏色（RGB格式）
        """
        self.rect = pygame.Rect(x, y, width, height)  # 建立主角的碰撞範圍
        self.color = color  # 設定主角顏色
        self.velocity_y = 10  # 設定初始垂直速度（向上為正）
        self.gravity = 0.5  # 設定重力加速度
        self.is_falling = True  # 新增：用於追蹤主角是否正在下落

    def draw(self, display_area):
        """
        繪製主角到指定的顯示區域
        參數說明：
        display_area: pygame的顯示區域物件
        """
        pygame.draw.rect(display_area, self.color, self.rect)  # 繪製主角方塊

    def move(self, bg_x):
        """
        處理主角的移動邏輯
        參數說明：
        bg_x: 遊戲背景的寬度，用於處理穿牆效果
        """
        # 更新垂直位置
        self.rect.y -= self.velocity_y  # 根據當前速度更新垂直位置
        self.velocity_y -= self.gravity  # 加入重力影響
        self.is_falling = self.velocity_y < 0  # 更新下落狀態

        # 處理鍵盤左右移動
        keys = pygame.key.get_pressed()  # 獲取當前鍵盤按鍵狀態
        if keys[pygame.K_LEFT]:  # 如果按下左方向鍵
            self.rect.x -= 5  # 向左移動5像素
        if keys[pygame.K_RIGHT]:  # 如果按下右方向鍵
            self.rect.x += 5  # 向右移動5像素

        # 處理穿牆效果
        if self.rect.left > bg_x:  # 如果主角超出右邊界
            self.rect.right = 0  # 從左側重新出現
        elif self.rect.right < 0:  # 如果主角超出左邊界
            self.rect.left = bg_x  # 從右側重新出現

    def check_collision(self, platform):
        """
        檢測主角是否與平台發生碰撞
        參數說明：
        platform: 要檢查碰撞的平台物件
        回傳值：
        True: 發生有效碰撞（從上方碰觸平台）
        False: 未發生碰撞或無效碰撞
        """
        # 檢查是否符合所有碰撞條件
        if (
            self.is_falling  # 確認主角正在下落
            and self.rect.bottom >= platform.rect.top  # 主角底部碰到平台頂部
            and self.rect.bottom <= platform.rect.bottom  # 確保不是從下方碰撞
            and self.rect.right >= platform.rect.left  # 確認水平方向有重疊
            and self.rect.left <= platform.rect.right
        ):  # 確認水平方向有重疊

            # 碰撞處理
            self.rect.bottom = platform.rect.top  # 將主角位置調整到平台頂部
            self.velocity_y = 10  # 給予向上的反彈速度
            self.is_falling = False  # 更新下落狀態
            return True
        return False


######################遊戲初始化設定######################
pygame.init()  # 初始化 pygame
FPS = pygame.time.Clock()  # 建立 FPS 時鐘物件

######################遊戲視窗設定######################
bg_x = 400  # 設定視窗寬度
bg_y = 600  # 設定視窗高度
bg_size = (bg_x, bg_y)  # 設定視窗尺寸
screen = pygame.display.set_mode(bg_size)  # 建立遊戲視窗
pygame.display.set_caption("Doodle Jump")  # 設定視窗標題

######################建立遊戲物件######################
# 建立主角物件
player = Player(
    (bg_x - 30) // 2,  # X座標置中
    bg_y - 100,  # Y座標在下方100像素處
    30,  # 主角寬度
    30,  # 主角高度
    (0, 255, 0),  # 主角顏色（綠色）
)

# 建立平台物件
platform = Platform(
    (bg_x - 60) // 2,  # X座標置中
    bg_y - 70,  # Y座標在主角腳下
    60,  # 平台寬度
    10,  # 平台高度
    (255, 255, 255),  # 平台顏色（白色）
)

######################遊戲主迴圈######################
while True:
    FPS.tick(60)  # 控制遊戲更新頻率為60FPS
    screen.fill((0, 0, 0))  # 用黑色填充畫面背景

    # 事件處理
    for event in pygame.event.get():  # 取得所有事件
        if event.type == pygame.QUIT:  # 如果是關閉視窗事件
            pygame.quit()  # 關閉 pygame
            sys.exit()  # 結束程式

    # 更新遊戲狀態
    player.move(bg_x)  # 更新主角位置
    player.check_collision(platform)  # 檢查碰撞

    # 繪製遊戲畫面
    platform.draw(screen)  # 繪製平台
    player.draw(screen)  # 繪製主角

    pygame.display.update()  # 更新顯示畫面
