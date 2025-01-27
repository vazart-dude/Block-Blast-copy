import pygame
import random
import sys

pygame.init()

#TODO : пофиксить цвет блоков, т.е. сделать из более приятными, улучшить внешний вид блоков - тени
#TODO : возвращать блок в началную позицию, если он был отпущен в invalid position
#TODO : улучшить рамещение блоков????

offset_x = 0
offset_y = 0

# Размеры экрана
width, height = 400, 600
block_size = 40
grid_size = 8

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = (135, 206, 250)  # Фон
block_colors = [RED, GREEN, BLUE]  # Красный, зелёный, синий

# Настройка окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Block Blast Clone")

# Шаблоны блоков (матрицы)
TEMPLATES = [
    [[1]],  # Одинарный блок
    [[1, 1]],  # Горизонтальная линия
    [[1], [1]],  # Вертикальная линия
    [[1, 1], [1, 1]],  # Квадрат
    [[1, 1, 1]],  # Длинная горизонтальная линия
    [[1], [1], [1]],  # Длинная вертикальная линия
    [[1, 0], [1, 1]],  # Левый нижний уголок
    [[0, 1], [1, 1]],  # Правый нижний уголок
    [[1, 1], [1, 0]],  # Левый верхний уголок
    [[1, 1], [0, 1]],  # Правый верхний уголок
    [[1, 1, 1], [0, 0, 1], [0, 0, 1]]  # Большой Г-образный
]


# Класс блока
class Block:
    def __init__(self, template, x, y, field_x, field_y):
        self.template = template
        self.color = random.choice(block_colors)
        self.position = (x, y)
        self.dragging = False
        self.field_x = field_x
        self.field_y = field_y

    def draw(self):
        for row_idx, row in enumerate(self.template):
            for col_idx, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        self.position[0] + col_idx * block_size,
                        self.position[1] + row_idx * block_size,
                        block_size,
                        block_size,
                    )
                    pygame.draw.rect(screen, self.color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 2)  # Контур блока

    def move(self, pos_x, pos_y):
        self.position = pos_x, pos_y

    def get_cells(self):
        global offset_x
        global offset_y
        """Возвращает координаты клеток, занимаемых блоком."""
        cells = []
        for row_idx, row in enumerate(self.template):
            for col_idx, cell in enumerate(row):
                if cell:
                    x = (self.position[0] - self.field_x) // block_size + col_idx
                    y = (self.position[1] - self.field_y) // block_size + row_idx
                    cells.append((y, x))
        print(cells)
        return cells


# Основная функция игры
def main():
    clock = pygame.time.Clock()
    score = 0

    # Игровое поле
    field = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    field_x = (width - (grid_size * block_size)) // 2
    field_y = 100

    # Генерация трёх блоков
    def generate_blocks():
        blocks = []
        for i in range(3):
            template = random.choice(TEMPLATES)
            x = 50 + i * 100
            y = height - 150
            block = Block(template, x, y, field_x, field_y)
            blocks.append(block)
        return blocks

    blocks = generate_blocks()

    # Проверка возможности размещения блока
    def can_place_block(block):
        for y, x in block.get_cells():
            if (
                x < 0
                or y < 0
                or x >= grid_size
                or y >= grid_size
                or field[y][x] is not None
            ):
                return False
        return True

    # Размещение блока на поле
    def place_block(block):
        nonlocal score
        for y, x in block.get_cells():
            field[y][x] = block.color

        # Добавление очков за размещение блока
        block_size = sum(sum(row) for row in block.template)
        score += block_size * 1.5

    # Очистка строк и столбцов
    def clear_lines():
        nonlocal score
        rows_to_clear = []
        cols_to_clear = []

        # Проверка строк
        for row in range(grid_size):
            if all(field[row][col] is not None for col in range(grid_size)):
                rows_to_clear.append(row)

        # Проверка столбцов
        for col in range(grid_size):
            if all(field[row][col] is not None for row in range(grid_size)):
                cols_to_clear.append(col)

        # Очистка строк
        for row in rows_to_clear:
            for col in range(grid_size):
                field[row][col] = None

        # Очистка столбцов
        for col in cols_to_clear:
            for row in range(grid_size):
                field[row][col] = None

        # Подсчёт очков
        for _ in rows_to_clear:
            score += grid_size * 3 + 5
        for _ in cols_to_clear:
            score += grid_size * 3 + 5

    # Основной цикл
    running = True
    while running:
        global offset_x
        global offset_y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for block in blocks:
                    mouse_x, mouse_y = event.pos
                    if pygame.Rect(
                        block.position[0],
                        block.position[1],
                        len(block.template[0]) * block_size,
                        len(block.template) * block_size,
                    ).collidepoint(event.pos):
                        block.dragging = True
                        offset_x = mouse_x - block.position[0]
                        offset_y = mouse_y - block.position[1]

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = event.pos
                for block in blocks:
                    if block.dragging:
                        block.dragging = False
                        if can_place_block(block):
                            place_block(block)
                            clear_lines()  # Очистка строк/столбцов после размещения
                            blocks.remove(block)  # Убираем блок после размещения
                            if not blocks:  # Генерируем новые
                                blocks = generate_blocks()
                        else:
                            # Возвращаем блок на стартовую позицию, если он не может быть размещен
                            template = block.template
                            x = 50 + blocks.index(block) * 100
                            y = height - 150
                            block.move(x, y)

            if event.type == pygame.MOUSEMOTION:
                for block in blocks:
                    if block.dragging:
                        mouse_x, mouse_y = event.pos
                        square_x = mouse_x - offset_x
                        square_y = mouse_y - offset_y
                        block.move(square_x, square_y)

        screen.fill(BG_COLOR)

        # Счет
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Поле
        for row in range(grid_size):
            for col in range(grid_size):
                x = field_x + col * block_size
                y = field_y + row * block_size
                pygame.draw.rect(screen, GRAY, (x, y, block_size, block_size), 0)
                pygame.draw.rect(screen, BLACK, (x, y, block_size, block_size), 2)

                # Рисование блоков
                if field[row][col]:
                    pygame.draw.rect(
                        screen, field[row][col], (x, y, block_size, block_size)
                    )
                    pygame.draw.rect(screen, BLACK, (x, y, block_size, block_size), 2)

        # Рисование блоков
        for block in blocks:
            block.draw()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
