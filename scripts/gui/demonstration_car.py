from scripts.settings import *
import math


# Класс для демонстрации машинки в главном меню.
class DemonstrationSprite(pygame.sprite.Sprite):
    def __init__(self, app, name, pos):
        super().__init__(app.demo_group)
        # Приложение.
        self.app = app
        # Имя спрайта.
        self.name = name
        # Позиция спрайта.
        self.pos = vec2(pos)
        # Группа спрайта.
        self.group = app.demo_group
        # Атрибуты.
        self.attrs = STACKED_SPRITE_ATTRIBUTES[name]
        # Класс кеширования.
        self.cache = app.cache.stacked_sprite_cache
        # Угол обзора.
        self.viewing_angle = app.cache.viewing_angle
        # Словарь изображений.
        self.rotated_sprites = self.cache[name]['rotated_sprites']
        # Угол поворота.
        self.angle = 0

    # Получение угла поворота.
    def get_angle(self):
        # Вычисляем угол в градусах.
        self.angle = -math.degrees(self.app.time) // self.viewing_angle
        # Преобразуем угол в число в диапазоне [0;NUMBER_ANGLES).
        self.angle = int(self.angle % NUMBER_ANGLES)

    # Изменение спрайта.
    def update(self):
        self.get_angle()
        self.get_image()

    # Получение изображения.
    def get_image(self):
        # Получаем повернутое изображение и его размеры.
        image = self.rotated_sprites[self.angle]
        self.image = pygame.transform.scale(image, vec2(image.get_size()) * 3)
        self.rect = self.image.get_rect(center=self.pos)
