from telebot import types
def lang_buttons():
    markup = types.InlineKeyboardMarkup()
    fir_button = types.InlineKeyboardButton(text="Русский🇷🇺", callback_data="en")
    sec_button = types.InlineKeyboardButton(text="English🇬🇧", callback_data="ru")
    third_button = types.InlineKeyboardButton(text="Spain🇪🇸", callback_data="es")
    markup.add(fir_button, sec_button, third_button)
    return markup