import json
import time
import socket
from threading import Thread
from scripts.settings import HOST, PORT, MAX_PLAYERS


# Класс сервера
class Server:
    def __init__(self, address, max_connections):
        # Создаём сокет
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Запускаем сервер от заданного адреса
        self.socket.bind(address)
        # Максимальное количество игроков
        self.max_players = max_connections
        # Список игроков на сервере
        self.players = []
        # Количество игроков в игре
        self.number_of_players_in_the_game = 0
        # Устанавливаем максимальное кол-во прослушиваний на сервере
        self.socket.listen(self.max_players)
        self.place = 0
        # Параметры
        self.options = {'state': 'waiting',
                        'time': 10 ** 10,
                        }

    def run(self):
        Thread(target=self.game_processing).start()
        Thread(target=self.listen).start()

    def tick(self):
        time.sleep(1)
        self.options['time'] -= 1

    def game_processing(self):
        while True:
            self.tick()
            print(f"state: {self.options['state']}, time: {self.options['time']}", end=' ')
            print(f'number: {self.number_of_players_in_the_game}')
            if self.number_of_players_in_the_game == 0:
                if self.options['state'] == 'waiting':
                    self.place = 0
                    if len(self.players) >= 7:
                        self.options['time'] = min(self.options['time'], 15)
                    if len(self.players) >= 5:
                        self.options['time'] = min(self.options['time'], 30)
                    if len(self.players) >= 3:
                        self.options['time'] = min(self.options['time'], 60)
                    if len(self.players) >= 2:
                        self.options['time'] = min(self.options['time'], 10)
                    if len(self.players) <= 1:
                        self.options['time'] = 10 ** 10

                    if self.options['time'] == 0:
                        self.number_of_players_in_the_game = len(self.players)
                        self.options['time'] = 420
                        self.options['state'] = 'running'
                elif self.options['state'] == 'running':
                    if self.options['time'] == 0:
                        self.options['time'] = 10 ** 10
                        self.options['state'] = 'waiting'
            else:
                self.options['time'] = 10 ** 10

    # Основной поток сервера
    def listen(self):
        while True:
            if len(self.players) < self.max_players:
                # Одобряем подключение, получаем взамен адрес и другую информацию о клиенте
                connect, address = self.socket.accept()
                # Выводим информацию о новом подключение
                print('New connection', address)
                # Запускаем в новом потоке проверку действий игрока
                Thread(target=self.handle_client, args=(connect,)).start()

    # Взаимодействие с игроком
    def handle_client(self, connect):
        # Настраиваем стандартные данные для игрока
        player = {
            'id': 0,
            'pos': 0,
            'rot': 0,
            'name': '',
            'car': '',
        }
        # Добавляем в список игроков
        self.players.append(player)
        # Переменная для цикла
        run = True
        was_the_game = False
        while run:
            if self.options['state'] == 'running':
                was_the_game = True
            self.players[self.players.index(player)]['id'] = self.players.index(player)
            # Ждём запросов от клиента
            data = connect.recv(1024)
            # Если запросы перестали поступать, то отключаем игрока от сервера
            if not data:
                run = False
            # Загружаем все запросы
            requests = json.loads(f"[{data.decode('utf-8').replace('}{', '},{')}]")
            # Просматриваем все запросы
            for data in requests:
                # Запрос на получение игроков на сервере
                if data['request'] == 'get_players':
                    connect.sendall(bytes(json.dumps({
                        'response': self.players
                    }), 'UTF-8'))
                # Запрос на получение id
                if data['request'] == 'get_id':
                    connect.sendall(bytes(json.dumps({
                        'response': player['id']
                    }), 'UTF-8'))
                if data['request'] == 'get_options':
                    connect.sendall(bytes(json.dumps({
                        'response': self.options
                    }), 'UTF-8'))
                # Запрос на обновление положения
                if data['request'] == 'update_position':
                    player['pos'] = data['pos']
                    player['rot'] = data['rot']
                    player['car'] = data['car']
                if data['request'] == 'update_name':
                    player['name'] = data['name']
                if data['request'] == 'finish':
                    self.place += 1
                    connect.sendall(bytes(json.dumps({
                        'response': self.place,
                    }), 'UTF-8'))
                # Запрос на отключение
                if data['request'] == 'disconnect':
                    run = False
        # Если игрок вышел или его выкинуло с сервера, то удалить
        print('Disconnect', player['id'])
        self.number_of_players_in_the_game -= int(was_the_game)
        if self.number_of_players_in_the_game == 0:
            self.options['state'] = 'waiting'
            self.place = 0
        self.players.remove(player)


if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)
    server.run()
