import pygame.sprite
from scripts.settings import *


# Камера для смещения по диагонали.
class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # Смещаем цель(камеры) и берем процент чтобы не выйти за границы отрисованного заднего фона.
    def apply(self, object):
        object.rect = object.rect.move(self.dx, self.dy)
        object.rect.x %= (WINDOW_WIDTH * 3)
        object.rect.y %= (WINDOW_HEIGHT * 3)

    # Вычисляем смещение.
    def update(self, target):
        self.dx = (WINDOW_WIDTH * 3) // 2 - target.rect.x - target.rect.w // 2
        self.dy = (WINDOW_HEIGHT * 3) // 2 - target.rect.y - target.rect.h // 2


# Класс для создания цели для камеры.
class Target(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, main_group):
        super().__init__(main_group)
        self.image = self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 30
        self.rect.y = pos_y * 30

    # Функция, для смещения координат цели для движения по диагонали.
    def move(self):
        self.rect.x += 5
        self.rect.y += 5


# Тайл для главного меню.
class SquareMain(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, size, color, main_group):
        super().__init__(main_group)
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        pygame.draw.rect(self.image, 'white', (0, 0, size, size), 4)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * size
        self.rect.y = pos_y * size


# Тайл для лобби.
class SquareLobby(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, size, color, main_group):
        super().__init__(main_group)
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * size
        self.rect.y = pos_y * size


# Задний фон для главного меню.
class BackgroundMain:
    def __init__(self, size, color):
        # Создаем BACKGROUND определенных размеров и в определенном стиле.
        self.size = size
        self.image = pygame.Surface((WINDOW_WIDTH * 3, WINDOW_HEIGHT * 9))
        self.main_group = pygame.sprite.Group()
        # Cоздаем объект класса камера.
        self.camera = Camera()
        self.w = int((WINDOW_WIDTH * 3) // size)
        self.h = int((WINDOW_HEIGHT * 3) // size)
        # Создаем объект внимания для класса камеры.
        self.target = Target(self.w // 2, self.h // 2, self.main_group)
        # Создаем тайлы на заднем фоне.
        for y in range(-1, self.h):
            for x in range(-1, self.w):
                SquareMain(x, y, size, color, self.main_group)

    # Эффект движения по диагонaлe на заднем фоне. Отрисовываем тайлы.
    def update(self):
        self.image.fill('white')
        self.target.move()
        for sprite in self.main_group:
            self.camera.apply(sprite)
        self.camera.update(self.target)
        self.main_group.draw(self.image)


# Задний фон для лобби.
class BackgroundLobby(BackgroundMain):
    def __init__(self, size, colors):
        super().__init__(size, colors[0])
        # Создаем BACKGROUND определенных размеров и в определенном стиле.
        self.size = size
        self.image = pygame.Surface((WINDOW_WIDTH * 3, WINDOW_HEIGHT * 9))
        self.main_group = pygame.sprite.Group()
        # Cоздаем объект класса камера.
        self.camera = Camera()
        self.w = int((WINDOW_WIDTH * 3) // size)
        self.h = int((WINDOW_HEIGHT * 3) // size)
        # Создаем объект внимания для класса камеры.
        self.target = Target(self.w // 2, self.h // 2, self.main_group)
        # Создаем тайлы на заднем фоне.
        # Задний фон в виде клетчатого поля.
        for y in range(self.h):
            if y % 2 == 0:
                for x in range(self.w - 1, -1, -1):
                    if x % 2 == 0:
                        SquareLobby(x, y, size, colors[1], self.main_group)
                    else:
                        SquareLobby(x, y, size, colors[0], self.main_group)
            else:
                for x in range(self.w - 1, -1, -1):
                    if x % 2 == 0:
                        SquareLobby(x, y, size, colors[0], self.main_group)
                    else:
                        SquareLobby(x, y, size, colors[1], self.main_group)
