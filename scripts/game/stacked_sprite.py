from scripts.settings import *
import math


# Класса спрайта, использующего технику sprite stacking
class StackedSprite(pygame.sprite.Sprite):
    def __init__(self, app, name, pos, rot=0):
        super().__init__(app.main_group, app.collision_group)
        # Приложение
        self.app = app
        # Имя спрайта
        self.name = name
        # Позиция спрайта
        self.pos = vec2(pos) * TILE_SIZE
        # Камера
        self.camera = app.camera
        # Основная группа спрайтов
        self.group = app.main_group
        # Атрибуты
        self.attrs = STACKED_SPRITE_ATTRIBUTES.get(name, {'y_offset': -10})
        # Смещение по координате y
        self.y_offset = vec2(0, self.attrs.get('y_offset', 0))
        # Класс кеширования
        self.cache = app.cache.stacked_sprite_cache
        # Угол обзора
        self.viewing_angle = app.cache.viewing_angle
        # Словарь изображений
        self.rotated_sprites = self.cache[name]['rotated_sprites']
        # Словарь масок
        self.masks = self.cache[name]['masks']
        # Угол поворота
        self.angle = 0
        # Позиция на экране
        self.screen_pos = vec2(0)
        # Начальный угол поворота объекта
        self.rot = (rot % 360) // self.viewing_angle
        # Загружаем изображения
        self.get_image()

    # Изменить имя(изображения) спрайта
    def set_name(self, name):
        # Имя спрайта
        self.name = name
        # Атрибуты
        self.attrs = STACKED_SPRITE_ATTRIBUTES[name]
        # Словарь изображений
        self.rotated_sprites = self.cache[name]['rotated_sprites']

    # Перемещение спрайта
    def transform(self):
        pos = self.pos - self.camera.offset
        pos = pos.rotate_rad(self.camera.angle)
        pos.y += PLAYER_OFFSET - self.app.player.acceleration_offset
        self.screen_pos = pos + CENTER

    # Изменение высоты объекта
    def change_layer(self):
        # Устанавливаем слой в зависимости от положения на экране
        self.group.change_layer(self, self.screen_pos.y)

    # Получение угла поворота
    def get_angle(self):
        # Вычисляем угол в градусах
        self.angle = -math.degrees(self.camera.angle) // self.viewing_angle + self.rot
        # Преобразуем угол в число в диапазоне [0;NUMBER_ANGLES)
        self.angle = int(self.angle % NUMBER_ANGLES) % NUMBER_ANGLES

    # Получение изображения
    def get_image(self):
        # Получаем изображение
        self.image = self.rotated_sprites[self.angle]
        # Получаем маску
        self.mask = self.masks[self.angle]
        # Меняем размеры спрайта
        self.rect = self.image.get_rect(center=self.screen_pos + self.y_offset)

    # Изменение спрайта
    def update(self):
        self.transform()
        self.get_angle()
        self.get_image()
        self.change_layer()
