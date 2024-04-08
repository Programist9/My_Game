from pygame import *
from random import randint

init()

# Создание окна
win_w, win_h = 900, 700
display.set_caption("Платформер")
window = display.set_mode((win_w, win_h))
FPS = 30
clock = time.Clock()

# Музыка
mixer_music.load("backgroundMusic.mp3")
mixer_music.play(-1)
mixer_music.set_volume(0.2)

# Задний фон
background = image.load("background.jpg")
background = transform.scale(background, (win_w, win_h))

walk_left = [
    image.load('mainCharJUMPorWALKleft2.png'),
    image.load('mainCharJUMPorWALKleft.png'),
    image.load('mainCharleft.png')
]
walk_right = [
    image.load('mainCharJUMPorWALK2.png'),
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

        self.jumping = False
        self.jumpCount = 20

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
        if self.count + 1 >= 30:
            self.count = 0
        if self.left == True:
            window.blit(walk_left[self.count // 10], (self.rect.x, self.rect.y))
            self.count += 1
        elif self.right == True:
            window.blit(walk_right[self.count // 10], (self.rect.x, self.rect.y))
            self.count += 1
        else:
            window.blit(self.image, (self.rect.x, self.rect.y))
    def jump(self,blocks):
        print(self.jumpCount)
        print(self.colide(blocks))
        if self.colide(blocks):
            k = key.get_pressed()
            if k[K_SPACE]:
                self.jumping = True
                print('1')
        else:
            self.rect.y += self.speed //2
        if self.jumping:
            if self.jumpCount == -20:
                self.jumpCount = 20
                self.jumping = False
            else:
                self.rect.y -= self.jumpCount
                self.jumpCount -= 1


    def colide(self,blocks):
        for block in blocks:
            if self.rect.bottom >= block.rect.top-(self.speed//2) and self.rect.bottom <= block.rect.top+(self.speed//2) and self.rect.right >= block.rect.left and self.rect.left <= block.rect.right:
                self.rect.bottom = block.rect.top
                self.jumpCount = 20
                self.jumping = False
                return True
# Создание объектов и персонажа
player = Player(20, 400, 47, 62, "mainChar.png", 10)
block2 = Block(0, win_h - 180, 70, 70, "block2.jpg")
blocks = []
blocks.append(block2)
my_x = 0
my_y = win_h - 70
for i in range(13):
    block = Block(my_x, my_y, 70, 70, "block2.jpg")
    blocks.append(block)
    my_x += 70
    # my_y -= 50
# Игровой цикл
pause = False
game = True
while game:
    window.blit(background, (0, 0))
    # Второстепенная часть цикла
    for block in blocks:
        block.update()
        block2.update()
    print(player.colide(blocks))
        # if player.rect.bottom >= block.rect.top:
        #     if player.rect.bottom > block.rect.top:  # Проверяем, что игрок находится выше блока
        #         player.rect.y -= 0.5
        #     if player.rect.bottom == block.rect.top:
        #         player.fall = False
        #     print(player.rect.bottom)
        # elif not player.rect.bottom >= block.rect.top:
        #     player.rect.y += 2
        #     player.fall = True
            # print(player.rect.bottom)
    player.jump(blocks)
    player.move()
    player.animation()

    # Обязательная часть цикла
    for e in event.get():
        if e.type == QUIT:
            game = False
        # if e.type == KEYDOWN and e.key == K_r and pause == False:
        #     pause = True
        #     print('пауза')
        # if e.type == KEYDOWN and e.key == K_ESCAPE and pause == True:
        #     pause = False
        #     print('не пауза')

    display.update()
    clock.tick(FPS)
