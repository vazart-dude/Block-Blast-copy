import pygame
import random
import sys
import os

pygame.init()

# Размеры экрана
width, height = 450, 600
block_size = 40
grid_size = 8

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BG_COLOR = (135, 206, 250)  # Фон
SHADOW_COLOR = (100, 100, 100, 50)  # Тень блока
block_colors = [
    (239, 83, 80),  # Красный
    (102, 187, 106),  # Зеленый
    (66, 165, 245),  # Синий
    (255, 238, 88),  # Желтый
    (171, 71, 188),  # Фиолетовый
]

# Настройка окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Block Blast Clone")
script_path = os.path.dirname(os.path.abspath(__file__))
icon = pygame.image.load(os.path.join(script_path, "data", "icon.png"))
pygame.display.set_icon(icon)

# Шаблоны блоков (матрицы)
TEMPLATES = [
    # Квадраты
    [[[1]],  # Одинарный блок
    [[1, 1], [1, 1]]], # Квадрат 2х2
    # Линии
    [[[1, 1]],  # Горизонтальная линия
    [[1], [1]],  # Вертикальная линия
    [[1, 1, 1]],  # Длинная горизонтальная линия
    [[1], [1], [1]]],  # Длинная вертикальная линия
    # Маленькие уголки
    [[[1, 0], [1, 1]],  # Левый нижний уголок
    [[0, 1], [1, 1]],  # Правый нижний уголок
    [[1, 1], [1, 0]],  # Левый верхний уголок
    [[1, 1], [0, 1]]],  # Правый верхний уголок
    # Г-образные блоки
    [[[1, 1], [0, 1], [0, 1]],  # Правый верхний уголок
    [[1, 1], [1, 0], [1, 0]],  # Левый верхний уголок
    [[0, 1], [0, 1], [1, 1]], # Правый нижний уголок
    [[1, 0], [1, 0], [1, 1]]], # Левый нижний уголок
    # Большие уголки
    [[[1, 1, 1], [0, 0, 1], [0, 0, 1]], # Правый верхний уголок
    [[1, 1, 1], [1, 0, 0], [1, 0, 0]], # Левый верхний уголок
    [[0, 0, 1], [0, 0, 1], [1, 1, 1]], # Правый нижний уголок
    [[1, 0, 0], [1, 0, 0], [1, 1, 1]]] # Левый нижний уголок
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
        self.initial_position = (x, y)

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
                    shadow_rect = rect.move(5, 5)  # Тень
                    pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect)
                    pygame.draw.rect(screen, self.color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 2)  # Контур блока

    def move(self, pos_x, pos_y):
        self.position = pos_x, pos_y

    def reset_position(self):
        """Возвращает блок в начальную позицию."""
        self.position = self.initial_position

    def snap_to_grid(self):
        """Привязка блока к сетке."""
        grid_x = (
            round((self.position[0] - self.field_x) / block_size) * block_size
            + self.field_x
        )
        grid_y = (
            round((self.position[1] - self.field_y) / block_size) * block_size
            + self.field_y
        )
        self.position = grid_x, grid_y

    def get_cells(self):
        """Возвращает координаты клеток, занимаемых блоком."""
        cells = []
        for row_idx, row in enumerate(self.template):
            for col_idx, cell in enumerate(row):
                if cell:
                    x = (self.position[0] - self.field_x) // block_size + col_idx
                    y = (self.position[1] - self.field_y) // block_size + row_idx
                    cells.append((y, x))
        return cells


# Функция перезапуска игры
def restart_game():
    main()


