from scripts.settings import *
import math


# Класс тайла
class Tile(pygame.sprite.Sprite):
    def __init__(self, app, map_name, tile_id, pos):
        super().__init__(app.tile_group)
        # Приложение
        self.app = app
        # Имя спрайта
        self.name = tile_id
        # Позиция спрайта
        self.pos = vec2(pos) * TILE_SIZE
        # Камера
        self.camera = app.camera
        # Основная группа спрайтов
        self.group = app.tile_group
        # Класс кеширования
        self.cache = app.cache.map_cache
        # Угол обзора
        self.viewing_angle = app.cache.viewing_angle
        # Словарь изображений
        self.rotated_sprites = self.cache[map_name]['map'][tile_id]
        # Угол поворота
        self.angle = 0
        # Позиция на экране
        self.screen_pos = vec2(0)

    # Перемещение спрайта
    def transform(self):
        pos = self.pos - self.camera.offset
        pos = pos.rotate_rad(self.camera.angle)
        pos.y += PLAYER_OFFSET - self.app.player.acceleration_offset
        self.screen_pos = pos + CENTER

    # Получение угла поворота
    def get_angle(self):
        # Вычисляем угол в градусах
        self.angle = -math.degrees(self.camera.angle) // self.viewing_angle
        # Преобразуем угол в число в диапазоне [0;NUMBER_ANGLES)
        self.angle = int(self.angle % NUMBER_ANGLES) % NUMBER_ANGLES

    # Получение изображения
    def get_image(self):
        # Получаем изображение
        self.image = self.rotated_sprites[self.angle]
        # Меняем размеры спрайта
        self.rect = self.image.get_rect(center=self.screen_pos)

    # Изменение спрайта
    def update(self):
        self.transform()
        self.get_angle()
        self.get_image()
