######################載入必要的套件######################
import pygame  # 載入 pygame 套件，用於遊戲開發
import sys  # 載入 sys 套件，用於系統相關功能
import random  # 載入 random 套件，用於產生隨機數


######################定義遊戲物件類別######################
class Platform:
    def __init__(self, x, y, width, height, color):
        """平台物件初始化
        x, y: 平台的左上角座標位置
        width, height: 平台的寬度和高度
        color: 平台的顏色（RGB格式）
        """
        # 建立平台的碰撞範圍（矩形）
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color  # 設定平台顏色

    def draw(self, display_area):
        """繪製平台
        display_area: pygame的顯示區域物件
        """
        # 在指定的顯示區域繪製矩形平台
        pygame.draw.rect(display_area, self.color, self.rect)

    def move_down(self, speed):
        """讓平台向下移動
        speed: 移動速度（像素/幀）
        """
        # 更新平台的垂直位置
        self.rect.y += speed


class Player:
    def __init__(self, x, y, width, height, color):
        """主角物件初始化
        x, y: 主角的初始位置（左上角座標）
        width, height: 主角的寬度和高度
        color: 主角的顏色（RGB格式）
        """
        # 建立主角的碰撞範圍（矩形）
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color  # 設定主角顏色
        self.velocity_y = 12  # 設定初始垂直速度
        self.gravity = 0.5  # 設定重力加速度
        self.is_falling = True  # 追蹤主角是否正在下落
        self.jump_speed = 12  # 設定跳躍速度

    def draw(self, display_area):
        """繪製主角
        display_area: pygame的顯示區域物件
        """
        # 在指定的顯示區域繪製主角方塊
        pygame.draw.rect(display_area, self.color, self.rect)

    def move(self, bg_x):
        """處理主角的移動邏輯
        bg_x: 遊戲背景的寬度，用於處理穿牆效果
        """
        # 更新垂直位置和速度
        self.rect.y -= self.velocity_y  # 根據當前速度更新垂直位置
        self.velocity_y -= self.gravity  # 受重力影響，速度減少
        self.is_falling = self.velocity_y < 0  # 當垂直速度小於0時，表示正在下落

        # 處理鍵盤左右移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # 按下左方向鍵
            self.rect.x -= 5  # 向左移動5像素
        if keys[pygame.K_RIGHT]:  # 按下右方向鍵
            self.rect.x += 5  # 向右移動5像素

        # 處理穿牆效果
        if self.rect.left > bg_x:  # 超出右邊界
            self.rect.right = 0  # 從左側出現
        elif self.rect.right < 0:  # 超出左邊界
            self.rect.left = bg_x  # 從右側出現

    def check_collision(self, platforms):
        """檢測主角是否與任何平台發生碰撞
        platforms: 要檢查碰撞的平台物件列表
        return: True表示發生有效碰撞，False表示未發生碰撞
        """
        # 檢查與每個平台的碰撞
        for platform in platforms:
            if (
                self.is_falling  # 確認主角正在下落
                and self.rect.bottom >= platform.rect.top  # 主角底部碰到平台頂部
                and self.rect.bottom <= platform.rect.bottom  # 確保不是從下方碰撞
                and self.rect.right >= platform.rect.left  # 確認水平方向有重疊（右側）
                and self.rect.left <= platform.rect.right
            ):  # 確認水平方向有重疊（左側）

                # 碰撞處理
                self.rect.bottom = platform.rect.top  # 將主角位置調整到平台頂部
                self.velocity_y = self.jump_speed  # 給予向上的彈跳速度
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

# 建立平台相關設定
platforms = []  # 建立平台列表
platform_count = 10  # 設定初始平台數量
platform_spacing = 60  # 設定平台間的垂直間距

# 建立玩家腳下的第一個平台（固定位置）
first_platform = Platform(
    (bg_x - 60) // 2,  # X座標置中
    bg_y - 70,  # Y座標在玩家腳下
    60,  # 平台寬度
    10,  # 平台高度
    (255, 255, 255),  # 平台顏色（白色）
)
platforms.append(first_platform)

# 建立初始的隨機平台
for i in range(1, platform_count):
    platform_x = random.randint(0, bg_x - 60)  # 隨機X座標
    platform_y = bg_y - (i * platform_spacing) - 50  # 計算Y座標
    platforms.append(
        Platform(
            platform_x,  # 隨機X座標
            platform_y,  # 計算後的Y座標
            60,  # 平台寬度
            10,  # 平台高度
            (255, 255, 255),  # 平台顏色（白色）
        )
    )

######################遊戲主迴圈######################
platform_speed = 0  # 平台移動速度（初始為0）

while True:
    FPS.tick(60)  # 控制遊戲更新頻率為60FPS
    screen.fill((0, 0, 0))  # 用黑色填充畫面背景

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 更新遊戲狀態
    player.move(bg_x)  # 更新主角位置

    # 當主角上升到畫面中間時，開始移動平台
    if player.rect.y < bg_y // 2:
        platform_speed = 5  # 設定平台下移速度
        player.rect.y = bg_y // 2  # 固定主角在畫面中間
    else:
        platform_speed = 0  # 主角在下半部時，平台不移動

    # 更新所有平台的位置
    for platform in platforms[:]:  # 使用切片來創建列表副本，避免在迭代時修改列表
        platform.move_down(platform_speed)  # 移動平台

        # 刪除移出畫面的平台
        if platform.rect.top >= bg_y:
            platforms.remove(platform)

            # 在上方生成新的平台
            new_platform_x = random.randint(0, bg_x - 60)
            # 找到最高的平台
            highest_platform = min(platforms, key=lambda p: p.rect.y)
            # 在最高平台上方生成新平台
            new_platform_y = highest_platform.rect.y - platform_spacing

            platforms.append(
                Platform(
                    new_platform_x,  # 隨機X座標
                    new_platform_y,  # 在最高平台上方
                    60,  # 平台寬度
                    10,  # 平台高度
                    (255, 255, 255),  # 平台顏色（白色）
                )
            )

    # 檢查碰撞
    player.check_collision(platforms)

    # 繪製遊戲畫面
    for platform in platforms:
        platform.draw(screen)  # 繪製所有平台
    player.draw(screen)  # 繪製主角

    pygame.display.update()  # 更新顯示畫面
