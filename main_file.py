import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Простой платформер")

# Класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.jump = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.acc = pygame.math.Vector2(0, 0.5)

        if keys[pygame.K_LEFT]:
            self.acc.x = -0.5
        if keys[pygame.K_RIGHT]:
            self.acc.x = 0.5

        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        self.rect.x += self.vel.x + 0.5 * self.acc.x
        self.rect.y += self.vel.y + 0.5 * self.acc.y

        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

# Группа спрайтов
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Главный цикл игры
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Отрисовка
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
