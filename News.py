import random
import json
import time
from pprint import pprint
from typing import Any

import telebot as tel
import wikipedia
import requests
import Tokens
from newsapi import NewsApiClient
from telebot import types
import sqlite3

from Buttons import lang_buttons, lang_change

token = Tokens.TOKEN_NEWS
creator = Tokens.CREATOR

bot = tel.TeleBot(token)

dict_id = {}


def create_table()->None:
    with sqlite3.connect("server.db") as db:
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
        ID_TG INTEGER,
        user_name TEXT,
        language INTEGER,
        first_name TEXT,
        last_name TEXT)""")
        db.commit()


def set_language_by_id_tg(tel_id: Any[int, str], language):
    with sqlite3.connect("server.db") as db:
        sql = db.cursor()
        sql.execute("UPDATE users SET language = ? WHERE ID_TG = ?", (language, tel_id))
        db.commit()


def register(message):
    with sqlite3.connect("server.db") as db:
        sql = db.cursor()
        sql.execute(f"SELECT ID_TG FROM users WHERE ID_TG = {message.from_user.id}")
        if sql.fetchone() is None:
            sql.execute(
                f"INSERT INTO users VALUES ({message.from_user.id}, '{message.from_user.username}', 2, '{message.from_user.first_name}', '{message.from_user.last_name}')")
            db.commit()


def check_language(ID_TG):
    with sqlite3.connect("server.db") as db:
        sql = db.cursor()
        sql.execute("SELECT language FROM users WHERE ID_TG = ?", (ID_TG,))
        return sql.fetchone()[0]


@bot.message_handler(commands=["start"])
def start(message):
    register(message)
    k = check_language(ID_TG=message.from_user.id)
    markup = lang_change(k)
    bot.delete_message(message.from_user.id, message.message_id)
    bot.send_animation(message.from_user.id, open("Images/robotgif.gif", 'rb'), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "news")
def news(cb):
    bot.delete_message(cb.from_user.id, cb.message.message_id)
    print(cb)
    h = ["Choose language🗞", "Введите запрос по новостям🗞", "Ingrese su consulta de noticias🗞"]
    l = check_language(cb.from_user.id)
    o = bot.send_message(cb.from_user.id, h[l - 1])
    bot.register_next_step_handler(o, news_api)


@bot.callback_query_handler(func=lambda call: call.data == "return_home")
def news(cb):
    bot.delete_message(cb.from_user.id, cb.message.message_id)
    start(cb.message)

@bot.callback_query_handler(func=lambda call: call.data == "lang")
def lang(cb):
    print(cb)
    h = ["Choose language", "Выберите язык", "Elige lengua"]
    l = check_language(cb.from_user.id)
    markup = lang_buttons(g=l)
    bot.delete_message(cb.from_user.id, cb.message.message_id)
    bot.send_message(cb.from_user.id, h[l-1], reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["ru", "en", "es"])
def all_lang(cb):
    print(cb.data)
    if cb.data == "ru":
        set_language_by_id_tg(tel_id=cb.from_user.id, language=2)
    if cb.data == "en":
        set_language_by_id_tg(tel_id=cb.from_user.id, language=1)
    if cb.data == "es":
        set_language_by_id_tg(tel_id=cb.from_user.id, language=3)


@bot.callback_query_handler(func=lambda call: call.data == "send_admin")
def sendadmin(cb):
    bot.delete_message(cb.from_user.id, cb.message.message_id)
    h = ["What do you want to send to the admin?", "Что вы хотите отправить админу?", '¿Qué quieres enviar al administrador?']
    l = check_language(cb.from_user.id)
    bot.send_message(cb.from_user.id, h[l - 1])
    bot.register_next_step_handler(cb.message, send__admin)


def send__admin(message):
    print(message)
    print("ok")
    # bot.send_message(creator, message.text)

    bot.delete_message(message.from_user.id, message.message_id)
    bot.delete_message(message.from_user.id, message.message_id - 1)
    h = ["Shipped", "Отправлено",
         'Enviado']
    l = check_language(message.from_user.id)
    bot.send_message(message.from_user.id, h[l - 1])
    start(message)


@bot.message_handler(commands=["send_user"])
def send_user(message):
    if message.from_user.id == creator:
        t = message.text.split()  # TODO: сделать только для админа
        v = " ".join(t[2:])
        g = t[1]
        print(g, v)
        try:
            bot.send_message(g, v)
            # bot.send_message(message.from_user.id, f"Обработано, всё красиво")
        except tel.apihelper.ApiTelegramException as Error:
            print(f"Обработано {Error}")
    else:
        h = ["You are not an admin😔", "Ты не админ😔",
             'No eres un administrador😔']
        l = check_language(message.from_user.id)
        bot.delete_message(message.from_user.id, message.message_id)
        bot.send_message(message.from_user.id, h[l - 1])
        return


@bot.message_handler(commands=["send_admin"])
def send_admin(message):
    s = message.text[11:]
    print(s)
    bot.delete_message(message.from_user.id, message.message_id)
    bot.send_message(creator, f"{s}, от {message.from_user.first_name} {message.from_user.username}")


def news_api(message):
    # newsapi = NewsApiClient(api_key=Tokens.NEWS_API)
    # top_headlines = newsapi.get_top_headlines(q='Майнкрафт',
    #                                           language='ru')
    # print(top_headlines)
    v = check_language(ID_TG=message.from_user.id)

    answer = requests.get(f"https://newsapi.org/v2/everything?q={message.text}&language={['en','ru','es'][v-1]}&apiKey={Tokens.NEWS_API}")
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
1. потестить испанский язык (составить запросы на испанском)
2. выставить bot.delete_message в нужных местах, чтобы была чистота в боте)
3. в теме "связаться с админом", когда бот пишет: "Напиши ваш вопрос админу" (типа того) добавить inline кнопку "Вернуться домой". При нажатии на эту кнопку - просто сделать обработчик, который просто вернёт человека в главное меню)
3.1. в разделе "Русский, English, Spain" также сделать кнопку для возврата в главное меню)
3.2. с новостями, думаю, аналогично) подумай, как тут бы ты хотел это реализовать
4. по желанию: в разных разделах вставить красивые анимации/картинки (найти в гугле)
"""
