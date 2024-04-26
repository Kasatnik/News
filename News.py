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
import sqlite3

from Buttons import lang_buttons

token = Tokens.TOKEN_NEWS
creator = Tokens.CREATOR

bot = tel.TeleBot(token)

dict_id = {}


def create_table():
    with sqlite3.connect("server.db") as db:
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
        ID_TG INTEGER,
        user_name TEXT,
        language INTEGER,
        first_name TEXT,
        last_name TEXT)""")
        db.commit()


def register(message):
    with sqlite3.connect("server.db") as db:
        sql = db.cursor()
        sql.execute(f"SELECT ID_TG FROM users WHERE ID_TG = {message.from_user.id}")
        if sql.fetchone() is None:
            sql.execute(
                f"INSERT INTO users VALUES ({message.from_user.id}, '{message.from_user.username}', 2, '{message.from_user.first_name}', '{message.from_user.last_name}')")
            db.commit()


@bot.message_handler(commands=["start"])
def start(message):
    register(message)
    markup = types.InlineKeyboardMarkup()
    fir_button = types.InlineKeyboardButton(text="Новости", callback_data="news")
    sec_button = types.InlineKeyboardButton(text="Связаться с админом", callback_data="send_admin")
    third_button = types.InlineKeyboardButton(text="Сменить язык", callback_data="lang")
    markup.add(sec_button, third_button).add(fir_button)
    bot.send_message(message.from_user.id,
                     "Привет! Это бот о новостях", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "news")
def news(cb):
    print(cb)
    bot.send_message(cb.from_user.id, "Введите запрос по новостям")
    bot.register_next_step_handler(cb, send_admin)


@bot.callback_query_handler(func=lambda call: call.data == "lang")
def lang(cb):
    markup = lang_buttons()
    bot.send_message(cb.from_user.id, "Выберите язык", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "send_admin")
def sendadmin(cb):
    bot.send_message(cb.from_user.id, "Введите что вы хотите отправить админу")
    bot.register_next_step_handler(cb, send_admin)


def send__admin(cb):
    print(cb)


@bot.message_handler(commands=["send_user"])
def send_user(message):
    t = message.text.split()  # TODO: сделать только для админа
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


create_table()
bot.polling()

"""

"""
