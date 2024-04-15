from pygame import *
from maps import *
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

background_for_menu = image.load("background_for_menu.jpg")
background_for_menu = transform.scale(background_for_menu, (win_w, win_h))

walk_left = [
    image.load('mainCharJUMPorWALKleft2.png'),
    image.load('mainCharJUMPorWALKleft.png'),
    image.load('mainCharJUMPorWALKleft2.png'),
    image.load('mainCharleft.png')
]
walk_right = [
    image.load('mainCharJUMPorWALK2.png'),
    image.load('mainCharJUMPorWALK.png'),
    image.load('mainCharJUMPorWALK2.png'),
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
        global camera_count
        k = key.get_pressed()
        if k[K_a] and self.rect.x >= 20:
            if cam_move == False:
                self.rect.x -= self.speed
            self.left = True
            self.right = False
            camera_count -= 1
        elif k[K_d] and self.rect.x <= win_w-20:
            if cam_move == False:
                self.rect.x += self.speed
            self.right = True
            self.left = False
            camera_count += 1
        else:
            self.left = False
            self.right = False
            self.count = 0

    def animation(self):
        if self.count + 1 >= 20:
            self.count = 0
        if self.left == True:
            window.blit(walk_left[self.count // 5], (self.rect.x, self.rect.y))
            self.count += 1
        elif self.right == True:
            window.blit(walk_right[self.count // 5], (self.rect.x, self.rect.y))
            self.count += 1
        else:
            window.blit(self.image, (self.rect.x, self.rect.y))
    def jump(self,blocks):
        if self.colide(blocks):
            k = key.get_pressed()
            if k[K_SPACE]:
                self.jumping = True
        else:
            self.rect.y += self.speed //2 * lose
        if self.jumping:
            if self.jumpCount == -15:
                self.jumpCount = 20
                self.jumping = False
            else:
                self.rect.y -= self.jumpCount
                self.jumpCount -= 1


    def colide(self,blocks):
        for block in blocks:
            if self.rect.bottom >= block.rect.top-(self.speed//2) and self.rect.bottom <= block.rect.top+(self.speed//2) and self.rect.right >= block.rect.left and self.rect.left <= block.rect.right and lose == 1:
                self.rect.bottom = block.rect.top
                self.jumpCount = 20
                self.jumping = False
                return True
# Создание текстовой надписи
font1 = font.SysFont(None, 100)
font2 = font.SysFont(None, 65)

text_surface_menu = font1.render("МЕНЮ", True, (255, 255, 255))
text_rect_menu = text_surface_menu.get_rect()
text_rect_menu.center = (win_w // 2, win_h // 20)

text_surface_restart = font1.render("Заново", True, (255, 0, 0))
text_rect_restart = text_surface_restart.get_rect()
text_rect_restart.center = (win_w // 2, win_h // 2)

score = 0

text_surface_score = font1.render(f"Очки: {score}", True, (255, 255, 255))
text_rect_score = text_surface_score.get_rect()
text_rect_score.center = (win_w // 2, win_h // 20)

text_surface_play = font2.render("ИГРАТЬ", True, (0,0,0))
text_rect_play = text_surface_play.get_rect()
text_rect_play.center = (win_w // 6, win_h // 3.5)

text_surface_options = font2.render("СКОРО...", True, (0,0,0))
text_rect_options = text_surface_options.get_rect()
text_rect_options.center = (win_w // 6, win_h // 2)
# Создание объектов и персонажа
lose = 1
player = Player(20, win_h - 230, 47, 62, "mainChar.png", 10)
blocks_first = list()
shipis = list()
coins = list()
blocks = blocks_first
# grass = Block(180, win_h - 140, 70, 70, "block.jpg")
# block3 = Block(180, win_h - 210, 70, 70, "block.jpg")
# Shipi = Block(100, win_h - 140, 70, 70, "Shipi.png")
# Flag = Block(win_w-80, win_h - 140, 70, 70, "flag.png")

# blocks_first.append(block3)
# blocks_first.append(grass)
# blocks_first.append(Flag)
# blocks_first.append(Shipi)
my_x = 0
my_y = win_h - 70

block_size = 60
x, y = 0, 0

for line in lvl:
    for s in line:
        if s == "1":
            block = Block(x, y, block_size, block_size, "block.jpg")
            blocks.append(block)
        if s == "2":
            block = Block(x, y, block_size, block_size, "grass.jpg")
            blocks.append(block)
        if s == "3":
            Shipi = Block(x, y, block_size, block_size, "Shipi.png")
            shipis.append(Shipi)
        if s == "4":
            Flag = Block(x, y, block_size, block_size, "flag.png")
            blocks.append(Flag)
        if s == "5":
            Coin = Block(x, y, block_size, block_size, "coin.png")
            coins.append(Coin)
        x += 60
    x = 0
    y += 60
# Игровой цикл
repeat = True
level = 1
camera_count = 0
cam_move = False
pause = False
game = True
sec_game = True
all_game = False
while game:
    if all_game == True:
        print(camera_count)
        # Второстепенная часть цикла
        window.blit(background, (0, 0))
        for block in blocks_first:
            block.update()
            if camera_count > 44 and camera_count < 93:
                cam_move = True
                k = key.get_pressed()
                if k[K_a] and lose == 1:
                    block.rect.x += player.speed
                elif k[K_d] and lose == 1:
                    block.rect.x -= player.speed
            else:
                cam_move = False
        for Coin in coins:
            Coin.update()
            if player.rect.colliderect(Coin.rect):
                coins.remove(Coin)
                score += 1
            if camera_count > 44 and camera_count < 93:
                cam_move = True
                k = key.get_pressed()
                if k[K_a] and lose == 1:
                    Coin.rect.x += player.speed
                elif k[K_d] and lose == 1:
                    Coin.rect.x -= player.speed
            else:
                cam_move = False
        for Shipi in shipis:
            Shipi.update()
            if camera_count > 44 and camera_count < 93:
                k = key.get_pressed()
                if k[K_a] and lose == 1:
                    Shipi.rect.x += player.speed
                elif k[K_d] and lose == 1:
                    Shipi.rect.x -= player.speed
            if (player.rect.bottom >= Shipi.rect.top-40 and player.rect.right >= Shipi.rect.left and player.rect.left <= Shipi.rect.right) or player.rect.colliderect(Shipi.rect):
                lose = 2
        if lose == 2 and repeat == True:
            mixer_music.stop()
            mixer_music.load("gameover.mp3")
            mixer_music.play(1)
            mixer_music.set_volume(1)
            repeat = False
            
        if player.rect.colliderect(Flag.rect):

            player.rect.x = 20
            player.rect.y = win_h - 230
            cam_move = False
            camera_count = 0
            level += 1
            score += 1
            blocks.clear()
            shipis.clear()
            coins.clear()
            if level == 2:
                x, y = 0, 0

                for line in lvl2:
                    for s in line:
                        if s == "1":
                            block = Block(x, y, block_size, block_size, "block.jpg")
                            blocks.append(block)
                        if s == "2":
                            block = Block(x, y, block_size, block_size, "grass.jpg")
                            blocks.append(block)
                        if s == "3":
                            Shipi = Block(x, y, block_size, block_size, "Shipi.png")
                            shipis.append(Shipi)
                        if s == "4":
                            Flag = Block(x, y, block_size, block_size, "flag.png")
                            blocks.append(Flag)
                        if s == "5":
                            Coin = Block(x, y, block_size, block_size, "coin.png")
                            coins.append(Coin)
                        x += 60
                    x = 0
                    y += 60
            elif level == 3:
                x, y = 0, 0

                for line in lvl3:
                    for s in line:
                        if s == "1":
                            block = Block(x, y, block_size, block_size, "block.jpg")
                            blocks.append(block)
                        if s == "2":
                            block = Block(x, y, block_size, block_size, "grass.jpg")
                            blocks.append(block)
                        if s == "3":
                            Shipi = Block(x, y, block_size, block_size, "Shipi.png")
                            shipis.append(Shipi)
                        if s == "4":
                            Flag = Block(x, y, block_size, block_size, "flag.png")
                            blocks.append(Flag)
                        if s == "5":
                            Coin = Block(x, y, block_size, block_size, "coin.png")
                            coins.append(Coin)
                        x += 60
                    x = 0
                    y += 60
            else:
                win = True
        if sec_game:
            if lose == 1:
                player.move()
            elif lose == 2:
                window.blit(text_surface_restart, text_rect_restart)



        player.jump(blocks)
        player.animation()
        text_surface_score = font1.render(f"Очки: {score}", True, (255, 255, 255))
        window.blit(text_surface_score, text_rect_score)
    elif all_game == False:
        window.blit(background_for_menu, (0, 0))
        window.blit(text_surface_menu, text_rect_menu)
        window.blit(text_surface_play, text_rect_play)
        window.blit(text_surface_options, text_rect_options)
    # Обязательная часть цикла
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            if text_rect_play.collidepoint(e.pos):
                all_game = True
            if text_rect_restart.collidepoint(e.pos):
                player.rect.x = 20
                player.rect.y = win_h - 230
                cam_move = False
                camera_count = 0
                score -= 1
                lose = 1
                repeat = True
                blocks.clear()
                shipis.clear()
                coins.clear()
                mixer_music.load("backgroundMusic.mp3")
                mixer_music.play(-1)
                mixer_music.set_volume(0.2)
                if level == 1:
                    x, y = 0, 0

                    for line in lvl:
                        for s in line:
                            if s == "1":
                                block = Block(x, y, block_size, block_size, "block.jpg")
                                blocks.append(block)
                            if s == "2":
                                block = Block(x, y, block_size, block_size, "grass.jpg")
                                blocks.append(block)
                            if s == "3":
                                Shipi = Block(x, y, block_size, block_size, "Shipi.png")
                                shipis.append(Shipi)
                            if s == "4":
                                Flag = Block(x, y, block_size, block_size, "flag.png")
                                blocks.append(Flag)
                            if s == "5":
                                Coin = Block(x, y, block_size, block_size, "coin.png")
                                coins.append(Coin)
                            x += 60
                        x = 0
                        y += 60
                elif level == 2:
                    x, y = 0, 0

                    for line in lvl2:
                        for s in line:
                            if s == "1":
                                block = Block(x, y, block_size, block_size, "block.jpg")
                                blocks.append(block)
                            if s == "2":
                                block = Block(x, y, block_size, block_size, "grass.jpg")
                                blocks.append(block)
                            if s == "3":
                                Shipi = Block(x, y, block_size, block_size, "Shipi.png")
                                shipis.append(Shipi)
                            if s == "4":
                                Flag = Block(x, y, block_size, block_size, "flag.png")
                                blocks.append(Flag)
                            if s == "5":
                                Coin = Block(x, y, block_size, block_size, "coin.png")
                                coins.append(Coin)
                            x += 60
                        x = 0
                        y += 60
                elif level == 3:
                    x, y = 0, 0

                    for line in lvl3:
                        for s in line:
                            if s == "1":
                                block = Block(x, y, block_size, block_size, "block.jpg")
                                blocks.append(block)
                            if s == "2":
                                block = Block(x, y, block_size, block_size, "grass.jpg")
                                blocks.append(block)
                            if s == "3":
                                Shipi = Block(x, y, block_size, block_size, "Shipi.png")
                                shipis.append(Shipi)
                            if s == "4":
                                Flag = Block(x, y, block_size, block_size, "flag.png")
                                blocks.append(Flag)
                            if s == "5":
                                Coin = Block(x, y, block_size, block_size, "coin.png")
                                coins.append(Coin)
                            x += 60
                        x = 0
                        y += 60
    display.update()
    clock.tick(FPS)
