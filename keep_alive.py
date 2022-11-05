from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "London Bus Checker Telegram Bot - https://github.com/rhysyim/londonBusCheckerTelegramBot"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
