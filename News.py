import random
import json
import time
from pprint import pprint

import telebot as tel
import wikipedia
import requests
import Tokens
from newsapi import NewsApiClient

token = Tokens.TOKEN_NEWS
creator = Tokens.CREATOR

bot = tel.TeleBot(token)

dict_id = {}


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.from_user.id,
                     "Привет! Это бот о новостях")


@bot.message_handler(commands=["send_admin"])
def send_admin(message):
    t = message.text.split()
    v = " ".join(t[2:])
    g = t[1]
    print(g, v)
    try:
        bot.send_message(g, v)
        # bot.send_message(message.from_user.id, f"Обработано, всё красиво")
    except tel.apihelper.ApiTelegramException as Error:
        bot.send_message(message.from_user.id, f"Обработано, {Error}")


def news_api(request):
    # newsapi = NewsApiClient(api_key=Tokens.NEWS_API)
    # top_headlines = newsapi.get_top_headlines(q='Майнкрафт',
    #                                           language='ru')
    # print(top_headlines)

    answer = requests.get(f"https://newsapi.org/v2/everything?q={request}&language=ru&apiKey={Tokens.NEWS_API}")
    pprint(answer.json())
    x = answer.json()

news_api("Майнкрафт")


def open_file_r(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def open_file_w(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


bot.polling()

"""
Юзеру отправлять сообщение мы научились, теперь нужно сделать наоборот (по какой-то команде отправить сообщение создателю), подсказка: есть функция forward_message 

2. Достать красиво все данные из переменной x и отправить их в ответ на сообщение отправителя.
Все новости должны быть запакованы в одну переменную (это важно, чтобы не бот не спамил юзеру)

3. Обрабатывать все ошибки в процессе
"""
