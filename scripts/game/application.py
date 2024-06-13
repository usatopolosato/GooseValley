from scripts.settings import *
from scripts.game.player import Player
from scripts.game.scene import Scene
from scripts.game.camera import Camera
from scripts.multiplayer.client import Client
from scripts.game.game_interface import GameInterface
from scripts.game.minimap import Minimap


# Класс приложения
class App:
    def __init__(self, client, cache, name_car, fps_counter, sound, map_name='green_forest'):
        # Клиент
        self.client = client
        self.client.set_app(self)
        # Экран
        self.screen = pygame.display.set_mode(WINDOW_SIZE * 2)
        # Поверхность окна
        self.window = pygame.Surface(WINDOW_SIZE)
        # Часы
        self.clock = pygame.time.Clock()
        # Время запуска приложения
        self.start_time = pygame.time.get_ticks() * 0.001
        # Время, прошедшее с начала запуска
        self.time = 0
        # Время, прошедшее с прошлой работы цикла
        self.delta_time = 0.01
        # Экземпляр класса кеширования
        self.cache = cache
        # Основная группа спрайтов
        self.main_group = pygame.sprite.LayeredUpdates()
        # Группа тайлов карты
        self.tile_group = pygame.sprite.Group()
        # Группа спрайтов для столкновений
        self.collision_group = pygame.sprite.Group()
        # Камера
        self.camera = Camera()
        # Игрок
        self.player = Player(self, name_car)
        # Словарь игроков
        self.players = {}
        # Переменная, отвечающая за то, показывать ли фпс или нет.
        self.fps_counter = fps_counter
        # Уровень звука
        self.sound = sound
        # Число кругов
        self.number_of_laps = 0
        # Всего кругов
        self.max_number_of_laps = MAP_ATTRIBUTES[map_name]['number_of_laps']
        # Скорость
        self.speed = 0
        # Интерфейс в игре
        self.labels = GameInterface(self)
        # Миникарта
        self.minimap = Minimap(self, map_name)
        # Состояние игры
        self.state = 'beginning'
        # Фон карты
        self.background = None
        self.client.update(self.player)
        # Экземпляр класса карты
        self.scene = Scene(self, map_name)
        # Обновление положение других игроков
        pygame.time.set_timer(CLIENT_UPDATE, 100)
        # Окончание начала гонки
        pygame.time.set_timer(END_BEGINNING, 10000)
        # Окончание заезда
        pygame.time.set_timer(END_GAME, 420000)

    # Проверка окончания заезда
    def check_end_race(self):
        return self.number_of_laps > self.max_number_of_laps

    # Просмотр всех событий
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == CLIENT_UPDATE:
                self.client.update(self.player)
            if event.type == END_BEGINNING:
                self.state = 'running'
                self.start_time = pygame.time.get_ticks() * 0.001
                pygame.time.set_timer(END_BEGINNING, 0)
            if event.type == END_GAME:
                return False
        # Проверка окончания заезда
        if self.check_end_race() and self.state != 'ending':
            self.client.finish()
            self.state = 'ending'
        return True

    # Получение времени, прошедшего с начала запуска
    def get_time(self):
        self.time = pygame.time.get_ticks() * 0.001 - self.start_time

    # Изменение объектов
    def update(self):
        pygame.display.set_caption(f'Speed Racer')
        self.main_group.update()
        self.tile_group.update()
        self.delta_time = self.clock.tick()

    # Рисование объектов
    def draw(self):
        # Заполняем фоновым цветом
        self.window.fill(self.background)
        # Рисуем тайлы
        self.tile_group.draw(self.window)
        # Рисуем объекты
        self.main_group.draw(self.window)
        # Увеличиваем поверхность
        large_window = pygame.transform.scale(self.window, (WINDOW_SIZE) * 2)
        # Переносим поверхность
        self.screen.blit(large_window, (0, 0))
        # Рисуем всю информацию
        self.labels.draw()
        self.minimap.draw()
        pygame.display.flip()

    # Основной цикл
    def run(self):
        while self.check_events():
            self.get_time()
            self.update()
            self.draw()
        self.client.exit_the_game()
        pygame.time.set_timer(CLIENT_UPDATE, 0)
        pygame.time.set_timer(END_BEGINNING, 0)
        pygame.display.flip()
        return True
