######################載入必要的套件######################
import pygame  # 載入 pygame 套件，用於遊戲開發
import sys  # 載入 sys 套件，用於系統相關功能
import random  # 載入 random 套件，用於產生隨機數

######################初始化設定######################
pygame.init()  # 初始化 pygame
pygame.font.init()  # 初始化字體系統
# 建立字體物件，使用微軟正黑體，大小為36
font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 36)
FPS = pygame.time.Clock()  # 建立 FPS 時鐘物件

######################遊戲視窗設定######################
bg_x = 400  # 設定視窗寬度
bg_y = 600  # 設定視窗高度
bg_size = (bg_x, bg_y)  # 設定視窗尺寸
screen = pygame.display.set_mode(bg_size)  # 建立遊戲視窗
pygame.display.set_caption("Doodle Jump")  # 設定視窗標題


######################定義遊戲物件類別######################
class Platform:
    def __init__(self, x, y, width, height, color):
        """平台物件初始化
        x, y: 平台的左上角座標位置
        width, height: 平台的寬度和高度
        color: 平台的顏色（RGB格式）
        """
        self.rect = pygame.Rect(x, y, width, height)  # 建立平台的碰撞範圍
        self.color = color  # 設定平台顏色

    def draw(self, display_area):
        """繪製平台到指定的顯示區域"""
        pygame.draw.rect(display_area, self.color, self.rect)

    def move_down(self, speed):
        """讓平台向下移動
        speed: 移動速度（像素/幀）
        """
        self.rect.y += speed  # 更新平台的垂直位置


class Player:
    def __init__(self, x, y, width, height, color):
        """主角物件初始化"""
        self.rect = pygame.Rect(x, y, width, height)  # 建立主角碰撞範圍
        self.color = color  # 設定主角顏色
        self.velocity_y = 12  # 設定初始垂直速度
        self.gravity = 0.5  # 設定重力加速度
        self.is_falling = True  # 追蹤主角是否正在下落
        self.jump_speed = 12  # 設定跳躍速度
        self.score = 0  # 初始化分數為0
        self.max_height = y  # 記錄最高點，用於計算分數

    def draw(self, display_area):
        """繪製主角到指定的顯示區域"""
        pygame.draw.rect(display_area, self.color, self.rect)

    def update_score(self):
        """更新分數
        當玩家到達新的最高點時增加分數
        """
        if self.rect.y < self.max_height:
            # 計算高度差並轉換為分數
            height_diff = self.max_height - self.rect.y
            self.score += int(height_diff / 10)  # 每上升10像素得1分
            self.max_height = self.rect.y

    def move(self, bg_x):
        """處理主角的移動邏輯"""
        # 更新垂直位置和速度
        self.rect.y -= self.velocity_y
        self.velocity_y -= self.gravity
        self.is_falling = self.velocity_y < 0

        # 處理鍵盤左右移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # 按下左方向鍵
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:  # 按下右方向鍵
            self.rect.x += 5

        # 處理穿牆效果
        if self.rect.left > bg_x:  # 從右邊出去
            self.rect.right = 0  # 從左邊進來
        elif self.rect.right < 0:  # 從左邊出去
            self.rect.left = bg_x  # 從右邊進來

    def check_collision(self, platforms):
        """檢測與平台的碰撞"""
        for platform in platforms:
            # 檢查碰撞條件
            if (
                self.is_falling
                and self.rect.bottom >= platform.rect.top
                and self.rect.bottom <= platform.rect.bottom
                and self.rect.right >= platform.rect.left
                and self.rect.left <= platform.rect.right
            ):

                # 碰撞處理
                self.rect.bottom = platform.rect.top
                self.velocity_y = self.jump_speed
                self.is_falling = False
                return True
        return False


######################建立遊戲物件######################
# 建立主角
player = Player(
    (bg_x - 30) // 2,  # X座標置中
    bg_y - 100,  # Y座標在下方100像素處
    30,
    30,  # 主角的寬度和高度
    (0, 255, 0),  # 主角顏色（綠色）
)

