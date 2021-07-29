from telebot import types
import config
from database import db
def member():
    markup = types.InlineKeyboardMarkup()
    for text in db().filter("channels", "","",all=True):
        markup.add(
            types.InlineKeyboardButton(text=text[0], url="https://t.me/" + text[1])
        )
    return markup
def markup(keys,start):
    object = types.ReplyKeyboardMarkup(True)
    key_pop = ""
    if len(keys) % 2 != 0:
        key_pop = keys.pop()
    for key_ in range(0, len(keys) , 2):
        key=keys[key_]
        object.row(types.KeyboardButton(key), types.KeyboardButton(keys[keys.index(key) +1]))
    if key_pop:
        object.row(types.KeyboardButton(key_pop))
    if start != "/start":
        object.row(types.KeyboardButton("🔙Orqaga"), types.KeyboardButton("🔝Bosh Sahifa"))
    return object

