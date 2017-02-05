# Веб-сервер на микрофреймворке flask

import time
import json

from flask import Flask, request, render_template, redirect, abort

import main


class Updater:
    def __init__(self, time_limit=60):
        # Запросы производить не чаще, чем раз в time_limit секунд
        # Здесь можно прикрутить БД, что бы освободить память
        self.updates = {}
        self.time_limit = time_limit
        self.last_data = {}
        return

    def get_update(self, godname, h=False, ascii_=False):
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


app = Flask(__name__)
update = Updater()


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
    except Exception:
        abort(404)
