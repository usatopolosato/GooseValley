import pygame
from scripts.gui.demonstration_car import DemonstrationSprite


# Класс платформы(мини-приложение) для показа выбранной машинки.
class Platform:
    def __init__(self, screen, cache, name_car):
        # Экран
        self.screen = screen
        # Часы
        self.clock = pygame.time.Clock()
        # Время, прошедшее с начала запуска
        self.time = 0
        # Время, прошедшее с прошлой работы цикла
        self.delta_time = 0.01
        # Экземпляр класса кеширования
        self.cache = cache
        # Группа спрайтов, изображенных на платформе.
        self.demo_group = pygame.sprite.Group()
        # Экземпляр для показа на платформе по переданному названию машинки.
        DemonstrationSprite(self, name=name_car, pos=(screen.get_width() // 2,
                                                      screen.get_height() // 2))

    # Получение времени, прошедшего с начала запуска.
    def get_time(self):
        self.time = pygame.time.get_ticks() * 0.001

    # Изменение объектов
    def update(self):
        self.demo_group.update()
        self.delta_time = self.clock.tick()

    # Рисование объектов
    def draw(self):
        # Делаем фон прозрачным.
        self.screen.fill(pygame.Color('#004953'))
        self.screen.set_colorkey(pygame.Color('#004953'))
        # Отрисовываем спрайты.
        self.demo_group.draw(self.screen)

    # Основной цикл.
    def run(self):
        self.get_time()
        self.update()
        self.draw()
