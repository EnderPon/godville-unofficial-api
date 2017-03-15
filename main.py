# Главный скрипт, который
import time

import requests

from page_parser import GodPageParser
from api_parser import ApiParser


def api_request(god_name, token=None):
    # запрашиваем страницу бога, малое апи и объеденяем, попутно приписывая время
    # когда был получен этот результат
    god_page = requests.get("https://godville.net/gods/" + god_name)
    time.sleep(1)
    if token is not None:
        api_page = requests.get("https://godville.net/gods/api/" + god_name + "/" + token)
    else:
        api_page = requests.get("https://godville.net/gods/api/" + god_name)
    god_page_parsed = GodPageParser(god_page.text).get()
    if api_page.status_code == 200:
        api_parsed = ApiParser(api_page.json()).get()
    else:
        # В некоторых случаях, малое АПИ возвращает ошибку 500
        # Тогда мы будем считать, что оно пустое
        api_parsed = {}
    god_page_parsed.update(api_parsed)
    god_page_parsed.update({"update_time": int(time.time())})
    return god_page_parsed
