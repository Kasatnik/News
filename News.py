import random
import json
import time
from pprint import pprint

import telebot as tel
import wikipedia
import requests
import Tokens
from newsapi import NewsApiClient
from telebot import types

token = Tokens.TOKEN_NEWS
creator = Tokens.CREATOR

bot = tel.TeleBot(token)

dict_id = {}


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    fir_button = types.InlineKeyboardButton(text="Новости", callback_data="news")
    sec_button = types.InlineKeyboardButton(text="Связаться с админом", callback_data="send_admin")
    third_button = types.InlineKeyboardButton(text="Сменить язык", callback_data="send_admin")
    markup.add(fir_button, sec_button)
    bot.send_message(message.from_user.id,
                     "Привет! Это бот о новостях", reply_markup=markup)

@bot.callback_query_handler(func = lambda call: call.data == "news")
def news(cb):
    print(cb)

@bot.callback_query_handler(func = lambda call: call.data == "send_admin")
def sendadmin(cb):
    print(cb)




@bot.message_handler(commands=["send_user"])
def send_user(message):
    t = message.text.split()
    v = " ".join(t[2:])
    g = t[1]
    print(g, v)
    try:
        bot.send_message(g, v)
        # bot.send_message(message.from_user.id, f"Обработано, всё красиво")
    except tel.apihelper.ApiTelegramException as Error:
        bot.send_message(message.from_user.id, f"Обработано, {Error}")


@bot.message_handler(commands=["send_admin"])
def send_admin(message):
    s = message.text[11:]
    print(s)
    bot.send_message(creator, f"{s}, от {message.from_user.first_name} {message.from_user.username}")

def news_api(request):
    # newsapi = NewsApiClient(api_key=Tokens.NEWS_API)
    # top_headlines = newsapi.get_top_headlines(q='Майнкрафт',
    #                                           language='ru')
    # print(top_headlines)

    answer = requests.get(f"https://newsapi.org/v2/everything?q={request}&language=ru&apiKey={Tokens.NEWS_API}")
    pprint(answer.json())
    x = answer.json()
    # bot.send_message(message.from_user.id, x["articles"]["author"]["description"][])

# news_api("Minecraft")


def open_file_r(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def open_file_w(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


bot.polling()

"""
1. Создать базу данных в самом начале коде и в ней таблицу:
Столбцы:
айди_тг
...
...
язык_юзера ИНТЕДЖЕР (это будет число)


При нажатии на кнопку "Старт" добавлять нового юзера в базу данных
"""
