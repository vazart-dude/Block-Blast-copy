import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))

background_color = (255, 255, 255)

block_color = (255, 0, 0)

block_alpha = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(background_color)

    s = pygame.Surface((100, 100))
    s.set_alpha(block_alpha)
    s.fill(block_color)

    screen.blit(s, (100, 100))

    pygame.display.flip()

    pygame.time.Clock().tick(60)
