import pygame 
pygame.init()
# Создание окна
win_w, win_h = 700, 500
pygame.display.set_caption("Платформер")
window=pygame.display.set_mode((win_w, win_h))
FPS = 60
clock = pygame.time.Clock()
# Музыка
pygame.mixer_music.load("backgroundMusic.mp3")
pygame.mixer_music.play(-1)
pygame.mixer_music.set_volume(0.2)
# Задний фон
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background,(win_w, win_h))
# Классы

# Создание объектов и персонажа

# Игровой цикл
game = True
while game:
    # Второстепенная часть цикла
    window.blit(background,(0,0))

    # Обязательная часть цикла
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    pygame.display.update()
    clock.tick(FPS)