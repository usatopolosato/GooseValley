import pytmx
from scripts.game.stacked_sprite import *
from scripts.game.tile import Tile
from random import uniform, choice


# Класс карты
class Scene:
    def __init__(self, app, map_name):
        # Приложение
        self.app = app
        # Название карты
        self.name = map_name
        # Карта, высота, ширина
        self.map = self.height = self.width = None
        # Загрузить карту и объекты
        self.load_scene(map_name)

    # Загрузить карту и объекты
    def load_scene(self, map_name):
        # Название карты
        self.name = map_name
        # Атрибуты карты
        self.attr = MAP_ATTRIBUTES[map_name]
        # Задний фон
        self.app.background = self.attr['background']
        # Карта
        self.map = pytmx.load_pygame(f'data/maps/{map_name}/road.tmx')
        # Высота
        self.height = self.map.height
        # Ширина
        self.width = self.map.width

        # Функция случайного угла поворота
        random_rotate = lambda: uniform(0, 360)
        # Функция случайного изменения позиции
        random_position = lambda pos: pos + vec2(uniform(-0.25, 0.25))

        # ID пустой клетки (всегда последняя в наборе тайлов)
        void_tile = len(self.app.cache.map_cache[map_name]['map'])
        # Проходим по всем клеткам
        for i in range(self.height):
            for j in range(self.width):
                tile_id = self.map.tiledgidmap[self.map.get_tile_gid(j, i, 0)]
                # Позиция объекта
                pos = vec2(j, i)
                if tile_id != void_tile:
                    Tile(self.app, map_name, tile_id, pos)
                    if tile_id - 1 in self.attr['barriers']:
                        if tile_id - 1 in self.attr['barriers_2x2']:
                            pos += vec2(0.5)
                        StackedSprite(self.app, str(tile_id), pos)
                else:
                    StackedSprite(self.app, choice(self.attr['objects']),
                                  random_position(pos), random_rotate())
        # Положение игрока
        pos = vec2(self.attr['player_position'][self.app.client.get_id()]) * TILE_SIZE
        # Положение финиша
        self.app.player.finish_line = vec2(self.attr['finish_line']) * TILE_SIZE
        # Смещение камеры
        self.app.player.camera_offset = pos
        # Положение игрока
        self.app.player.pos = pos
        # Поворачиваем игрока в нужном направление
        self.app.player.rotate(math.pi)
        # Запоминаем состояние
        self.app.player.remember()
        # Запоминаем состояние второй раз
        self.app.player.remember()
        # Костыль, который исправляет баг "разбитой машины"
        self.app.player.return_back()
        self.app.player.remember()
