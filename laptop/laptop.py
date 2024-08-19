from pygame_texteditor import TextEditor
from data import db_session
from data.users import User
from data.questions import Question
from data.blocks import Block
import pygame
import os
import sys


class Button:
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None,
                 onePress=False, normal='#ffffff', hover='#666666', pressed='#333333',
                 color=(20, 20, 20)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': normal,
            'hover': hover,
            'pressed': pressed,
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.name = buttonText
        self.buttonSurf = need_font(15).render(buttonText, True, color)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction(self.name)
                elif not self.alreadyPressed:
                    self.onclickFunction(self.name)
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2])
        screen.blit(self.buttonSurface, self.buttonRect)


class Label:
    def __init__(self, x, y, text, *groups, **args):
        super().__init__()
        self.color = (0, 0, 0)
        if 'color' in args:
            self.color = args['color']
        self.size = 16
        if 'size' in args:
            self.size = args['size']
        self.fat = 1
        if 'fat' in args:
            self.fat = args['fat']
        self.inter_y = 5
        if 'inter' in args:
            self.inter_y = args['inter']
        self.set_text(text)
        self.x = x
        self.y = y

    def draw(self, screen):
        font = need_font(self.size)
        for i, t in enumerate(self.text.split('\n')):
            text = font.render(t, self.fat, self.color)
            screen.blit(text,
                        (self.x + 5,
                         self.y + (font.get_height() + self.inter_y) * i + font.get_height()))

    def set_text(self, text):
        r_text = ''
        for i, el in enumerate(text):
            if i % 94 == 0 and i != 0 and el != '\n':
                r_text += '\n'
            r_text += el
        self.text = r_text

    def set_size(self, size):
        self.size = size

    def set_color(self, color):
        self.color = color

    def set_fat(self, fat):
        self.fat = fat

    def move(self, x, y):
        self.x = x
        self.y = y


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
size = width, height = WINDOW_SIZE * 2.5
screen = pygame.display.set_mode(size)
pygame.display.set_caption('GooseValley')
text = need_font(15).render('GaGaBook', True, pygame.Color("#FFFAFA"))
label_text_rect = pygame.Rect(195 / 390 * width - text.get_width() // 2,
                              -text.get_height() // 2 + 175 / 260 * height,
                              text.get_width(), text.get_height())


def laptop(nickname):
    def press_button(name):
        nonlocal screen_1, screen_2
        if name == 'ОТПРАВИТЬ':
            print(TX.get_text_as_string().rstrip())
        elif name == 'ПРИСТУПИТЬ К ВЫПОЛНЕНИЮ':
            screen_1 = False
            screen_2 = True
        elif name == 'ЗАКРЫТЬ':
            screen_1 = True
            screen_2 = False

    screen_1, screen_2 = True, False
    pygame.display.get_surface().fill(pygame.Color('#BDECB6'))
    TX = TextEditor(
        offset_x=int(45 / 390 * width), offset_y=int(95 / 260 * height),
        editor_width=int(305 / 390 * width),
        editor_height=int(75 / 260 * height), screen=screen)
    TX.set_syntax_highlighting(True)
    TX.set_font_size(23)
    COLOR_BUTTON = pygame.Color('#3b3b3b')
    COLOR_MOUSE = pygame.Color('#636363')
    label2 = Label(int(53 / 390 * width), int(25 / 260 * height),
                   'УСЛОВИЕ ЗАДАЧИ')
    labels1 = [Label(int(63 / 390 * width), int(25 / 260 * height),
                     f'Пользователь:   {nickname}.', size=20),
               Label(int(63 / 390 * width), int(40 / 260 * height),
                     'Линейные программы. Ввод и вывод данных\nУсловный оператор\nЦиклы\nМассивы\nФункции и Рекурсия',
                     size=25, inter=15, color=pygame.Color('#7986CB'))]
    buttons2 = [Button(int(290 / 390 * width), int(85 / 260 * height), int(25 / 390 * width),
                       int(10 / 260 * height), 'ЗАКРЫТЬ', press_button,
                       normal=pygame.Color('#7986CB')),
                Button(int(320 / 390 * width), int(85 / 260 * height), int(28 / 390 * width),
                       int(10 / 260 * height), 'ОТПРАВИТЬ', press_button,
                       color=(255, 255, 255),
                       normal=pygame.Color('#1565C0'),
                       hover=pygame.Color('#0D47A1'))
                ]
    buttons1 = [Button(int(270 / 390 * width), int(155 / 260 * height), int(70 / 390 * width),
                       int(10 / 260 * height), 'ПРИСТУПИТЬ К ВЫПОЛНЕНИЮ', press_button,
                       color=(255, 255, 255),
                       normal=pygame.Color('#1565C0'),
                       hover=pygame.Color('#0D47A1'))
                ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
        if screen_2:
            pygame_events = pygame.event.get()
            pressed_keys = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            TX.display_editor(pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed)
            screen.blit(text, label_text_rect)
            pygame.draw.rect(screen, pygame.Color('#FFFFFF'),
                             (int(53 / 390 * width), int(25 / 260 * height), int(297 / 390 * width),
                              int(70 / 260 * height)))
            label2.draw(screen)
            for button in buttons2:
                button.process()
        elif screen_1:
            pygame.draw.rect(screen, pygame.Color('#FFFFFF'),
                             (int(53 / 390 * width), int(25 / 260 * height), int(297 / 390 * width),
                              int(145 / 260 * height)))
            pygame.draw.line(screen, pygame.Color('#DCDCDC'), (int(53 / 390 * width),
                                                               int(40 / 260 * height)),
                             (int(349 / 390 * width), int(40 / 260 * height)), 5)
            for label in labels1:
                label.draw(screen)
            for button in buttons1:
                button.process()
        pygame.display.flip()


def main():
    db_session.global_init('db/datebase.db')
    laptop('usatopolosato')


main()
