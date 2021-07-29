from telebot import types
import config
def member():
    markup = types.InlineKeyboardMarkup()
    for text in config.KanalvaGuruhlar:
        markup.add(
            types.InlineKeyboardButton(text=text[0], url="https://t.me/" + text[1])
        )
    return markup
def markup(keys):
    object = types.ReplyKeyboardMarkup(True)
    key_pop = ""
    if len(keys) % 2 != 0:
        key_pop = keys.pop()
    for key_ in range(0, len(keys) , 2):
        key=keys[key_]
        object.row(types.KeyboardButton(key), types.KeyboardButton(keys[keys.index(key) +1]))
    if key_pop:
        object.row(types.KeyboardButton(key_pop))
    return object

