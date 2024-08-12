from pygame_texteditor import TextEditor
import pygame
import os
import sys


# Функция для загрузки шрифтов.
def load_font(name):
    fullname = os.path.join('..', 'data', 'fonts', name)
    if not os.path.isfile(fullname):
        print(f'Файл {fullname} не найден')
        sys.exit()
    return fullname


# Функция для возврата нужного размера шрифта.
def need_font(size):
    return pygame.font.Font(load_font('Minecraft Rus NEW.otf'), size)


# Короткое название для двумерного вектора
vec2 = pygame.math.Vector2

# Размеры экрана
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = vec2(600, 360)

# Задаем размеры окна и инициализируем Pygame.
pygame.init()
size = width, height = WINDOW_SIZE * 2
screen = pygame.display.set_mode(size)
pygame.display.set_caption('GooseValley')
text = need_font(15).render('GaGaBook', True, pygame.Color("#FFFAFA"))
label_x = 195 / 390 * width + text.get_width() // 2
label_y = text.get_height() // 2 + 175 / 260 * height
label_text_rect = pygame.Rect(195 / 390 * width - text.get_width() // 2,
                              -text.get_height() // 2 + 175 / 260 * height,
                              text.get_width(), text.get_height())
pygame.display.get_surface().fill(pygame.Color('#BDECB6'))
TX = TextEditor(
    offset_x=int(45 / 390 * width), offset_y=int(25 / 260 * height),
    editor_width=int(305 / 390 * width),
    editor_height=int(145 / 260 * height), screen=screen)
TX.set_syntax_highlighting(True)
TX.set_font_size(23)
COLOR_BUTTON = pygame.Color('#3b3b3b')
COLOR_MOUSE = pygame.Color('#636363')

