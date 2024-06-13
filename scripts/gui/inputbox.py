import pygame


class LineEdit:
    def __init__(self, x, y, font, color_active, color_inactive, text):
        # Создаем наше поле ввода, сохраняем цвета, шрифт, размеры.
        self.rect = pygame.Rect(x, y, 1, 1)
        self.text = text
        self.font = font
        # Нужно для вычисления границ размеров поля ввода.
        self.ed_width = font.render('W', True, 'white').get_width()
        self.ed_height = font.render('W', True, 'white').get_height()
        self.max_width, self.min_width = self.ed_width * 20, 700
        self.colors_activity = [color_inactive, color_active]
        self.active = False
        self.update('')

    # Активируем поле ввода, если на него нажали(или наооборот).
    def is_active(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.active = not self.active
            self.text_surface = self.font.render(self.text, True,
                                                 self.colors_activity[int(self.active)])

    # Изменяем размеры поля ввода, в зависимости от длины текста.
    def update(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True,
                                             self.colors_activity[int(self.active)])
        self.rect.w = min(max(self.min_width, self.text_surface.get_width()), self.max_width) + 30
        self.rect.h = self.ed_height + 30

    # Отрисовываем наше поле ввода.
    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.x + 15, self.rect.y + 15))
        pygame.draw.rect(screen, self.colors_activity[int(self.active)], self.rect, 8)
