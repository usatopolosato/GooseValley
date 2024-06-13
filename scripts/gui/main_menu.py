import json

import pygame

from scripts.gui.button import ButtonEllipse, Arrow
from scripts.game.application import App
from scripts.gui.platform_car import Platform
from scripts.gui.options import OPTIONS_APP
from scripts.gui.background import BackgroundMain, BackgroundLobby
from scripts.settings import *
from scripts.base_function import *
from scripts.multiplayer.client import Client
from math import ceil


# Инициализируем pygame и создаём экран.
pygame.init()
clock = pygame.time.Clock()
size = width, height = WINDOW_SIZE * 2
screen = pygame.display.set_mode(size)
pygame.display.set_icon(load_image('logo.png'))

# Переменная, отвечающая за то, показывать ли фпс или нет.
FPS_COUNTER = False

# Уровень звука
SOUND = 100

pygame.time.set_timer(DIAGONAl_MOVE_EVENT, 50)


# Функция для запуска игры.
def play(client, cache, name_car):
    global FPS_COUNTER, SOUND
    # Создаем объект класса Арр и запускаем игровой цикл.
    app = App(client, cache, name_car, FPS_COUNTER, SOUND)
    while not app.run():
        ...
    del app
    # После завершения игры возвращаемся в главное меню.
    main_menu(cache, name_car)


# Функция для запуска окна настроеек.
def options(cache, name_car):
    global SOUND, FPS_COUNTER
    # Запускаем основной цикл.
    OPTIONS_APP.start()
    while OPTIONS_APP.run():
        ...
    # После закрытия окна настроек возвращаемся в главное меню.
    SOUND = OPTIONS_APP.slider.getValue()
    FPS_COUNTER = OPTIONS_APP.fps_counter
    main_menu(cache, name_car)


