import pygame 
pygame.init()

win_w, win_h = 700, 500
window=pygame.display.set_mode((win_w, win_h))
fps=60
clock = pygame.time.Clock()

pygame.mixer_music.load("snd/No More Magic.ogg")
pygame.mixer_music.play(-1)
pygame.mixer_music.set_volume(0.2)

background = pygame.image.load("img/background.png")
background = pygame.transform.scale(background,(win_w, win_h))
game = True
while game:
    window.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    pygame.display.update()
    clock.tick(fps)