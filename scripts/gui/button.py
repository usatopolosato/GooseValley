import pygame


# Класс Кнопки-Эллипс.
class ButtonEllipse:
    def __init__(self, background, position, text, font, peace_color, hover_color):
        # Инициализируем кнопку.
        # Сохраняем текст кнопки и его шрифт.
        # Сохраняем и устанавливаем нужный задний фон для кнопки.
        # Получаем координаты и нужные размеры для отображения на экране.
        self.pos_x, self.pos_y = position
        self.font = font
        self.label = text
        self.text = self.font.render(text, True, peace_color)
        self.colors = peace_color, hover_color
        # Нужно для общего стандарта размера кнопки.
        self.standart = self.font.render('YFCNHJQRВВDB', True, peace_color)
        self.standart_rect = self.standart.get_rect()
        self.text_rect = self.text.get_rect(center=(self.pos_x, self.pos_y))
        if background is None:
            self.background = self.text
        else:
            # Делаем задний фон эллипсом.
            self.background = pygame.Surface((self.standart_rect.w + 60,
                                              self.standart_rect.h + 40))
            self.background.fill('#f75394')
            self.background.set_colorkey('#f75394')
            pygame.draw.ellipse(self.background, background, (0, 0, self.standart_rect.w + 60,
                                                              self.standart_rect.h + 40))
            pygame.draw.ellipse(self.background, 'black', (0, 0, self.standart_rect.w + 60,
                                                           self.standart_rect.h + 40), 4)
        self.rect = self.background.get_rect(center=(self.pos_x, self.pos_y))

    # Функция для размещения кнопки на экране.
    def update(self, screen):
        if self.background is not None:
            screen.blit(self.background, self.rect)
        screen.blit(self.text, self.text_rect)

    # Функция проверяет навели ли на кнопку мышкой или же нет.
    # В соответствии с этим меняем внешний вид кнопки.
    def hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.text = self.font.render(self.label, True, self.colors[1])
        else:
            self.text = self.font.render(self.label, True, self.colors[0])

    # Функция, которая возвращает результат проверки нажатия на кнопку.
    def click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False


# Класс Кнопки-Rect.
class ButtonRect(ButtonEllipse):
    def __init__(self, background, position, text, font, peace_color, hover_color):
        super().__init__(background, position, text, font, peace_color, hover_color)
        # Инициализируем кнопку.
        # Сохраняем текст кнопки и его шрифт.
        # Сохраняем и устанавливаем нужный задний фон для кнопки.
        # Получаем координаты и нужные размеры для отображения на экране.
        self.pos_x, self.pos_y = position
        self.font = font
        self.label = text
        self.text = self.font.render(text, True, peace_color)
        self.colors = peace_color, hover_color
        # Нужно для обшего размера кнопок.
        self.standart = self.font.render('YFCNHJQRВВDB', True, peace_color)
        self.standart_rect = self.standart.get_rect()
        self.text_rect = self.text.get_rect(center=(self.pos_x, self.pos_y))
        if background is None:
            self.background = self.text
        else:
            self.background = pygame.Surface((self.standart_rect.w + 60,
                                              self.standart_rect.h + 40))
            self.background.fill('#f75394')
            self.background.set_colorkey('#f75394')
            pygame.draw.rect(self.background, background, (0, 0, self.standart_rect.w + 60,
                                                           self.standart_rect.h + 40))
        self.rect = self.background.get_rect(center=(self.pos_x, self.pos_y))


# Класс Кнопки-Стрелочки(в дальнейшем может использоваться как кнопка с меняющимся оформлением).
class Arrow:
    def __init__(self, position, peace_image, hover_image):
        # Инициализируем кнопку.
        # Сохраняем и устанавливаем нужные изображения для кнопки.
        # Получаем координаты и нужные размеры для отображения на экране.
        self.image = peace_image
        self.images = peace_image, hover_image
        self.pos_x, self.pos_y = position
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    # Функция для размещения кнопки на экране.
    def update(self, screen):
        screen.blit(self.image, self.rect)

    # Функция проверяет навели ли на кнопку мышкой.
    # В соответствии с этим меняем внешний вид кнопки.
    def hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    # Функция, которая возвращает результат проверки нажатия на кнопку.
    def click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False
