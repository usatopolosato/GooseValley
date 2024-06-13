import pygame.sprite
from scripts.settings import *
from scripts.game.stacked_sprite import StackedSprite
from copy import deepcopy
import math


# Класс игрока
class Player(StackedSprite):
    def __init__(self, app, name):
        super().__init__(app, name, (0, 0))
        # Устанавливаем цель для камеры
        app.camera.set_target(self)
        # Смещение
        self.camera_offset = vec2(0)
        # Вектор движения
        self.movement = vec2(0)
        # Скорость
        self.speed = 0
        # Угол поворота камеры
        self.camera_angle = 0
        # Угол поворота руля
        self.steering_angle = 0
        # Атрибуты автомобиля
        self.cars_attrs = CARS_ATTRIBUTES[name]
        # Максимальная скорость вперёд
        self.max_speed = self.cars_attrs['max_speed']
        # Максимальная скорость назад
        self.reverse_speed = self.cars_attrs['reverse_speed']
        # Увеличение скорости при газе
        self.gas = self.cars_attrs['gas']
        # Уменьшение скорости при тормозе
        self.brake = self.cars_attrs['brake']
        # Замедление автомобиля
        self.slowdown = self.cars_attrs['slowdown']
        # Угол поворота камеры
        self.camera_rotation_angle = self.cars_attrs['camera_rotation_angle']
        # Шаг поворота руля
        self.step_angle = self.cars_attrs['step_rotation_angle']
        # Смещение автомобиля от ускорения
        self.acceleration_offset = 0
        # Были ли столкновение до этого
        self.time_collision = 0
        # Предыдущее состояние
        self.previous = None
        # Предпредыдущее состояние
        self.preprevious = None
        # Координаты финиша
        self.finish_line = None
        # Было ли пересечение финиша
        self.finish = False
        # Число пройденных кругов
        self.number_of_laps = 0
        # Изменение количества пройденных кругов
        self.change = 0

    # Управление игроком
    def control(self):
        # Словарь клавиш
        pressed_keys = pygame.key.get_pressed()

        k = 170 / self.app.clock.get_fps() if self.app.clock.get_fps() else 1
        # Газ
        gas = self.gas * self.app.delta_time * k
        # Тормоз
        brake = self.brake * self.app.delta_time * k
        # Замедление
        slowdown = self.slowdown * self.app.delta_time * k
        # Угол поворота руля
        step_angle = self.step_angle * self.app.delta_time
        # Угол поворота камеры
        camera_rot = self.camera_rotation_angle * self.app.delta_time

        # Если заезд не окончен
        if self.app.state == 'running':
            # Обработка движения игрока
            # Движение вперёд
            if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
                self.speed += gas
                self.acceleration_offset += 40 * gas
            # Движение назад
            if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
                self.speed -= brake
                self.acceleration_offset -= 80 * gas
            # Поворот налево
            if ((pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]) and self.speed > 0.0001 or
                    (pressed_keys[pygame.K_d] or pressed_keys[
                        pygame.K_RIGHT]) and self.speed < -0.0001):
                self.rot += math.degrees(step_angle)
                self.steering_angle -= step_angle
            # Поворот направо
            if ((pressed_keys[pygame.K_a] or pressed_keys[
                pygame.K_LEFT]) and self.speed < -0.0001 or
                    (pressed_keys[pygame.K_d] or pressed_keys[
                        pygame.K_RIGHT]) and self.speed > 0.0001):
                self.rot -= math.degrees(step_angle)
                self.steering_angle += step_angle

        # Знак числа
        sign = lambda x : 0 if x == 0 else abs(x) // x
        # Угол поворота
        angle = self.camera_angle + self.steering_angle
        # Если углы почти равны
        if abs(angle) % math.tau < 0.003:
            self.camera_angle = -self.steering_angle
        # Если угол больше 180 градусов
        elif abs(angle) % math.tau > math.pi - 0.003:
            self.camera_angle = -self.steering_angle + sign(angle) * (math.pi - 0.0031)
        # Если угол в диапазоне (0;pi)
        else:
            self.camera_angle -= sign(angle) * camera_rot

        # Ограничиваем скорость
        self.speed = min(self.max_speed, max(-self.reverse_speed, self.speed))
        # Замедление работает, если скорость не нулевая
        if abs(self.speed) > 0.0003:
            self.speed += (-1 if self.speed > 0 else 1) * slowdown
        else:
            self.speed = 0

        # Ограничиваем смещение от ускорения
        self.acceleration_offset = 15 * self.speed

        # Вычисляем вектор движения
        self.movement = vec2(0, -self.speed).rotate_rad(self.steering_angle)

        # Скорость игрока в км/ч
        self.app.speed = abs(round(20 * self.speed))

    # Сохранение текущего состояния
    def remember(self):
        # Сохраняем препредыдущее состояние
        self.preprevious = deepcopy(self.previous)
        # Сохраняем предыдущее состояние
        self.previous = {
                         'rot': deepcopy(self.rot),
                         'pos': deepcopy(self.pos),
                         'angle': deepcopy(self.angle),
                         'speed': deepcopy(self.speed / -4),
                         'movement': deepcopy(self.movement),
                         'screen_pos': deepcopy(self.screen_pos),
                         'camera_angle': deepcopy(self.camera_angle),
                         'camera_offset': deepcopy(self.camera_offset),
                         'steering_angle': deepcopy(self.steering_angle),
                         'acceleration_offset': deepcopy(self.acceleration_offset),
                        }

    # Возвращение предыдущего состояния
    def return_back(self):
        # Будем возвращать в препредыдущее состояние
        # Это сделано для большей надёжности
        self.previous = deepcopy(self.preprevious)
        # Возвращаем в препредыдущее состояние
        self.rot = deepcopy(self.previous['rot'])
        self.pos = deepcopy(self.previous['pos'])
        self.angle = deepcopy(self.previous['angle'])
        self.speed = deepcopy(self.previous['speed'])
        self.movement = deepcopy(self.previous['movement'])
        self.screen_pos = deepcopy(self.previous['screen_pos'])
        self.camera_angle = deepcopy(self.previous['camera_angle'])
        self.camera_offset = deepcopy(self.previous['camera_offset'])
        self.steering_angle = deepcopy(self.previous['steering_angle'])
        self.acceleration_offset = deepcopy(self.previous['acceleration_offset'])

    # Проверка столкновений
    def check_collision(self):
        # Список объектов, с которыми произошло стокновение
        collide = pygame.sprite.spritecollide(self, self.app.collision_group,
                                              False, pygame.sprite.collide_mask)
        # Увеличиваем время без столкновений
        self.time_collision += 1
        # Проверяем есть ли столкновение
        if len(collide) > 1:
            # Время без столкновений равно 0
            self.time_collision = 0
            # Возвращаем состояние назад
            self.return_back()
        # Проверяем прошло ли достаточно времени для нового "сохранения"
        elif self.time_collision >= 20:
            # Время без столкновений равно 0
            self.time_collision = 0
            # Сохраняем новое состояние
            self.remember()

    # Проверка перечения финиша
    def check_finish_collision(self):
        # Координаты финиша
        x, y = self.finish_line
        # Проверка на пересечение
        collsion = (x - 110 <= self.pos.x <= x + 110 and
                    y - 20 <= self.pos.y <= y + 20)
        if collsion:
            # Проверка на пересечение в верном направление
            finish = (90 < self.rot % 360 < 270 and self.speed > 0 or
                      (0 < self.rot % 360 < 90 or 270 < self.rot % 360 < 360) and self.speed < 0)
            # Если направление правильное, то увеличиваем
            if finish:
                self.change = 1
            # Иначе уменьшаем
            else:
                self.change = -1
            # Перечение было
            self.finish = True
        else:
            # Изменяем количество кругов
            self.number_of_laps += self.change
            # Изменений больше нет
            self.change = 0
            # Пересечений нет
            self.finish = False
        self.app.number_of_laps = max(self.app.number_of_laps, self.number_of_laps)

    # Обновление спрайта
    def update(self):
        super().update()
        # Движение возможно только после старта и до окончания заезда
        self.control()
        self.move()
        self.check_collision()
        self.check_finish_collision()
        self.camera.update()

    # Движение игрока
    def move(self):
        self.pos += self.movement
        self.camera_offset += self.movement

    # Поворот игрока на угол в градусах
    def rotate(self, angle):
        self.rot -= math.degrees(angle)
        self.camera_angle += angle
        self.steering_angle -= angle
