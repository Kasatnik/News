import random
import json
import time
import telebot as tel
import wikipedia
import requests
import Tokens

token = Tokens.TOKEN_NEWS
creator = Tokens.CREATOR

bot = tel.TeleBot(token)

dict_id = {}


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.from_user.id,
                     "Привет! Это бот о новостях")



def open_file_r(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def open_file_w(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


bot.polling()


"""
Сделать команду для админа, которая поможет отправлять сообщения пользователям.
Создатель пишет: "/send 38547387 привет, как твои дела?" - это сообщение будет срабатывать по команде /send
Бот должен разделить команду /send, затем айдишник и само сообщение с помощью функции split(), то есть, в таком виде:
["/send", "3458934873", "привет..."] - вот такой результат должен быть
Мы достаём айдишник из списка и просто юзаем bot.send_message...

"""