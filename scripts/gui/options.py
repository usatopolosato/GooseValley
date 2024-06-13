import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from scripts.settings import *
from scripts.base_function import *
import json


# Класс Модифицированной Кнопки.
class ModButton:
    def __init__(self, position, peace_image, hover_image):
        # Инициализируем кнопку.
        # Сохраняем и устанавливаем нужные изображения для кнопки.
        # Получаем координаты и нужные размеры для отображения на экране.
        self.image = peace_image
        self.images = peace_image, hover_image
        self.current_image = 0
        self.pos_x, self.pos_y = position
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    # Функция для размещения кнопки на экране.
    def update(self, screen):
        screen.blit(self.image, self.rect)

    # Функция, которая возвращает результат проверки нажатия на кнопку.
    def click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_image += 1
            self.image = self.images[self.current_image % 2]
            return True
        return False


# Класс приложения
class Options:
    def __init__(self, size, background):
        # Экран
        self.screen = pygame.display.set_mode(size)
        # Размеры экрана
        self.width, self.height = size
        # Часы
        self.clock = pygame.time.Clock()
        # Задний фон
        self.background = background
        self.fps_counter = False
        # Объект Slider
        self.slider = Slider(self.screen, int(self.width * 0.3), int(self.height * 0.4),
                             int(self.width * 0.6), int(self.height * 0.05),
                             min=0, max=100, step=1)
        self.slider.value = 50
        # Объект TextBox
        self.textbox = TextBox(self.screen, int(self.width * 0.286), int(self.height * 0.2),
                               int(self.width * 0.64), int(self.height * 0.08),
                               onSubmit=self.change_name, font=need_font(40),
                               colour=pygame.Color('#464451'),
                               borderColour=pygame.Color('white'),
                               textColour=pygame.Color('yellow'))
        # Получаем текущее имя игрока.
        with open('data/files/settings.json', 'r', encoding='utf-8') as file:
            name = json.load(file)['name'][0]
        # Устанавливаем текущее имя в поле никнейм.
        self.textbox.setText(name)
        # Надпись НАСТРОЙКИ и ее размещение на экране
        self.label_settings = need_font(50).render("Настройки", True,
                                                   pygame.Color('#ffffff'))
        self.name = self.textbox.getText()
        label_x = self.width // 2
        label_y = self.label_settings.get_height() // 2 + 10
        self.label_settings_rect = self.label_settings.get_rect(center=(label_x, label_y))
        # Надпись ЗВУК и ее размещение на экране
        self.label_sound = need_font(48).render("Звук", True,
                                                pygame.Color('#ffffff'))
        label_x = self.label_sound.get_width() + 50
        label_y = int(self.height * 0.425)
        self.label_sound_rect = self.label_settings.get_rect(center=(label_x, label_y))
        # Надпись Имя и ее размещение на экране
        self.label_name = need_font(48).render("Никнейм:", True,
                                               pygame.Color('#ffffff'))
        label_y = int(self.height * 0.286) - int(self.height * 0.08) // 2
        self.label_name_rect = self.label_settings.get_rect(center=(label_x, label_y))
        # Надпись СЧЕТЧИК ФПС и ее размещение на экране
        self.label_fps = need_font(48).render("Счетчик фпс", True,
                                              pygame.Color('#ffffff'))
        label_x = self.label_sound.get_width() + 50
        label_y = int(self.height * 0.625)
        self.label_fps_rect = self.label_settings.get_rect(center=(label_x, label_y))
        # Кнопка ФПС-CHECK
        button_w, button_h = self.label_fps_rect.w, self.label_fps_rect.h + 15
        EMPTY = pygame.transform.scale(load_image('empty.png'), (button_h, button_h))
        CHECKMARK = pygame.transform.scale(load_image('checkmark.png'), (button_h, button_h))
        self.button_fps_check = ModButton((label_x + button_w, label_y), EMPTY, CHECKMARK)

    # Просмотр всех событий
    def check_events(self):
        events = pygame.event.get()
        for event in events:
            # Если мы вышли из окна настроеек или нажали клавишу enter, то сохраняем имя в
            # json файл.
            if event.type == pygame.QUIT:
                self.change_name()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.change_name()
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_fps_check.click():
                    self.fps_counter = not self.fps_counter
        pygame.mixer.music.set_volume(self.slider.getValue() / 100)
        pygame_widgets.update(events)
        # Ограничение по длине имени 20.
        if len(self.textbox.getText()) > 20:
            self.textbox.setText(self.textbox.getText()[:-1])
        return True

    # Функция для изменения имени в json файле.
    def change_name(self):
        self.name = self.textbox.getText()
        player = {'name': [self.name]}
        with open('data/files/settings.json', 'w') as file:
            json.dump(player, file, ensure_ascii=True)
        return True

    # Рисование объектов
    def draw(self):
        pygame.display.set_caption(f'Speed Racer')
        # Заполняем фоновым цветом
        self.screen.fill(self.background)
        # Размещаем надписи
        self.screen.blit(self.label_settings, self.label_settings_rect)
        self.screen.blit(self.label_sound, self.label_sound_rect)
        self.screen.blit(self.label_fps, self.label_fps_rect)
        self.screen.blit(self.label_name, self.label_name_rect)
        pygame.draw.rect(self.screen, pygame.Color('#A5A5A5'), self.button_fps_check.rect, 5)
        self.button_fps_check.update(self.screen)

    # Основной цикл
    def run(self):
        while self.check_events():
            self.draw()
            self.clock.tick()
            pygame_widgets.update(pygame.event.get())
            pygame.display.flip()

    # Функция нужна, чтобы установить корректный никнейм в поле ввода для редактиовоания имени.
    def start(self):
        with open('data/files/settings.json', 'r', encoding='utf-8') as file:
            name = json.load(file)['name'][0]
        self.textbox.setText(name)


# Создаем объект класса Options
OPTIONS_APP = Options(WINDOW_SIZE * 2, pygame.Color('#464451'))
