import pygame
import sys
import os
from scripts.settings import *
from scripts.base_function import *


# Инициализируем pygame и создаём экран.
pygame.init()
size = width, height = WINDOW_SIZE * 2
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Speed Racer')
pygame.display.set_icon(load_image('logo.png'))
FPS = 18
start_fon = pygame.sprite.Group()


# Класс для отображения изображения по кадрам.
class GifInPygame(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(start_fon)
        # Разобьём изображение на фреймы.
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        # Устанавливаем текущий кадр в качестве изображения.
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    # Функция для нарезания изображения на фреймы.
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    # Меняем текущий кадр.
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


# Функция для завершения работы приложения.
def terminate():
    pygame.quit()
    sys.exit()


# Функция для отображения текста по текущим координатам на экране.
def draw_text(text, coord_y, size_font):
    # Получаем нужный шрифт нужного размера.
    font = pygame.font.Font(load_font('Gameplay.ttf'), size_font)
    # Рендерим наш текст.
    draw_line = font.render(text, True, pygame.Color('#bc13fe'))
    # Размещаем наш текст по указанным координатам.
    line_rect = draw_line.get_rect()
    line_rect.top = coord_y * height
    line_rect.x = width // 2 - draw_line.get_width() // 2
    screen.blit(draw_line, line_rect)


# Функция старта загрузочного экрана.
def start_screen():
    clock = pygame.time.Clock()
    name = 'Speed Racer'
    label = 'Чтобы начать, нажмите любую кнопку.'
    # Координаты размещения на экране указанного выше текста.
    coord_y_name = 100 / 600
    coord_y_label = 550 / 600
    # Устанавливаем Гиф-изображение на задний фон.
    GifInPygame(pygame.transform.scale(load_image('wallpaper.png'), (width * 7, height * 1.4)),
                7, 1, 0, -height*0.3)
    # Основной цикл.
    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # Возвращаем True,
            # если выполнены необходимые условия для запуска
            # следующего окна.
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return True
        # Отрисовываем задний фон.
        start_fon.update()
        start_fon.draw(screen)
        # Отрисовываем нужный текст.
        draw_text(name, coord_y_name, 90)
        draw_text(label, coord_y_label, 34)
        pygame.display.flip()
        clock.tick(FPS)
