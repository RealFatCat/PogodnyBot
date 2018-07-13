#!/usr/bin/env python3

import requests
import time
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELE_TOKEN = 'tele_token'

OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
OPENWEATHER_TOKEN = 'openweather_token'


class WeatherApi(object):
    def __init__(self, base_api_url, token_file):
        self.base_api_url = base_api_url
        self.token = self.read_token_file(token_file)

    @staticmethod
    def read_token_file(token_file):
        with open(token_file) as f:
            return f.readline().strip()

    def get_weather(self, city='Moscow'):
        params = {
            'q': city,
            'appid': self.token,
            'units': 'metric',
        }

        print(params)
        responce = requests.get(self.base_api_url, params=params)
        temp = responce.json()['main']['temp']
        humidity = responce.json()['main']['humidity']
        wind = responce.json()['wind']['speed']
        return temp, humidity, wind


def run():
    weather = WeatherApi(OPENWEATHER_API_URL, OPENWEATHER_TOKEN)
    tele_updater = Updater(token=WeatherApi.read_token_file(TELE_TOKEN))
    tele_dispatcher = tele_updater.dispatcher

    def start_bot(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Send city name to get weather for it")
    start_handler = CommandHandler('start', start_bot)
    tele_dispatcher.add_handler(start_handler)

    def city(bot, update, args):
        resp = weather.get_weather(' '.join(args))
        text = 'Temp: {}, Humidity: {}, WindSpeed: {}'.format(*resp)
        bot.send_message(chat_id=update.message.chat_id, text=text)
    city_handler = CommandHandler('city', city, pass_args=True)
    tele_dispatcher.add_handler(city_handler)

    tele_updater.start_polling()


if __name__ == '__main__':
    run()
