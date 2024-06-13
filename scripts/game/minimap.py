import pytmx
from scripts.settings import *


# Класс миникарты
class Minimap:
    def __init__(self, app, map_name, pos=vec2(10, 450)):
        # Приложение
        self.app = app
        # Тайлы миникарты
        self.tiles = self.app.cache.map_cache[map_name]['minimap']
        # Позиция миникарты
        self.pos = pos
        # Карта
        self.map = pytmx.load_pygame(f'data/maps/{map_name}/road.tmx')
        # Высота
        self.height = self.map.height
        # Ширина
        self.width = self.map.width
        # Размер тайла миникарты
        self.tile_size = int(55 * MAP_ATTRIBUTES[map_name]['minimap_scale'])
        # Миникарта
        self.minimap = pygame.Surface(vec2(self.width, self.height) * self.tile_size)
        # Инициализация миникарты
        self.init_minimap()

    # Инициализация миникарты
    def init_minimap(self):
        # Заполняем цветом
        self.minimap.fill(pygame.Color('khaki'))
        # Делаем его прозрачным
        self.minimap.set_colorkey(pygame.Color('khaki'))
        # Просматриваем все тайлы
        for i in range(self.height):
            for j in range(self.width):
                # Получаем id тайла
                tile_id = self.map.tiledgidmap[self.map.get_tile_gid(j, i, 0)]
                # Вычисляем позицию тайла
                pos = vec2(j, i) * self.tile_size
                # Получаем изображение
                image = self.tiles[tile_id]
                # Переносим изображение
                self.minimap.blit(image, pos)

    # Рисование миникарты на экран
    def draw(self):
        self.app.screen.blit(self.minimap, self.pos)

        for player in self.app.players.values():
            pos = player.pos * self.tile_size / TILE_SIZE
            pos = pos + vec2(2.5) + self.pos
            color = STACKED_SPRITE_ATTRIBUTES[player.name]['color']
            pygame.draw.ellipse(self.app.screen, pygame.Color(color), (*pos, 10, 10), 0)

        pos = self.app.player.pos * self.tile_size / TILE_SIZE
        pos = pos + vec2(2.5) + self.pos
        color = STACKED_SPRITE_ATTRIBUTES[self.app.player.name]['color']
        pygame.draw.ellipse(self.app.screen, pygame.Color(color), (*pos, 10, 10), 0)
        pygame.draw.ellipse(self.app.screen, pygame.Color('black'), (*pos, 10, 10), 2)