# Меню победы
def show_victory_menu(score):
    """Отображает меню победы с кнопкой рестарта."""
    font = pygame.font.Font(None, 48)
    text = font.render(f"Победа! Счет: {score}", True, BLACK)
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))

    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("ИГРАТЬ СНОВА", True, BLACK)
    button_rect = button_text.get_rect(center=(width // 2, height // 2 + 30))
    button_box = button_rect.inflate(20, 10)

    while True:
        screen.fill(BG_COLOR)
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, GRAY, button_box)  # Кнопка
        pygame.draw.rect(screen, BLACK, button_box, 2)  # Контур кнопки
        screen.blit(button_text, button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_box.collidepoint(
                event.pos
            ):
                restart_game()

        pygame.display.flip()


# Меню старта игры
def show_start_menu():
    """Отображает стартовое меню с кнопкой начала игры."""
    font = pygame.font.Font(None, 48)
    text = font.render("Block Blast", True, WHITE)
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))

    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("СТАРТ", True, WHITE)
    button_rect = button_text.get_rect(center=(width // 2, height // 2 + 30))
    button_box = button_rect.inflate(20, 10)

    while True:
        screen.fill(BG_COLOR)
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, GRAY, button_box)  # Кнопка
        pygame.draw.rect(screen, BLACK, button_box, 2)  # Контур кнопки
        screen.blit(button_text, button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_box.collidepoint(
                event.pos
            ):
                return  # Переход к основной игре

        pygame.display.flip()


def show_game_over_menu(score):
    """Показывает меню Вы проиграли!."""
    font = pygame.font.Font(None, 64)
    title_text = font.render("Вы проиграли!", True, WHITE)
    title_rect = title_text.get_rect(center=(width // 2, height // 2 - 50))

    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(f"Счет: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(width // 2, height // 2))

    button_font = pygame.font.Font(None, 48)
    button_text = button_font.render("ИГРАТЬ СНОВА", True, WHITE)
    button_rect = button_text.get_rect(center=(width // 2, height // 2 + 100))
    button_box = button_rect.inflate(20, 10)

    while True:
        screen.fill(BG_COLOR)
        screen.blit(title_text, title_rect)
        screen.blit(score_text, score_rect)
        pygame.draw.rect(screen, GRAY, button_box)  # Кнопка
        pygame.draw.rect(screen, BLACK, button_box, 2)  # Контур кнопки
        screen.blit(button_text, button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_box.collidepoint(
                event.pos
            ):
                restart_game()  # Перезапуск игры

        pygame.display.flip()


# Основная функция игры
def main():
    clock = pygame.time.Clock()
    score = 0

    # Показываем стартовое меню при первом запуске игры
    show_start_menu()

    # Игровое поле
    field = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    field_x = (width - (grid_size * block_size)) // 2
    field_y = 100

    def generate_blocks():
        blocks = []
        block_width = max(len(temp[0]) for template in TEMPLATES for temp in template) * block_size
        gap = 20  # расстояние между блоками
        x = 50
        templates = list(TEMPLATES)
        random.shuffle(templates)
        for i in range(3):

            probability = random.randint(1, 100)
            if probability <= 20:
                template = random.choice(templates[0]) # Квадраты
            if 20 < probability <= 45 :
                template = random.choice(templates[1]) # Линии
            if 45 < probability <= 70 :
                template = random.choice(templates[2]) # Маленькие уголки
            if 70 < probability <= 90 :
                template = random.choice(templates[3]) # Г-образные
            if probability >= 90:
                template = random.choice(templates[4]) # Большие уголки

            template_group = random.choice(templates)
            block = Block(random.choice(template_group), x, height - 150, field_x, field_y)
            blocks.append(block)
            x += block_width + gap
        return blocks

    blocks = generate_blocks()

    def can_place_block(block):
        """Проверка возможности размещения блока."""
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

    def is_game_over():
        """Проверяет, возможен ли ход."""
        for block in blocks:
            for row_shift in range(grid_size - len(block.template) + 1):
                for col_shift in range(grid_size - len(block.template[0]) + 1):
                    temp_block = Block(block.template, 0, 0, field_x, field_y)
                    temp_block.move(
                        field_x + col_shift * block_size,
                        field_y + row_shift * block_size,
                    )
                    if can_place_block(temp_block):
                        return False
        return True

    def place_block(block):
        """Размещение блока на поле."""
        nonlocal score
        for y, x in block.get_cells():
            field[y][x] = block.color
        score += sum(sum(row) for row in block.template)

    def clear_lines():
        """Очистка заполненных строк и столбцов."""
        nonlocal score
        rows_to_clear = []
        cols_to_clear = []

        for row in range(grid_size):
            if all(field[row][col] is not None for col in range(grid_size)):
                rows_to_clear.append(row)

        for col in range(grid_size):
            if all(field[row][col] is not None for row in range(grid_size)):
                cols_to_clear.append(col)

        for row in rows_to_clear:
            for col in range(grid_size):
                field[row][col] = None

        for col in cols_to_clear:
            for row in range(grid_size):
                field[row][col] = None

        #Подсчет очков
        score += len(rows_to_clear + cols_to_clear) * (grid_size * 3 + 5)

    running = True
    while running:
        global offset_x, offset_y

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
                for block in blocks:
                    if block.dragging:
                        block.dragging = False
                        block.snap_to_grid()
                        if can_place_block(block):
                            place_block(block)
                            clear_lines()
                            blocks.remove(block)
                            if not blocks:
                                blocks = generate_blocks()
                        else:
                            block.reset_position()

            if event.type == pygame.MOUSEMOTION:
                for block in blocks:
                    if block.dragging:
                        mouse_x, mouse_y = event.pos
                        square_x = mouse_x - offset_x
                        square_y = mouse_y - offset_y
                        block.move(square_x, square_y)

        # Проверяем победу
        if score >= 1000:
            show_victory_menu(score)

        # Проверяем проигрыш
        if is_game_over():
            show_game_over_menu(score)

        screen.fill(BG_COLOR)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        for row in range(grid_size):
            for col in range(grid_size):
                x = field_x + col * block_size
                y = field_y + row * block_size
                pygame.draw.rect(screen, GRAY, (x, y, block_size, block_size))
                pygame.draw.rect(screen, BLACK, (x, y, block_size, block_size), 2)
                if field[row][col]:
                    pygame.draw.rect(
                        screen, field[row][col], (x, y, block_size, block_size)
                    )
                    pygame.draw.rect(screen, BLACK, (x, y, block_size, block_size), 2)

        for block in blocks:
            block.draw()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
