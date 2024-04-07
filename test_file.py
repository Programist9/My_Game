import pygame
import os

# Инициализация Pygame
pygame.init()

# Установка размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Простой платформер")

# Загрузка изображений

background_image = pygame.image.load('background.jpg')
block_image = pygame.image.load('block.jpg')
main_char_image = pygame.image.load('mainChar.png')

# Класс для представления персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = main_char_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.vel_y = 0
        self.jump_power = -10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT:
            self.vel_y = self.jump_power
        self.vel_y += 1
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.vel_y
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height

# Класс для представления блоков
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = block_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Функция для создания уровня
def create_level():
    level = pygame.sprite.Group()
    for i in range(10):
        block = Block(i * 100, SCREEN_HEIGHT - 50)
        level.add(block)
    return level

# Создание персонажа и уровня
character = Character()
level = create_level()

# Основной игровой цикл
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    character.update()
    screen.blit(character.image, character.rect)

    level.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
