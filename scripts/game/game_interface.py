from scripts.base_function import *
from scripts.settings import *
from math import ceil


# Класс, содержащий весь внутриигровой интерфейс
class GameInterface:
    def __init__(self, app):
        # Приложение
        self.app = app
        # Количество кругов
        self.laps = {'pos': vec2(10, 10), 'font': need_font(50), 'offset': vec2(3)}
        # Время с начала гонки
        self.time = {'pos': vec2(10, 70), 'font': need_font(30), 'offset': vec2(2)}
        self.race_time = 0
        # Количество кадров в секунду
        self.fps = {'pos': vec2(945, 10), 'font': need_font(40), 'offset': vec2(2.5)}
        # Скорость
        self.speed = {'pos': vec2(920, 665), 'font': need_font(50), 'offset': vec2(3)}
        # Сообщение по центру
        self.message = {'pos': vec2(600, 380), 'font': need_font(180), 'offset': vec2(10)}

    # Размещение элемента
    def blit(self, font, text, pos, offset, centre=False):
        text_render = font.render(text, True, pygame.Color(0, 0, 0))
        pos = vec2(pos) -vec2(text_render.get_size()) // 2 if centre else vec2(pos)
        self.app.screen.blit(text_render, pos + offset)
        text_render = font.render(text, True, pygame.Color(255, 255, 255))
        self.app.screen.blit(text_render, pos)

    # Отрисовка всех элиментов
    def draw(self):
        # Количество кругов
        laps = min(self.app.number_of_laps, self.app.max_number_of_laps)
        self.blit(self.laps['font'], f'Круг {laps}/{self.app.max_number_of_laps}',
                  self.laps['pos'], self.laps['offset'])

        # Время с начала гонки
        if self.app.state == 'running':
            self.race_time = int(self.app.time * 100)
        if self.app.state != 'beginning':
            m, s, ms = self.race_time // 6000, self.race_time % 6000 // 100, self.race_time % 100
            self.blit(self.time['font'], f'{m // 10}{m % 10}:{s // 10}{s % 10}:{ms // 10}{ms % 10}',
                      self.time['pos'], self.time['offset'])

        # Скорость
        s, d, e = self.app.speed // 100, self.app.speed % 100 // 10, self.app.speed % 10
        self.blit(self.speed['font'], f'{s}{d}{e} км/ч',
                  self.speed['pos'], self.speed['offset'])

        # Количество кадров в секунду
        if self.app.fps_counter:
            self.blit(self.fps['font'], f'{self.app.clock.get_fps(): .1f} FPS',
                      self.fps['pos'], self.fps['offset'])

        # Сообщение по центру
        message = ''
        if self.app.state == 'beginning':
            message = f'{max(1, ceil(10 - self.app.time))}'
        elif self.app.time < 1:
            message = 'ПОЕХАЛИ'
        elif self.app.state == 'ending':
            place = {1: '1-ый', 2: '2-ой', 3: '3-ий', 4: '4-ый',
                     5: '5-ый', 6: '6-ой', 7: '7-ой', 8: '8-ой'}[self.app.client.place]
            message = f'{place}'
        self.blit(self.message['font'], message,
                  self.message['pos'], self.message['offset'], True)
