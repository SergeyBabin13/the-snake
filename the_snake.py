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
class GameObject:
    """
    Класс для представления объекта игры.

    Attributes:
        body_color tuple[int, int, int]:
            Цвет объекта.
        position tuple[int, int]:
            Координаты объекта в игровом окне. По умолчанию центр окна.
    """

    def __init__(
        self,
        body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR,
        position: tuple[int, int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
    ) -> None:
        """
        Инициализирует объект с заданным цветом и координатами в игровом окне.

        Args:
            body_color tuple[int, int, int]:
                Цвет объекта.
            position tuple[int, int]:
                Координаты объекта в игровом окне. По умолчанию центр окна.
        """
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Определяет наличие метода для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """
    Дочерний класс для представления объекта игры - яблоко.

    Attributes:
        body_color tuple[int, int, int]: Цвет объекта яблоко.
        position tuple[int, int]:
            Позиция объекта яблоко в игровом окне. По умолчанию None.
    """

    def __init__(
        self,
        body_color: tuple[int, int, int] = APPLE_COLOR,
        position=None,
    ) -> None:
        """
        Инициализирует объект яблоко с заданным цветом и координатами
        в игровом окне.

        Args:
            body_color tuple[int, int, int]:
                Цвет объекта яблоко. По умолчанию красного.
            position tuple[int, int]:
                Позиция объекта яблоко в игровом окне. По умолчанию None.
        """
        super().__init__(body_color, position)

    def randomize_position(self) -> tuple[int, int]:
        """Определяет рандомную позицию яблока в игровом окне.

        Функция рандомно определяет координаты по осям x и y
        с учетом размера игрового поля.

        Returns:
        tuple[int, int]: Кортеж двух целых чисел.
        """
        position_width: int = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        position_height: int = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (position_width, position_height)
        return self.position

    # Метод draw класса Apple
    def draw(self):
        """Отрисовывает объект яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс для представления объекта игры - змейка.

    Attributes:
        body_color tuple[int, int, int]:
            Цвет объекта змейка. По умолчанию зеленого.
        position tuple[int, int]:
            Позиция объекта змейка в игровом окне. По умолчанию центр окна.
        positions list:
            Список позиций всех элементов змейки. По умолчанию список пуст.
        length int:
            Количество элементов в змейке. По умолчанию 1.
        direction tuple[int, int]:
            Направление движения змейки в текущий момент. По умолчанию вправо.
        next_direction tuple[int, int]:
            Направление движения змейки в текущий момент. По умолчанию вправо.
        last:
            Позиция хвоста змейки в игровом окне. По умолчанию None.
    """

    def __init__(
        self,
        body_color: tuple[int, int, int] = SNAKE_COLOR,
        position: tuple[int, int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        positions: list = [],
        length: int = 1,
        direction: tuple[int, int] = RIGHT,
        next_direction=None,
        last=None,
    ) -> None:
        """
        Класс для представления объекта игры - змейка.

        Args:
            body_color tuple[int, int, int]:
                Цвет объекта змейка.
            position tuple[int, int]:
                Позиция объекта змейка в игровом окне. По умолчанию центр окна.
            positions list:
                Список позиций всех элементов змейки. По умолчанию список пуст.
            length int:
                Количество элементов в змейке. По умолчанию 1.
            direction tuple[int, int]:
                Направление движения змейки в текущий момент.
                По умолчанию вправо.
            next_direction tuple[int, int]:
                Направление движения змейки в текущий момент.
                По умолчанию вправо.
            last:
                Позиция хвоста змейки в игровом окне. По умолчанию None.
        """
        super().__init__(body_color, position)
        self.positions = positions
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.last = last
        list.insert(positions, 0, position)

    def get_head_position(
        self,
        positions: list[tuple[int, int]]
    ) -> tuple[int, int]:
        """Возвращает позицию головного элемента змейки.

        Args:
            positions list: Список позиций всех элементов змейки.

        Returns:
        tuple[int, int]: Кортеж двух целых чисел.
        """
        return positions[0]

    def move(self) -> None:
        """Определяет позицию головного элемента змейки при движении.
        Убирает след змейки при превышении её длины.
        """
        head: tuple[int, int] = self.get_head_position(self.positions)
        if self.direction == RIGHT:
            dx: int = (head[0] + RIGHT[0] * GRID_SIZE) % SCREEN_WIDTH
            dy: int = head[1]
        elif self.direction == LEFT:
            dx = (head[0] + LEFT[0] * GRID_SIZE)
            if dx < 0:
                dx += SCREEN_WIDTH
            dy = head[1]
        elif self.direction == UP:
            dx = head[0]
            dy = (head[1] + UP[1] * GRID_SIZE)
            if dy < 0:
                dy += SCREEN_HEIGHT
        elif self.direction == DOWN:
            dx = head[0]
            dy = (head[1] + DOWN[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_of_head: tuple[int, int] = (dx, dy)
        list.insert(self.positions, 0, new_of_head)
        self.last = self.positions[len(self.positions) - 1]
        if len(self.positions) > self.length:
            del self.positions[-1]

    def reset(self) -> None:
        """Возвращает змейку в позицию по умолчанию в игровом поле
        с рандомным выбором направления движения.
        """
        self.positions = []
        list.insert(self.positions, 0, self.position)
        self.length = 1
        self.direction = choice([RIGHT, LEFT, UP, DOWN])

    # Метод draw класса Snake
    def draw(self):
        """Отрисовывает объект змейка на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает ввод команд пользователя с клавиатуры.

    Args:
        game_object: Объект игры, для которого осуществляется перемещение.
    """
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
    """Определяет основной игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    apple.randomize_position()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position == snake.positions[0]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.length += 1
            apple.randomize_position()
        if snake.positions[0] in snake.positions[4::]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
