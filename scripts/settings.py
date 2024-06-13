import pygame
import csv


# Функция для получения ip и порта
def get_host_port():
    with open('data/files/host_and_port.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        host, port = list(reader)[0]
    return host, int(port)


# Обновление клиента
CLIENT_UPDATE = pygame.USEREVENT + 1
# Конец старта
END_BEGINNING = pygame.USEREVENT + 2
# Конец заезда
END_GAME = pygame.USEREVENT + 3

# Короткое название для двумерного вектора
vec2 = pygame.math.Vector2

# Адрес сервера
HOST, PORT = get_host_port()
# Максимальное кол-во подключений
MAX_PLAYERS = 8

# Размеры экрана
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = vec2(600, 360)
# Центра экрана
CENTER = CENTER_WIDTH, CENTER_HEIGHT = WINDOW_SIZE // 2
# Смещение игрока на экране
PLAYER_OFFSET = CENTER_HEIGHT // 2 + 15

# Размер тайла на карте
TILE_SIZE = 219

# Событие: Движениe по диагонали
DIAGONAl_MOVE_EVENT = pygame.USEREVENT + 4

# Событие: Начало игры
WAITING = pygame.USEREVENT + 5

# Цвет фона
BG_COLOR = '#729809'
# Количество углов обзора
NUMBER_ANGLES = 360

CARS_ATTRIBUTES = {
    'ford_f-150': {
        'max_speed': 2.4,
        'reverse_speed': 1.2,
        'gas': 0.001,
        'brake': 0.002,
        'slowdown': 0.0002,
        'camera_rotation_angle': 0.001,
        'step_rotation_angle': 0.003,
    },
    'toyota_land_cruiser': {
        'max_speed': 2.8,
        'reverse_speed': 1.4,
        'gas': 0.0012,
        'brake': 0.002,
        'slowdown': 0.0002,
        'camera_rotation_angle': 0.001,
        'step_rotation_angle': 0.0026,
    },
    'hyundai_creta': {
        'max_speed': 3,
        'reverse_speed': 1.5,
        'gas': 0.0013,
        'brake': 0.002,
        'slowdown': 0.0002,
        'camera_rotation_angle': 0.001,
        'step_rotation_angle': 0.0024,
    },
    'dodge_challenger': {
        'max_speed': 3.2,
        'reverse_speed': 1.8,
        'gas': 0.0014,
        'brake': 0.002,
        'slowdown': 0.0002,
        'camera_rotation_angle': 0.001,
        'step_rotation_angle': 0.0022,
    },
    'nissan_skyline_r34': {
        'max_speed': 3.6,
        'reverse_speed': 1.6,
        'gas': 0.0016,
        'brake': 0.002,
        'slowdown': 0.0002,
        'camera_rotation_angle': 0.001,
        'step_rotation_angle': 0.0018,
    },
    'lamborghini_aventador': {
        'max_speed': 4,
        'reverse_speed': 2,
        'gas': 0.002,
        'brake': 0.004,
        'slowdown': 0.0002,
        'camera_rotation_angle': 0.001,
        'step_rotation_angle': 0.0016,
    },
}

# Словарь словарей объектов
STACKED_SPRITE_ATTRIBUTES = {
    'dodge_challenger': {
        'path': 'data/images/cars/dodge_challenger.png',
        'number_layers': 10,
        'scale': 2,
        'y_offset': 0,
        'outline': False,
        'mask_layer': 5,
        'color': '#ff7501',
    },
    'nissan_skyline_r34': {
        'path': 'data/images/cars/nissan_skyline_r34.png',
        'number_layers': 10,
        'scale': 2,
        'y_offset': 0,
        'outline': False,
        'mask_layer': 5,
        'color': '#acacac',
    },
    'hyundai_creta': {
        'path': 'data/images/cars/hyundai_creta.png',
        'number_layers': 11,
        'scale': 2,
        'y_offset': 0,
        'outline': False,
        'mask_layer': 3,
        'color': '#2f89f1',
    },
    'ford_f-150': {
        'path': 'data/images/cars/ford_f-150.png',
        'number_layers': 11,
        'scale': 2,
        'y_offset': 0,
        'outline': False,
        'mask_layer': 2,
        'color': '#4e74c6',
    },
    'toyota_land_cruiser': {
        'path': 'data/images/cars/toyota_land_cruiser.png',
        'number_layers': 13,
        'scale': 2,
        'y_offset': 0,
        'outline': False,
        'mask_layer': 4,
        'color': '#dbd9f7',
    },
    'lamborghini_aventador': {
        'path': 'data/images/cars/lamborghini_aventador.png',
        'number_layers': 9,
        'scale': 2,
        'y_offset': 0,
        'outline': False,
        'mask_layer': 1,
        'color': '#5521ff',
    },
    'birch': {
        'path': 'data/images/objects/birch.png',
        'number_layers': 40,
        'scale': 8,
        'y_offset': -150,
        'outline': False,
        'mask_layer': 1,
    },
    'oak': {
        'path': 'data/images/objects/oak.png',
        'number_layers': 32,
        'scale': 8,
        'y_offset': -120,
        'outline': False,
        'mask_layer': 1,
    },
}

MAP_ATTRIBUTES = {
    'green_forest': {
        'path': 'data/maps/green_forest',
        'scale': 4,
        'minimap_scale': 0.25,
        'number_of_laps': 3,
        'background': '#639809',
        'number_layers': 8,
        'finish_line': [1, 13.6],
        'objects': ['birch', 'oak'],
        'barrier_mask_layer': -1,
        'barriers': [0, 2, 4, 6, 8, 17, 18, 20, 22, 24, 26, 35, 36, 37, 38, 39, 40, 41],
        'barriers_2x2': [0, 2, 4, 6, 18, 20, 22, 24],
        'player_position': [(0.825, 13.22), (1.175, 12.80),
                            (0.825, 12.22), (1.175, 11.80),
                            (0.825, 11.22), (1.175, 10.80),
                            (0.825, 10.22), (1.175, 9.80),],
    }
}