# Лобби
def lobby(client, cache, name_car):
    global SOUND, FPS_COUNTER
    # Устанавливаем таймер до начала игры.
    start_time = pygame.time.get_ticks() * 0.001
    # Задний фон.
    BACKGROUND = BackgroundLobby(90, [pygame.Color('#262B44'), pygame.Color('#181425')])
    # Получаем список машин и узнаем индекс текущей машинки.
    NAME_CARS = list(CARS_ATTRIBUTES.keys())
    CURRENT_CAR = NAME_CARS.index(name_car)
    # Загружаем нужные картинки для кнопок.
    LEFT = pygame.transform.scale(load_image('left.png'), (int(175 / 800 * WINDOW_WIDTH),
                                                           int(175 / 600 * WINDOW_HEIGHT)))
    RIGHT = pygame.transform.scale(load_image('right.png'), (int(175 / 800 * WINDOW_WIDTH),
                                                             int(175 / 600 * WINDOW_HEIGHT)))
    LEFT_HOVER = pygame.transform.scale(load_image('left_hover.png'),
                                        (int(175 / 800 * WINDOW_WIDTH),
                                         int(175 / 600 * WINDOW_HEIGHT)))
    RIGHT_HOVER = pygame.transform.scale(load_image('right_hover.png'),
                                         (int(175 / 800 * WINDOW_WIDTH),
                                          int(175 / 600 * WINDOW_HEIGHT)))
    # Создаем платформу для отображения выбранной машинки.
    DEMONSTRATION_SURFACE = pygame.Surface((300, 300))
    coor_x = width - 1.5 * LEFT.get_width() - DEMONSTRATION_SURFACE.get_width() // 2
    coor_y = height // 2
    d_height = DEMONSTRATION_SURFACE.get_height()
    d_width = DEMONSTRATION_SURFACE.get_width()
    DEMONSTRATION_RECT = DEMONSTRATION_SURFACE.get_rect(center=(coor_x, coor_y))
    demo_app = Platform(DEMONSTRATION_SURFACE, cache, NAME_CARS[CURRENT_CAR])
    # Создаем надписи.
    CAR_LABEl = need_font(40).render("Ваш автомобиль", True,
                                     pygame.Color('#ffffff'))
    CAR_RECT = CAR_LABEl.get_rect(center=(coor_x,
                                          coor_y - d_height // 2 - CAR_LABEl.get_height() // 2))
    LEFT_BUTTON = Arrow((width - 2 * LEFT.get_width() - d_width, height // 2),
                        LEFT, LEFT_HOVER)
    RIGHT_BUTTON = Arrow((width - LEFT.get_width(), height // 2),
                         RIGHT, RIGHT_HOVER)
    # Объединяем кнопки в соответствующие группы для дальнейшей работы над ними.
    arrows = [LEFT_BUTTON, RIGHT_BUTTON]
    with open('data/files/settings.json', 'r', encoding='utf-8') as file:
        name = json.load(file)['name'][0]
    client.update_name(name)
    # Вот сюда список игроков!!!
    players = list(map(lambda el: el['name'], client.players))
    time = client.options['time']
    message = ''
    if client.options['state'] == 'waiting' and time < 10 ** 9:
        message = f'начало через {time} секунд'
    # Для вычисления нужных размеров полей никнеймов игроков.
    EX_LABEL = need_font(33).render('W' * 20, True, pygame.Color('white'))
    while True:
        pygame.display.set_caption(f'Speed Racer')
        # Размещаем объекты на экране.
        screen.blit(BACKGROUND.image, (-90, -360))
        screen.blit(DEMONSTRATION_SURFACE, DEMONSTRATION_RECT)
        screen.blit(CAR_LABEl, CAR_RECT)
        step_y = 40
        # Выводим список игроков.
        for el in players:
            LABEL_NAME = need_font(30).render(el, True, pygame.Color('white'))
            BG_LABEL = pygame.Surface((EX_LABEL.get_width(), EX_LABEL.get_height() + 20))
            BG_LABEL.fill('black')
            pygame.draw.rect(BG_LABEL, 'white', (0, 0, BG_LABEL.get_width(),
                                                 BG_LABEL.get_height()), 5)
            screen.blit(BG_LABEL, (60, step_y - 10))
            screen.blit(LABEL_NAME, (80, step_y))
            step_y += LABEL_NAME.get_height() + 40
        # Выводим сообщение сколько осталось до начала игры.
        message = ''
        if client.options['state'] == 'waiting' and time < 10 ** 9:
            message = f'начало через {time} секунд'
        MESSAGE = need_font(26).render(message, True, pygame.Color('#ffffff'))
        MESSAGE_RECT = MESSAGE.get_rect(center=(50 + MESSAGE.get_width() // 2, 650))
        screen.blit(MESSAGE, MESSAGE_RECT)
        # Запускаем цикл платформы для вращения демоверсии машинки.
        demo_app.run()
        # Обработка действий над кнопками.
        for button in arrows:
            button.hover()
            button.update(screen)
        # Просмотр событий.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu(cache, NAME_CARS[CURRENT_CAR])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    client.exit_the_game()
                    main_menu(cache, NAME_CARS[CURRENT_CAR])
            # Движение заднего фона по диагонали.
            if event.type == DIAGONAl_MOVE_EVENT:
                BACKGROUND.update()
            if event.type == CLIENT_UPDATE:
                client.get_id()
                client.get_options()
                client.get_players()
                players = list(map(lambda el: el['name'], client.players))
            # Меняем текущую машинку в зависимости от нажатой клавиши или
            # кнопки на экране.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in [1, 3]:
                if LEFT_BUTTON.click():
                    CURRENT_CAR = (CURRENT_CAR - 1) % len(NAME_CARS)
                    demo_app = Platform(DEMONSTRATION_SURFACE, cache, NAME_CARS[CURRENT_CAR])
                if RIGHT_BUTTON.click():
                    CURRENT_CAR = (CURRENT_CAR + 1) % len(NAME_CARS)
                    demo_app = Platform(DEMONSTRATION_SURFACE, cache, NAME_CARS[CURRENT_CAR])
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    CURRENT_CAR = (CURRENT_CAR - 1) % len(NAME_CARS)
                    demo_app = Platform(DEMONSTRATION_SURFACE, cache, NAME_CARS[CURRENT_CAR])
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    CURRENT_CAR = (CURRENT_CAR + 1) % len(NAME_CARS)
                    demo_app = Platform(DEMONSTRATION_SURFACE, cache, NAME_CARS[CURRENT_CAR])
            if client.options['state'] == 'running':
                # Запускаем игру.
                play(client, cache, NAME_CARS[CURRENT_CAR])
                return
        time = client.options['time']
        clock.tick()
        pygame.display.flip()


# Главное меню.
def main_menu(cache, name_car):
    global SOUND, FPS_COUNTER
    BACKGROUND = BackgroundMain(72, pygame.Color('#09b2c2'))
    # Получаем список машин и узнаем индекс текущей машинки.
    NAME_CARS = list(CARS_ATTRIBUTES.keys())
    CURRENT_CAR = NAME_CARS.index(name_car)
    MENU_LABEL = need_font(85).render("Speed Racer", True, pygame.Color('#ffffff'))
    MENU_BORDER = pygame.Surface((MENU_LABEL.get_width() + 20, MENU_LABEL.get_height() + 20))
    MENU_BORDER.fill(pygame.Color('#00416a'))
    pygame.draw.rect(MENU_BORDER, pygame.Color('grey'),
                     (0, 0, MENU_BORDER.get_width(), MENU_BORDER.get_height()),
                     4)
    # Создаем надписи и кнопки нужных размеров.
    MENU_RECT = MENU_BORDER.get_rect(center=(WINDOW_WIDTH, WINDOW_WIDTH * 0.2))
    PLAY_BUTTON = ButtonEllipse(pygame.Color('grey'),
                                (WINDOW_WIDTH, MENU_RECT.bottom + 100),
                                'Играть',
                                need_font(55),
                                pygame.Color('#09b2c2'),
                                pygame.Color('#00416a'))
    OPTIONS_BUTTON = ButtonEllipse(pygame.Color('grey'),
                                   (WINDOW_WIDTH,
                                    PLAY_BUTTON.rect.bottom + 75),
                                   'Настройки',
                                   need_font(55),
                                   pygame.Color('#09b2c2'),
                                   pygame.Color('#00416a'))
    QUIT_BUTTON = ButtonEllipse(pygame.Color('grey'),
                                (WINDOW_WIDTH,
                                 OPTIONS_BUTTON.rect.bottom + 75),
                                'Выход',
                                need_font(55),
                                pygame.Color('#09b2c2'),
                                pygame.Color('#00416a'))
    buttons = [PLAY_BUTTON, QUIT_BUTTON, OPTIONS_BUTTON]
    while True:
        # Показываем ФПС или нет.
        pygame.display.set_caption(f'Speed Racer')
        # Размещаем объекты на экране.
        screen.blit(BACKGROUND.image, (-90, -360))
        screen.blit(MENU_BORDER, MENU_RECT)
        screen.blit(MENU_LABEL, (MENU_RECT.x + 10, MENU_RECT.y + 10))
        # Обработка действий над кнопками.
        for button in buttons:
            button.hover()
            button.update(screen)
        # Просмотр событий.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in [1, 3]:
                # Обработка нажатых клавиш
                # для открытия соответствующих окон
                # или же
                # совершения определенных действий.
                if PLAY_BUTTON.click():
                    client = Client(None, (HOST, PORT))
                    # Запускаем лобби.
                    pygame.time.set_timer(CLIENT_UPDATE, 100)
                    lobby(client, cache, name_car)
                    pygame.time.set_timer(CLIENT_UPDATE, 0)
                    return
                if OPTIONS_BUTTON.click():
                    # Запускаем окно настроек.
                    options(cache, name_car)
                    return
                if QUIT_BUTTON.click():
                    # Завершение работы приложения.
                    pygame.quit()
                    sys.exit()
            if event.type == DIAGONAl_MOVE_EVENT:
                BACKGROUND.update()
        clock.tick()
        pygame.display.flip()
