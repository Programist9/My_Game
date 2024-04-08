from pygame import *
from random import randint
init()
# Создание окна
win_w, win_h = 700, 500
display.set_caption("Платформер")
window=display.set_mode((win_w, win_h))
FPS = 20
clock = time.Clock()
# Музыка
mixer_music.load("backgroundMusic.mp3")
mixer_music.play(-1)
mixer_music.set_volume(0.2)
# Задний фон
background = image.load("background.jpg")
background = transform.scale(background,(win_w, win_h))
# Классы
class Sprite():
    def __init__(self,x,y,w,h,image):
        self.rect = Rect(x,y,w,h)
        image = transform.scale(image,(w,h))
        self.image = image
    def update(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
walk_left = [
    image.load('mainCharJUMPorWALKleft.png'),
    image.load('mainCharleft.png')
]
walk_right = [
    image.load('mainCharJUMPorWALK.png'),
    image.load('mainChar.png')
]
class Player(Sprite):
    def __init__(self,x,y,w,h,player_image,speed):
        self.image = transform.scale(image.load(player_image),(w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.left = False
        self.right = False
        self.count = 0

    def move(self):
        k = key.get_pressed()
        if k[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
            self.left = True
            self.right = False
        elif k[K_d] and self.rect.right <= win_w:
            self.rect.x += self.speed
            self.right = True
            self.left = False
        else:
            self.left = False
            self.right = False
            self.count = 0
    def animation(self):
        if self.count + 1 >= 20:
            self.count = 0
        if self.left == True:
            window.blit(walk_left[self.count // 10], (self.rect.x,self.rect.y))
            self.count += 1
        elif self.right == True:
            window.blit(walk_right[self.count // 10], (self.rect.x,self.rect.y))
            self.count += 1
        else:
            window.blit(self.image,(self.rect.x,self.rect.y))
# Создание объектов и персонажа
player = Player(20, 20, 47, 62, "mainChar.png", 2)
# Игровой цикл
pause = False
game = True
while game:
    window.blit(background,(0,0))
    if pause == False:
        # Второстепенная часть цикла
        player.move()
        # player.update()
        player.animation()
    # Обязательная часть цикла
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_ESCAPE and pause == False:
            pause = True
            font = font.Font(None, 80)
            text = '//'
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(win_w // 2, win_h // 2))
        if e.type == KEYDOWN and e.key == K_ESCAPE and pause == True:
            pause = False
    display.update()
    clock.tick(FPS)