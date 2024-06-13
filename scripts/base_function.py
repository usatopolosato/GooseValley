import pygame
import os
import sys
import socket
import csv

# Инициализируем pygame
pygame.init()
# Загружаем фоновую музыку
pygame.mixer.music.load('data/music/background_music.mp3')
# Запускаем фоновую музыку
pygame.mixer.music.play(loops=-1, start=30)
pygame.mixer.music.set_volume(0.5)


# Функция для загрузки изображений.
def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'images', 'gui', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_it((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


# Функция для загрузки шрифтов.
def load_font(name):
    fullname = os.path.join('data', 'fonts', name)
    if not os.path.isfile(fullname):
        print(f'Файл {fullname} не найден')
        sys.exit()
    return fullname


# Функция для получения локального ip
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


# Функция для возврата нужного размера шрифта.
def need_font(size):
    return pygame.font.Font(load_font('Minecraft Rus NEW.otf'), size)
