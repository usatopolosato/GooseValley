from scripts.settings import *


# Класс камеры
class Camera():
    def __init__(self):
        # Смещение
        self.offset = vec2(0)
        # Угол поворота
        self.angle = 0
        # Цель
        self.target = None

    # Установить цель
    def set_target(self, target):
        self.target = target

    # Обновление камеры
    def update(self):
        self.offset = self.target.camera_offset
        self.angle = self.target.camera_angle
