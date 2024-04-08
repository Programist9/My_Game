from pygame import *
from random import randint

init()

# Создание окна
win_w, win_h = 900, 700
display.set_caption("Платформер")
window = display.set_mode((win_w, win_h))
FPS = 20
clock = time.Clock()

# Музыка
mixer_music.load("backgroundMusic.mp3")
mixer_music.play(-1)
mixer_music.set_volume(0.2)

# Задний фон
background = image.load("background.jpg")
background = transform.scale(background, (win_w, win_h))

walk_left = [
    image.load('mainCharJUMPorWALKleft.png'),
    image.load('mainCharleft.png')
]
walk_right = [
    image.load('mainCharJUMPorWALK.png'),
    image.load('mainChar.png')
]

# Классы
class Sprite():
    def __init__(self, x, y, w, h, image):
        self.rect = Rect(x, y, w, h)
        image = transform.scale(image, (w, h))
        self.image = image
    
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Block(Sprite):
    def __init__(self, x, y, w, h, block_image):
        self.image = transform.scale(image.load(block_image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(Sprite):
    def __init__(self, x, y, w, h, player_image, speed):
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.left = False
        self.right = False
        self.count = 0

        self.isJump = False
        self.fall = False
        self.jump_count = 20

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
    def jump(self):
        k = key.get_pressed()
        if k[K_SPACE] and not self.isJump: # and self.fall == False
            self.isJump = True
        if self.isJump:
            if self.jump_count >= 0:
                self.rect.y -= (self.jump_count ** 2) * 0.2
                self.jump_count -= 1
            else:
                self.isJump = False
                self.jump_count = 20

    def animation(self):
        if self.count + 1 >= 20:
            self.count = 0
        if self.left == True:
            window.blit(walk_left[self.count // 10], (self.rect.x, self.rect.y))
            self.count += 1
        elif self.right == True:
            window.blit(walk_right[self.count // 10], (self.rect.x, self.rect.y))
            self.count += 1
        else:
            window.blit(self.image, (self.rect.x, self.rect.y))

# Создание объектов и персонажа
player = Player(20, 200, 47, 62, "mainChar.png", 10)
blocks = []
my_x = 0
my_y = win_h - 70
for i in range(13):
    block = Block(my_x, my_y, 70, 70, "block2.jpg")
    blocks.append(block)
    my_x += 70
    my_y -= 50
# Игровой цикл
pause = False
game = True
while game:
    window.blit(background, (0, 0))

    # Второстепенная часть цикла
    for block in blocks:
        if player.rect.colliderect(block.rect):
            if player.rect.bottom > block.rect.top - 8:  # Проверяем, что игрок находится выше блока
                player.rect.bottom = block.rect.top - 8 # Помещаем игрока на верхнюю грань блока
                player.fall = False
                print('1')
        elif not player.rect.colliderect(block.rect):
            player.rect.y += 2
            player.fall = True
            print('2')
        block.update()
        
    if pause == False:
        player.move()
        player.jump()
        
    player.animation()

    # Обязательная часть цикла
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_r and pause == False:
            pause = True
            print('пауза')
        if e.type == KEYDOWN and e.key == K_ESCAPE and pause == True:
            pause = False
            print('не пауза')

    display.update()
    clock.tick(FPS)