# 建立平台
platforms = []  # 平台列表
platform_count = 10  # 初始平台數量
platform_spacing = 60  # 平台間距

# 建立第一個平台（玩家腳下的平台）
first_platform = Platform(
    (bg_x - 60) // 2,  # X座標置中
    bg_y - 70,  # Y座標在玩家腳下
    60,
    10,  # 平台的寬度和高度
    (255, 255, 255),  # 平台顏色（白色）
)
platforms.append(first_platform)

# 建立其他初始平台
for i in range(1, platform_count):
    platform_x = random.randint(0, bg_x - 60)
    platform_y = bg_y - (i * platform_spacing) - 50
    platforms.append(
        Platform(
            platform_x,  # 隨機X座標
            platform_y,  # 計算後的Y座標
            60,
            10,  # 平台的寬度和高度
            (255, 255, 255),  # 平台顏色（白色）
        )
    )

######################遊戲主迴圈######################
platform_speed = 0  # 平台初始移動速度
game_over = False  # 遊戲結束標記

while True:
    FPS.tick(60)  # 限制遊戲更新頻率為60FPS
    screen.fill((0, 0, 0))  # 黑色背景

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # 更新遊戲狀態
        player.move(bg_x)
        player.update_score()  # 更新分數

        # 檢查遊戲結束條件
        if player.rect.top > bg_y:
            game_over = True

        # 相機跟隨效果（當玩家上升到一定高度時）
        if player.rect.y < bg_y // 2:
            platform_speed = 5
            player.rect.y = bg_y // 2
        else:
            platform_speed = 0

        # 更新平台
        for platform in platforms[:]:
            platform.move_down(platform_speed)

            # 移除離開畫面的平台並在上方生成新平台
            if platform.rect.top >= bg_y:
                platforms.remove(platform)
                new_platform_x = random.randint(0, bg_x - 60)
                highest_platform = min(platforms, key=lambda p: p.rect.y)
                new_platform_y = highest_platform.rect.y - platform_spacing

                platforms.append(
                    Platform(
                        new_platform_x,  # 隨機X座標
                        new_platform_y,  # 在最高平台上方
                        60,
                        10,  # 平台寬度和高度
                        (255, 255, 255),  # 平台顏色（白色）
                    )
                )

        # 碰撞檢測
        player.check_collision(platforms)

    # 繪製遊戲畫面
    for platform in platforms:
        platform.draw(screen)
    player.draw(screen)  # 顯示分數
    score_text = font.render(f"分數：{player.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # 顯示遊戲結束畫面
    if game_over:
        game_over_text = font.render("遊戲結束！", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(bg_x // 2, bg_y // 2))
        screen.blit(game_over_text, game_over_rect)

        final_score_text = font.render(
            f"最終分數：{player.score}", True, (255, 255, 255)
        )
        final_score_rect = final_score_text.get_rect(center=(bg_x // 2, bg_y // 2 + 50))
        screen.blit(final_score_text, final_score_rect)

        # 添加重玩按鈕
        restart_text = font.render("重新開始", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(bg_x // 2, bg_y // 2 + 100))
        # 繪製按鈕背景
        pygame.draw.rect(screen, (100, 100, 100), restart_rect.inflate(20, 10))
        screen.blit(restart_text, restart_rect)

        # 檢測滑鼠點擊
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        if restart_rect.collidepoint(mouse_pos) and mouse_click:
            # 重置遊戲
            game_over = False
            player.rect.x = (bg_x - 30) // 2
            player.rect.y = bg_y - 100
            player.velocity_y = 12
            player.score = 0
            player.max_height = player.rect.y

            # 重置平台
            platforms.clear()
            platforms.append(
                Platform((bg_x - 60) // 2, bg_y - 70, 60, 10, (255, 255, 255))
            )
            for i in range(1, platform_count):
                platform_x = random.randint(0, bg_x - 60)
                platform_y = bg_y - (i * platform_spacing) - 50
                platforms.append(
                    Platform(platform_x, platform_y, 60, 10, (255, 255, 255))
                )

    pygame.display.update()  # 更新顯示畫面
