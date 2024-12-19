from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameOject:
    """Базовый класс, от которого наследуются другие игровые объекты."""
    # Инициализация позиции и цвета объекта на игровом поле.
    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    # Абстрактный метод, который будут переопределен в дочерних классах.
    def draw(self):
        pass


class Apple(GameOject):
    """
    Класс, унаследованный от GameObject, описывающий яблоко и действия с ним.
    """
    # Задание цвета и установка случайного положения яблока.
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод для отрисовки яблока на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Метод для установки случайного положения яблоку."""
        width = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        height = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (width, height)


class Snake(GameOject):
    """
    Класс, унаследованный от GameObject, описывающий змейку и её поведение.
    """
    # Начальное состояние змейки.
    def __init__(self):
        super().__init__()
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = (1, 0)  # По умолчанию змейка движется вправо
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод для обновления направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        """Метод для обновления позиции змейки."""
        # Получаем текущее положение головы.
        old_head_x, old_head_y = self.get_head_position()
        # Получаем новую позицию головы.
        new_head_x = (
            old_head_x + self.direction[0] * GRID_SIZE
        ) % SCREEN_WIDTH  # Обработка x-края.
        new_head_y = (
            old_head_y + self.direction[1] * GRID_SIZE
        ) % SCREEN_HEIGHT  # Обработка y-края.
        new_head = (new_head_x, new_head_y)
        # Добавляем новую голову в начало.
        self.position.insert(0, new_head)
        # Удаляем хвост, если текущая длина превышает максимальное значение
        if len(self.position) > self.length:
            self.position.pop()
        
    def draw(self):
        """Метод для отрисовки змейки на игровой поверхности."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
    
    def get_head_position(self):
        """Метод, возвращающий позицию головы змейки"""
        return self.position[0]
    
    def reset(self):
        """Метод, сбрасывающий змейку в начальное состояние"""
        # Сбрасываем длину змейки.
        self.length = 1
        # Сбрасываем позицию змейки.
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # Изменяем напрвление движения случайным образом
        x_right = (1, 0)
        x_left = (-1, 0)
        y_right = (0, 1)
        y_left = (0, -1)
        self.direction = choice[x_right, x_left, y_right, y_left]


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(apple)
        apple.randomize_position()
        apple.draw()
        pygame.display.update()

        # Тут опишите основную логику игры.
        # ...


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
