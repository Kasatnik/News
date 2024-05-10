from telebot import types


def lang_buttons(g: int)-> types.InlineKeyboardMarkup:
    dict_lang = {1: ("Return home",),
                 2: ("Вернуться домой",),
                 3: ("Volver a casa",)}
    markup = types.InlineKeyboardMarkup()
    fir_button = types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru")
    sec_button = types.InlineKeyboardButton(text="English🇬🇧", callback_data="en")
    third_button = types.InlineKeyboardButton(text="Spain🇪🇸", callback_data="es")
    fourth_button = types.InlineKeyboardButton(text=dict_lang[g][0], callback_data="return_home")
    markup.add(fir_button, sec_button, third_button).add(fourth_button)
    return markup


def lang_change(g: int)-> types.InlineKeyboardMarkup:
    dict_lang = {1: ("News", "Contact with admin", "Change language", "Return home"),
                 2: ("Новости", "Связаться с админом", "Сменить язык", "Вернуться домой"),
                 3: ("Noticias", "Contactar al administrador", "Cambiar idioma", "Volver a casa")}
    markup = types.InlineKeyboardMarkup()
    fir_button = types.InlineKeyboardButton(text=dict_lang[g][0], callback_data="news")
    sec_button = types.InlineKeyboardButton(text=dict_lang[g][1], callback_data="send_admin")
    third_button = types.InlineKeyboardButton(text=dict_lang[g][2], callback_data="lang")

    markup.add(sec_button, third_button).add(fir_button)
    return markup