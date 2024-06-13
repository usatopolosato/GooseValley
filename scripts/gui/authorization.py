import json
from scripts.base_function import *
from scripts.settings import WINDOW_SIZE
from scripts.gui.inputbox import LineEdit
from scripts.gui.button import ButtonRect

# Задаем размеры окна и инициализируем Pygame.
pygame.init()
size = width, height = WINDOW_SIZE * 2
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Speed Racer')
pygame.display.set_icon(load_image('logo.png'))


# Игрок должен придумать себе никнейм. Данная функция создает форму для этого.
def authorization():
    # Создаем поле ввода для никнейма.
    text = ''
    line_edit = LineEdit(100 / 1200 * width, height // 3, need_font(65), pygame.Color('white'),
                         pygame.Color('grey'), text)
    # Создаем надписи и вычисляем нужные координаты для их размещения.
    label_authorization = need_font(65).render("Придумайте себе имя", True,
                                               pygame.Color('#ffffff'))
    label_x = 100 / 1200 * width + label_authorization.get_width() // 2
    label_y = label_authorization.get_height() // 2 + 50
    label_authorization_rect = label_authorization.get_rect(center=(label_x, label_y))
    # Создаем кнопки на экране.
    text_button = need_font(65).render("Продолжить", True,
                                       pygame.Color('#ffffff'))
    d_y = line_edit.rect.top - label_y
    button_next = ButtonRect(pygame.Color('#3F888F'),
                             (100 / 1200 * width + text_button.get_width() // 2 + 80,
                              line_edit.rect.bottom + d_y),
                             'Продолжить',
                             need_font(65), pygame.Color('#e6e6fa'), pygame.Color('#ffffff'))
    # Основной цикл.
    while True:
        screen.fill(pygame.Color('#09b2c2'))
        # Просмотр всех событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем нажата ли кнопка продолжить и введен ли текст в соответствующее поле
                # ввода. В зависимости от этого сохраняем никнейм в json файл и переходим к
                # следующему окну.
                line_edit.is_active()
                if button_next.click():
                    if len(text) != 0:
                        player = {'name': [text]}
                        with open('data/files/settings.json', 'w') as file:
                            json.dump(player, file, ensure_ascii=True)
                        return True
            if event.type == pygame.KEYDOWN:
                # Проверяем нажат ли ENTER и введен ли текст в соответствующее поле
                # ввода. В зависимости от этого сохраняем никнейм в json файл и переходим к
                # следующему окну.
                key_p = pygame.key.get_pressed()
                if key_p[pygame.K_RETURN]:
                    if len(text) != 0:
                        player = {'name': [text]}
                        with open('data/files/settings.json', 'w') as file:
                            json.dump(player, file, ensure_ascii=True)
                        return True
                if key_p[pygame.K_BACKSPACE]:
                    # Если нажимаем BACKSPACE, то удаляем последний введенный символ.
                    text = text[:-1]
                if not key_p[pygame.K_BACKSPACE] and not key_p[pygame.K_RETURN]:
                    # Обновляем поле ввода, если вводим какой-то текст.
                    if len(text) < 20:
                        if line_edit.active:
                            text += event.unicode
                line_edit.update(text)
        # Обработка действий над кнопками.
        button_next.hover()
        button_next.update(screen)
        # Отрисовка объектов.
        line_edit.draw(screen)
        screen.blit(label_authorization, label_authorization_rect)
        pygame.display.flip()
