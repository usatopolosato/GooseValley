from scripts.gui.screensaver import start_screen
from scripts.gui.main_menu import main_menu
from scripts.game.cache import Cache
import json
from scripts.gui.authorization import authorization


# Инициализация класса кеширования
def init(cache):
    cache.append(Cache())
    cache[0] = True


if __name__ == '__main__':
    list_players = {'name': []}
    with open('settings.json', 'w') as file:
        json.dump(list_players, file, ensure_ascii=True)
    cache = Cache()
    if start_screen():
        if authorization():
            main_menu(cache, 'ford_f-150')