while True:
    pygame.display.set_caption('GooseValley')
    pygame.draw.rect(screen, pygame.Color('#765432'), (0, int(150 / 260 * height), width,
                                                       int(110 / 260 * height)))
    pygame.draw.polygon(screen, (176, 168, 168),
                        ((int(50 / 390 * width), int(10 / 260 * height)),
                         (int(350 / 390 * width), int(10 / 260 * height)),
                         (int(355 / 390 * width), int(15 / 260 * height)),
                         (int(355 / 390 * width), int(180 / 260 * height)),
                         (int(385 / 390 * width), int(240 / 260 * height)),
                         (int(375 / 390 * width), int(250 / 260 * height)),
                         (int(25 / 390 * width), int(250 / 260 * height)),
                         (int(15 / 390 * width), int(240 / 260 * height)),
                         (int(45 / 390 * width), int(180 / 260 * height)),
                         (int(45 / 390 * width), int(15 / 260 * height))))
    pygame.draw.polygon(screen, pygame.Color('#3b3b3b'),
                        ((int(50 / 390 * width), int(10 / 260 * height)),
                         (int(350 / 390 * width), int(10 / 260 * height)),
                         (int(355 / 390 * width), int(15 / 260 * height)),
                         (int(355 / 390 * width), int(180 / 260 * height)),
                         (int(45 / 390 * width), int(180 / 260 * height)),
                         (int(45 / 390 * width), int(15 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(60 / 390 * width), int(195 / 260 * height)),
                         (int(90 / 390 * width), int(195 / 260 * height)),
                         (int(85 / 390 * width), int(205 / 260 * height)),
                         (int(55 / 390 * width), int(205 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(100 / 390 * width), int(195 / 260 * height)),
                         (int(125 / 390 * width), int(195 / 260 * height)),
                         (int(120 / 390 * width), int(205 / 260 * height)),
                         (int(95 / 390 * width), int(205 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(135 / 390 * width), int(195 / 260 * height)),
                         (int(165 / 390 * width), int(195 / 260 * height)),
                         (int(165 / 390 * width), int(205 / 260 * height)),
                         (int(130 / 390 * width), int(205 / 260 * height))))
    for i in range(2):
        pygame.draw.rect(screen, COLOR_BUTTON, (int((175 + 30 * i) / 390 * width),
                                                int(195 / 260 * height),
                                                int(20 / 390 * width), int(10 / 260 * height)))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(235 / 390 * width), int(195 / 260 * height)),
                         (int(265 / 390 * width), int(195 / 260 * height)),
                         (int(270 / 390 * width), int(205 / 260 * height)),
                         (int(235 / 390 * width), int(205 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(275 / 390 * width), int(195 / 260 * height)),
                         (int(300 / 390 * width), int(195 / 260 * height)),
                         (int(305 / 390 * width), int(205 / 260 * height)),
                         (int(280 / 390 * width), int(205 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(310 / 390 * width), int(195 / 260 * height)),
                         (int(340 / 390 * width), int(195 / 260 * height)),
                         (int(345 / 390 * width), int(205 / 260 * height)),
                         (int(315 / 390 * width), int(205 / 260 * height))))
    pygame.draw.rect(screen, (187, 187, 187), (int(190 / 390 * width),
                                                int(13 / 260 * height),
                                                int(10 / 390 * width), int(10 / 260 * height)))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(50 / 390 * width), int(210 / 260 * height)),
                         (int(80 / 390 * width), int(210 / 260 * height)),
                         (int(75 / 390 * width), int(220 / 260 * height)),
                         (int(45 / 390 * width), int(220 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(90 / 390 * width), int(210 / 260 * height)),
                         (int(115 / 390 * width), int(210 / 260 * height)),
                         (int(110 / 390 * width), int(220 / 260 * height)),
                         (int(85 / 390 * width), int(220 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(125 / 390 * width), int(210 / 260 * height)),
                         (int(145 / 390 * width), int(210 / 260 * height)),
                         (int(145 / 390 * width), int(220 / 260 * height)),
                         (int(125 / 390 * width), int(220 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(155 / 390 * width), int(210 / 260 * height)),
                         (int(255 / 390 * width), int(210 / 260 * height)),
                         (int(260 / 390 * width), int(220 / 260 * height)),
                         (int(150 / 390 * width), int(220 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(265 / 390 * width), int(210 / 260 * height)),
                         (int(285 / 390 * width), int(210 / 260 * height)),
                         (int(285 / 390 * width), int(220 / 260 * height)),
                         (int(265 / 390 * width), int(220 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(295 / 390 * width), int(210 / 260 * height)),
                         (int(315 / 390 * width), int(210 / 260 * height)),
                         (int(320 / 390 * width), int(220 / 260 * height)),
                         (int(300 / 390 * width), int(220 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_BUTTON,
                        ((int(325 / 390 * width), int(210 / 260 * height)),
                         (int(355 / 390 * width), int(210 / 260 * height)),
                         (int(360 / 390 * width), int(220 / 260 * height)),
                         (int(330 / 390 * width), int(220 / 260 * height))))
    pygame.draw.polygon(screen, COLOR_MOUSE,
                        ((int(170 / 390 * width), int(225 / 260 * height)),
                         (int(230 / 390 * width), int(225 / 260 * height)),
                         (int(245 / 390 * width), int(240 / 260 * height)),
                         (int(155 / 390 * width), int(240 / 260 * height))))
    for i in range(3):
        pygame.draw.polygon(screen, COLOR_BUTTON,
                            ((int((70 + 30 * i) / 390 * width), int(185 / 260 * height)),
                             (int((90 + 30 * i) / 390 * width), int(185 / 260 * height)),
                             (int((85 + 30 * i) / 390 * width), int(190 / 260 * height)),
                             (int((65 + 30 * i) / 390 * width), int(190 / 260 * height))))
        pygame.draw.polygon(screen, COLOR_BUTTON,
                            ((int((250 + 30 * i) / 390 * width), int(185 / 260 * height)),
                             (int((270 + 30 * i) / 390 * width), int(185 / 260 * height)),
                             (int((275 + 30 * i) / 390 * width), int(190 / 260 * height)),
                             (int((255 + 30 * i) / 390 * width), int(190 / 260 * height))))
        pygame.draw.rect(screen, COLOR_BUTTON, (int((160 + 30 * i) / 390 * width),
                                                int(185 / 260 * height),
                                                int(20 / 390 * width),
                                                int(5 / 260 * height)))

    pygame_events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    TX.display_editor(pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed)
    screen.blit(text, label_text_rect)
    pygame.display.flip()
