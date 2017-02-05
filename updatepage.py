#!/usr/bin/python3
# Пример скрипта для запросов с сохранением данных в csv файл.
# Его можно добавить в крон для ежедневных записей, например.
import time
import os.path

from page_parser import GodPageParser
import requests

history_file_path = "history.csv"
god_page = "https://godville.net/gods/Example"

if not os.path.is_file(history_file_path):
    with open(history_file_path, "w") as history:
        history.write("time, level, tr_level, creatures_m, creatures_f, creatures_%, money, monsters, deaths, savings\n")

with open(history_file_path, "a") as history:
    page = requests.get().text
    a = GodPageParser(page).get()
    res = str(int(time.time())) + "," + str(a["hero_lvl"]) + "," + str(a["trader_lvl"]) + \
          "," + str(a["creatures_m"]) + "," + str(a["creatures_f"]) + \
          "," + str(a["creatures_percent"]) + "," + str(a["gold"]) + \
          "," + str(a["monsters"]) + "," + str(a["deaths"]) + "," + str(a["savings"])

    history.write(res+"\n")
