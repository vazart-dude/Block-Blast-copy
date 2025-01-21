import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 400, 600
BLOCK_SIZE = 50
FPS = 30

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Blast")
pygame.display.set_icon(pygame.image.load("data/icon.png"))
# Класс блока
class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.color = random.choice([RED, GREEN, BLUE])

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    blocks = []
    score = 0

    # Создание блоков
    for _ in range(5):
        x = random.randint(0, WIDTH - BLOCK_SIZE)
        y = random.randint(0, HEIGHT - BLOCK_SIZE)
        blocks.append(Block(x, y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for block in blocks[:]:
                    if block.rect.collidepoint(mouse_x, mouse_y):
                        blocks.remove(block)
                        score += 1

        # Отрисовка
        screen.fill(WHITE)
        for block in blocks:
            block.draw()

        # Отображение счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
