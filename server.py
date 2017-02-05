# Веб-сервер на микрофреймворке flask

import time
import json

from flask import Flask, request, render_template, redirect, abort
from tinydb import TinyDB, Query

import main


class Updater:
    def __init__(self, time_limit=60, tinydb=False):
        # Запросы производить не чаще, чем раз в time_limit секунд
        # Здесь можно прикрутить БД, что бы освободить память
        self.tinydb = tinydb
        self.time_limit = time_limit
        if tinydb is False:
            self.updates = {}
            self.last_data = {}
        else:
            self.db = TinyDB('db.json')
        return

    def get_update(self, godname, h=False, ascii_=False):
        # выбираем как обрабатывать запросы: с базой данных или только в памяти
        if self.tinydb is True:
            return self.get_update_db(godname, h=h, ascii_=ascii_)
        else:
            return self.get_update_nodb(godname, h=h, ascii_=ascii_)

    def get_update_nodb(self, godname, h=False, ascii_=False):
        # Если это первый запрос для данного бога
        # или прошло больше минуты ( по умолчанию)
        if godname not in self.updates or \
           self.updates[godname]+self.time_limit < time.time():
            self.last_data[godname] = main.api_request(godname)
            self.updates[godname] = int(time.time())
        if h is False:
            return json.dumps(self.last_data[godname], ensure_ascii=ascii_)
        else:
            return json.dumps(self.last_data[godname], ensure_ascii=ascii_, indent=2)

    def get_update_db(self, godname, h=False, ascii_=False):
        query = Query()
        last_data = self.db.search(query.godname == godname)
        if len(last_data) == 0:
            data_ = main.api_request(godname)
            self.db.insert({"godname": godname, "data": data_})
            answer = data_
            print("First time")
        else:
            last_update = last_data[0]["data"]["update_time"]
            print("Not first time")
            if last_update+self.time_limit > int(time.time()):
                answer = last_data[0]["data"]
                print("Less than minute")
            else:
                data_ = main.api_request(godname)
                self.db.remove(query.godname == godname)
                self.db.insert({"godname": godname, "data": data_})
                answer = data_
                print("More than minute")

        if h is False:
            return json.dumps(answer, ensure_ascii=ascii_)
        else:
            return json.dumps(answer, ensure_ascii=ascii_, indent=2)


app = Flask(__name__)
update = Updater(tinydb=True)


@app.route("/")
def main_page():
    if request.query_string == b"":
        return render_template('index.html')
    else:
        godname = request.args.get("godname")
        h, ascii_ = request.args.get("h"), request.args.get("ascii")
        redirect_url = godname + "?"
        if h is not None:
            redirect_url += "h=1&"
        if ascii_ is not None:
            redirect_url += "ascii=1"
        return redirect(redirect_url)


@app.route("/<godname>")
def api_request(godname):
    if godname == "":
        return
    h, ascii_ = request.args.get("h"), request.args.get("ascii")
    # Если эти пункты есть, то они станут True, а если None, то False
    h = h is not None
    ascii_ = ascii_ is not None
    global update
    try:
        return update.get_update(godname, h, ascii_)
    except NameError:
        abort(404)
