######################匯入模組######################
import pygame
import sys
import math
import random  # 新增random模組

######################初始化######################
pygame.init()
width = 640
height = 320
can_draw = False  # 新增控制是否可以畫畫的變數
######################建立視窗及物件######################
# screen(width, height)
screen = pygame.display.set_mode((width, height))
# set screen'title
pygame.display.set_caption("MY poor game")
#####################畫布######################
bg = pygame.Surface((width, height))
bg.fill((255, 255, 255))  # 畫布顏色
####################繪製圖形######################
# 畫圓形 (畫布, 顏色, 圓心座標, 半徑, 線寬)
pygame.draw.circle(bg, (0, 0, 255), (200, 100), 30, 0)
pygame.draw.circle(bg, (0, 0, 255), (400, 100), 30, 0)
# 畫線 (畫布, 顏色, 起始座標, 結束座標, 線寬)
pygame.draw.line(bg, (225, 0, 255), (280, 220), (320, 220), 3)
# 畫矩形 (畫布, 顏色, (左上角座標, 寬, 高), 線寬)
pygame.draw.rect(bg, (0, 255, 0), (270, 130, 60, 40), 5)
# 畫橢圓 (畫布, 顏色, (左上角座標, 寬, 高), 線寬)
pygame.draw.ellipse(bg, (255, 0, 0), (200, 130, 200, 100), 5)
pygame.draw.ellipse(bg, (255, 0, 0), (200, 130, 200, 100), 5)
# 畫弧形 (畫布, 顏色, (左上角座標, 寬, 高), 起始角度, 結束角度, 線寬)
# 畫多邊形 (畫布, 顏色, [(座標1), (座標2), ...], 線寬)
pygame.draw.polygon(bg, (0, 0, 0), [(200, 130), (400, 130), (300, 50)], 5)
pygame.draw.arc(
    bg, (255, 10, 0), [100, 100, 100, 50], math.radians(180), math.radians(0), 2
)


def get_random_color():
    return (
        random.randint(0, 255),  # 隨機紅色
        random.randint(0, 255),  # 隨機綠色
        random.randint(0, 255),  # 隨機藍色
    )


######################循環偵測######################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # 離開遊戲

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()  # 獲取滑鼠位置
            print(f"mouse position: {x}, {y}")
            can_draw = not can_draw  # 切換畫畫模式

        if event.type == pygame.MOUSEMOTION and can_draw:
            x, y = pygame.mouse.get_pos()
            # 在滑鼠位置畫一個小圓點，使用隨機顏色
            pygame.draw.circle(bg, get_random_color(), (x, y), 4, 0)

    screen.blit(bg, (0, 0))
    pygame.display.update()
