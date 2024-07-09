import pygame

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen = pygame.display.set_mode((640, 480))

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# 退出 Pygame
pygame.quit()
