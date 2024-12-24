from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        """Инициализация позиции и цвета объекта на игровом поле."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод."""
        raise NotImplementedError(
            "Этот метод должен быть переопределён в подклассе."
        )

    def draw_rectangle(self, position):
        """Метод для отрисовки прямоугольника."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def draw(self):
        """Метод для отрисовки яблока на игровой поверхности."""
        self.draw_rectangle(position=self.position)

    @staticmethod
    def randomize_position(snake_positions):
        """Метод для установки случайного положения яблоку."""
        while True:
            width = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            height = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (width, height) not in snake_positions:
                return (width, height)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        """Начальное состояние змейки."""
        super().__init__(position, body_color)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT  # По умолчанию змейка движется вправо
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод для обновления направления движения змейки."""
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
        self.positions.insert(0, new_head)
        # Удаляем хвост, если текущая длина превышает максимальное значение
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод для отрисовки змейки на игровой поверхности."""
        for position in self.positions[:-1]:
            self.draw_rectangle(position=position)

        # Отрисовка головы змейки
        self.draw_rectangle(position=self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод, возвращающий позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод, сбрасывающий змейку в начальное состояние."""
        # Сбрасываем длину змейки.
        self.length = 1
        # Сбрасываем позицию змейки.
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # Изменяем напрвление движения случайным образом
        self.direction = choice([RIGHT, LEFT, UP, DOWN])


def handle_keys(game_object):
    """Функция для обработки действий пользователя."""
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


def check_eat_apple(snake, apple):
    """Функция для проверки съела ли змейка яблоко."""
    # Проверяем находится ли голова змейки на позиции яблока.
    if snake.get_head_position() == apple.position:
        # Фиксируем координаты хвоста змейки.
        x_tail, y_tail = snake.positions[-1]
        # Если длина змейки больше 1.
        if len(snake.positions) > 1:
            # Определяем координаты предпоследней точки.
            x_prev, y_prev = snake.positions[-2]
            # Определяем смещение хвоста.
            diff_x = x_prev - x_tail
            diff_y = y_prev - y_tail
        # Если голова = хвосту, то удлиняем змейку по направлению движения.
        else:
            diff_x = snake.direction[0] * GRID_SIZE
            diff_y = snake.direction[1] * GRID_SIZE
        # Добавляем хвост в конец.
        snake.positions.append((x_tail - diff_x, y_tail - diff_y))
        # Определяем новую позицию яблока.
        apple.position = Apple.randomize_position(
            snake_positions=snake.positions
        )


def check_snake_collide(snake, apple):
    """Функция для проверки столкнулась ли змейка с собой."""
    # Проверяем, если длина змейки > 1 и голова на позиции змейки.
    if (len(snake.positions) > 1
            and snake.get_head_position() in snake.positions[1:]):
        # Очищаем экран.
        screen.fill(BOARD_BACKGROUND_COLOR)
        # Сбрасываем змейку в первоначальное состояние.
        snake.reset()
        # Определяем новую позицию яблока.
        apple.position = Apple.randomize_position(
            snake_positions=snake.position
        )


def main():
    """Основной цикл игры."""
    # Инициализация PyGame:
    pygame.init()
    # Создание экземпляров класса.
    snake = Snake()
    apple = Apple(
        position=Apple.randomize_position(snake_positions=snake.position),
        body_color=APPLE_COLOR
    )

    while True:
        # Делаем паузу, чтобы увидеть изменения.
        clock.tick(SPEED)
        # Обрабатываем действия пользователя.
        handle_keys(snake)
        # Изменяем напрвление движения змейки.
        snake.update_direction()
        # Двигаем змейку.
        snake.move()
        # Проверяем съела ли змейка яблоко.
        check_eat_apple(snake, apple)
        check_snake_collide(snake, apple)
        # Отрисовывем яблоко.
        apple.draw()
        # Отрисовывем змейку.
        snake.draw()
        # Обновляем поле.
        pygame.display.update()


if __name__ == '__main__':
    main()
