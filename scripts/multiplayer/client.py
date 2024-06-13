import json
import socket
from scripts.game.stacked_sprite import StackedSprite
from scripts.settings import *


# Класс клиента
class Client:
    def __init__(self, app, address):
        # Приложение
        self.app = app
        # Создаём сокет
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Подключаемся к айпи адресу сервера
        self.sock.connect(address)
        # Список для хранения данных об игроках
        self.players = []
        # Id игрока
        self.player_id = self.get_id()
        # Место в гонке
        self.place = 0
        # Параметры
        self.options = {'state': 'waiting', 'time': 10 ** 10}

    def finish(self):
        # Отправляем серверу запрос
        self.sock.sendall(bytes(json.dumps({'request': 'finish'}), 'UTF-8'))
        # Получаем информацию
        received = json.loads(self.sock.recv(1024).decode('UTF-8'))
        # Возвращаем id
        self.place = received['response']

    # Установить приложение
    def set_app(self, app):
        self.app = app

    # Выход из игры
    def exit_the_game(self):
        self.sock.sendall(bytes(json.dumps({'request': 'disconnect'}), 'UTF-8'))

    # Получение id игрока
    def get_id(self):
        # Отправляем серверу запрос
        self.sock.sendall(bytes(json.dumps({'request': 'get_id'}), 'UTF-8'))
        # Получаем информацию
        received = json.loads(self.sock.recv(1024).decode('UTF-8'))
        # Возвращаем id
        return received['response']

    # Получение параметров
    def get_options(self):
        # Отправляем серверу запрос для получения параметров
        self.sock.sendall(bytes(json.dumps({'request': 'get_options'}), 'UTF-8'))
        # Получаем информацию о параметрах
        received = json.loads(self.sock.recv(1024).decode('UTF-8'))
        # Сохраняем результат запроса в переменную
        self.options = received['response']

    # Получить информацию об игроках
    def get_players(self):
        # Отправляем серверу запрос для получения игроков
        self.sock.sendall(bytes(json.dumps({'request': 'get_players'}), 'UTF-8'))
        # Получаем информацию об игроках
        received = json.loads(self.sock.recv(1024).decode('UTF-8'))
        # Сохраняем результат запроса в переменную
        self.players = received['response']

    # Обновить информацию об игроках в приложение
    def update_players(self):
        # Просматриваем всех активных игроков
        for player in self.players:
            # Если не проверяем самого себя
            if player['id'] != self.player_id:
                # Если игрок только зашёл на сервер
                if player['id'] not in self.app.players.keys():
                    name, pos, rot, car = player['name'], vec2(player['pos']), player['rot'], player['car']
                    if car != '':
                        self.app.players[player['id']] = StackedSprite(self.app, car, pos, rot)
                # Иначе обновляем положение игрока
                else:
                    player_id, pos, rot = player['id'], vec2(player['pos']), player['rot']
                    self.app.players[player_id].pos = pos
                    self.app.players[player_id].rot = rot
        all_id = map(lambda el: el['id'], self.players)
        del_id = []
        for player_id in self.app.players.keys():
            if player_id not in all_id:
                del_id.append(player_id)
        for player_id in del_id:
            self.app.players[player_id].kill()
            del self.app.players[player_id]

    def get_state(self):
        return self.options['state']

    def update_name(self, name):
        # Запрос
        request = {
            'request': 'update_name',
            'name': name,
        }
        # Отправляем серверу запрос на изменение положения
        self.sock.sendall(bytes(json.dumps(request), 'UTF-8'))

    # Обновить иноформация игрока
    def update(self, player):
        # Получить параметры
        self.get_options()
        # Получить информацию об игроках
        self.get_players()
        # Обновить информацию об игроках в приложение
        self.update_players()
        # Запрос
        request = {
            'request': 'update_position',
            'pos': tuple(player.pos),
            'rot': player.rot,
            'name': player.name,
            'car': player.name,
        }
        # Отправляем серверу запрос на изменение положения
        self.sock.sendall(bytes(json.dumps(request), 'UTF-8'))
