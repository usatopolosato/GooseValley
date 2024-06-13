import pygame.mask
import pytmx
from threading import Thread
from scripts.settings import *


# Класс кеширования изображений
class Cache:
    def __init__(self):
        # Словарь изображений для карт
        self.map_cache = {}
        # Словарь изображений для объектов
        self.stacked_sprite_cache = {}
        # Шаг в градусах между повёрнутыми изображениями
        self.viewing_angle = 360 // NUMBER_ANGLES
        # Толщина обводки
        self.outline_thickness = 2
        # Получение изображений для объектов
        t = Thread(target=self.get_stacked_sprite_cache(), daemon=True)
        t.start()
        t.join()
        # Получение изображений для тайлов карт
        self.get_map_cache()

    # Получение изображений для тайлов карт
    def get_map_cache(self):
        # Перебираем все карты
        for map_name in MAP_ATTRIBUTES:
            # Получаем атрибуты
            attrs = MAP_ATTRIBUTES[map_name]
            path = attrs['path']
            # Загружаем тайлы
            tiles = pytmx.load_pygame(f'{path}/tiles.tmx')
            # Загружыем миникарту
            minimap = pytmx.load_pygame(f'{path}/minimap.tmx')
            # Высота
            height = tiles.height
            # Ширина
            width = tiles.width
            # Создаём словарь для тайлов
            self.map_cache[map_name] = {}
            # Тайлы карты
            self.map_cache[map_name]['map'] = {}
            # Тайлы миникарты
            self.map_cache[map_name]['minimap'] = {}

            k = 2
            threads = [Thread(target=self.map_processing, daemon=True,
                              args=(height * i // k, height * (i + 1) // k, 0,
                                    width, map_name, tiles, minimap, attrs))
                       for i in range(k)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

    def map_processing(self, i_0, i_1, j_0, j_1, map_name, tiles, minimap, attrs):
        for i in range(i_0, i_1):
            for j in range(j_0, j_1):
                self.tile_processing(i, j, map_name, tiles, minimap, attrs)

    def tile_processing(self, i, j, map_name, tiles, minimap, attrs):
        # Получаем индекс тайла
        tile_id = tiles.get_tile_gid(j, i, 0)
        # Получаем изображение тайла
        image = tiles.get_tile_image(j, i, 0)
        # Получаем изображение тайла миникарты
        minimap_image = minimap.get_tile_image(j, i, 0)
        # Создаём словарь для повёрнутых изображений
        self.map_cache[map_name]['map'][tile_id] = {}
        # Получаем повёрнутые изображения
        self.run_prerender_tiles(map_name, tile_id, image, attrs)
        # Получаем тайл для миникарты
        self.run_prerender_minimap_tiles(map_name, tile_id, minimap_image, attrs)
        if tile_id - 1 in attrs['barriers']:
            # Создаём новый словарь словарей
            self.stacked_sprite_cache[str(tile_id)] = {
                'rotated_sprites': {},
                'masks': {},
            }
            # Атрибуты объекта
            sprite_attrs = {'path': f'data/maps/{map_name}/barriers/{tile_id - 1}.png',
                            'number_layers': attrs['number_layers'],
                            'scale': attrs['scale'],
                            'mask_layer': attrs['barrier_mask_layer'],
                            'y_offset': -50,
                            }
            # Слои 3D модели
            layer_array = self.get_layer_array(sprite_attrs)
            # Получение повёрнутых изобажений
            self.run_prerender_sprite(str(tile_id), layer_array, sprite_attrs)

    def run_prerender_minimap_tiles(self, map_name, tile_id, image, attr):
        # Изменяем размер тайла
        image = pygame.transform.scale(image, vec2(image.get_size()) * attr['minimap_scale'])
        # Создаём поверхность для изображение
        sprite_surface = pygame.Surface(image.get_size())
        # Оптимизация: заполняем ненужным цветом
        sprite_surface.fill(pygame.Color('khaki'))
        # Делаем этот цвет прозрачным
        sprite_surface.set_colorkey(pygame.Color('khaki'))
        # Переносим изображение
        sprite_surface.blit(image, (0, 0))
        # Добавляем в словарь словарей класса
        self.map_cache[map_name]['minimap'][tile_id] = sprite_surface

    # Получение повёрнутых изображений тайлов
    def run_prerender_tiles(self, map_name, tile_id, image, attr):
        # Изменяем размер тайла
        image = pygame.transform.scale(image, vec2(image.get_size()) * attr['scale'])
        # Перебираем углы
        for angle in range(NUMBER_ANGLES):
            # Создаём поверхность для изображение
            surface = pygame.Surface(image.get_size())
            # Поворачиваем поверхность
            surface = pygame.transform.rotate(surface, angle * self.viewing_angle)
            # Создаём поверхность, на который поместятся все изображения
            sprite_surface = pygame.Surface([surface.get_width(), surface.get_height()])
            # Оптимизация: заполняем ненужным цветом
            sprite_surface.fill(pygame.Color('khaki'))
            # Делаем этот цвет прозрачным
            sprite_surface.set_colorkey(pygame.Color('khaki'))
            # Поворачиваем изображение
            layer = pygame.transform.rotate(image, angle * self.viewing_angle)
            # Переносим изображение
            sprite_surface.blit(layer, (0, 0))
            # Добавляем в словарь словарей класса
            self.map_cache[map_name]['map'][tile_id][angle] = sprite_surface

    # Получение изображений для объектов
    def get_stacked_sprite_cache(self):
        for object_name in STACKED_SPRITE_ATTRIBUTES:
            # Создаём новый словарь словарей
            self.stacked_sprite_cache[object_name] = {
                'rotated_sprites': {},
                'masks': {},
            }
            # Атрибуты объекта
            attrs = STACKED_SPRITE_ATTRIBUTES[object_name]
            # Слои 3D модели
            layer_array = self.get_layer_array(attrs)
            # Получение повёрнутых изобажений
            self.run_prerender_sprite(object_name, layer_array, attrs)

    # Получение слоёв 3D модели
    def get_layer_array(self, attrs):
        # Исходное изображение
        sprite_sheet = pygame.image.load(attrs['path']).convert_alpha()
        # Изменяем размер изображения
        sprite_sheet = pygame.transform.scale(sprite_sheet,
                                              vec2(sprite_sheet.get_size()) * attrs['scale'])
        # Ширина слоя
        sheet_width = sprite_sheet.get_width()
        # Высота слоя
        sheet_height = sprite_sheet.get_height()
        # Высота изображения
        sprite_height = sheet_height // attrs['number_layers']
        # Правильная высота слоя
        sheet_height = sprite_height * attrs['number_layers']
        # Список слоёв
        layer_array = []
        # Перебираем каждый слой
        for y in range(0, sheet_height, sprite_height):
            # Вырезаем изображение
            sprite = sprite_sheet.subsurface((0, y, sheet_width, sprite_height))
            # Добавляем изображение
            layer_array.append(sprite)
        # Возвращаем в обратном порядке (слои идут снизу вверх)
        return layer_array[::-1]

    # Получение повёрнутых изобажений
    def run_prerender_sprite(self, object_name, layer_array, attrs):
        outline = attrs.get('outline', False)
        # Перебираем углы
        for angle in range(NUMBER_ANGLES):
            # Создаём поверхность для изображение
            surface = pygame.Surface(layer_array[0].get_size())
            # Поворачиваем поверхность
            surface = pygame.transform.rotate(surface, angle * self.viewing_angle)
            # Создаём поверхность, на который поместятся все изображения
            sprite_surface = pygame.Surface([surface.get_width(), surface.get_height()
                                             + attrs['number_layers'] * attrs['scale']])
            # Оптимизация: заполняем ненужным цветом
            sprite_surface.fill(pygame.Color('khaki'))
            # Делаем этот цвет прозрачным
            sprite_surface.set_colorkey(pygame.Color('khaki'))
            # Перебираем все слои
            for i, layer in enumerate(layer_array):
                # Поворачиваем слой
                layer = pygame.transform.rotate(layer, angle * self.viewing_angle)
                # Размещаем несколько раз для придания большой объёмности
                for j in range(attrs['scale'] + 1):
                    sprite_surface.blit(layer, (0, i * attrs['scale'] + j))
            # Обводка изображений
            if outline:
                outline_coordinates = pygame.mask.from_surface(sprite_surface).outline()
                pygame.draw.polygon(sprite_surface, 'black',
                                    outline_coordinates, self.outline_thickness)
            # Отражаем изображение
            image = pygame.transform.flip(sprite_surface, True, True)
            # Добавляем в словарь словарей класса
            self.stacked_sprite_cache[object_name]['rotated_sprites'][angle] = image
        mask = layer_array[attrs['mask_layer']]
        for angle in range(NUMBER_ANGLES):
            # Создаём повехность для изображение
            surface = pygame.Surface(mask.get_size())
            # Поворачиваем поверхность
            surface = pygame.transform.rotate(surface, angle * self.viewing_angle)
            # Создаём поверхность, на который поместятся все изображения
            sprite_surface = pygame.Surface([surface.get_width(), surface.get_height()
                                             + attrs['number_layers'] * attrs['scale']])
            # Оптимизация: заполняем ненужным цветом
            sprite_surface.fill(pygame.Color('khaki'))
            # Делаем этот цвет прозрачным
            sprite_surface.set_colorkey(pygame.Color('khaki'))
            # Поворачиваем слой
            layer = pygame.transform.rotate(mask, angle * self.viewing_angle)
            # Размещаем несколько раз для придания большой объёмности
            sprite_surface.blit(layer, (0, 0))
            # Отражаем изображение
            image = pygame.transform.flip(sprite_surface, True, True)
            # Добавляем в словарь словарей класса
            self.stacked_sprite_cache[object_name]['masks'][angle] = pygame.mask.from_surface(image)
