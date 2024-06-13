from scripts.gui.screensaver import start_screen
from scripts.gui.main_menu import main_menu
from scripts.game.cache import Cache
import json
from scripts.gui.authorization import authorization
from threading import Thread


# Инициализация класса кеширования
def init(cache):
    cache.append(Cache())
    cache[0] = True


if __name__ == '__main__':
    result = [True]
    cache = [False]
    t1 = Thread(target=start_screen, args=(result, cache, ), daemon=True)
    t2 = Thread(target=init, args=(cache, ), daemon=True)
    t1.start()
    t2.start()

    #list_players = {'name': []}
    #with open('settings.json', 'w') as file:
    #    json.dump(list_players, file, ensure_ascii=True)
    while not cache[0]:
        ...
    if result[0]:
        cache = cache[1]
        if authorization():
            main_menu(cache, 'ford_f-150')
