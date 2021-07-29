from telebot import TeleBot 
import config
from datetime import datetime
from functions import get_chat_member, copy_message
import keyboards
from database import db
import json
bot = TeleBot(config.Token)
@bot.message_handler(commands = ["start"])
def start(message):
    try:
        id = message.from_user.id
        name = message.from_user.first_name
        Username =  message.from_user.username
        if get_chat_member(id):
            bot.send_message(id, config.start_text.format(name, bot.get_me().username, ""),parse_mode="html")
            if db().filter("users", "id", id):
                print("Finded!")
            else:
                db().add("users", id, name,Username,0)
            keys = []
            for button in db().filter("keyboards", "markup_name","/start" , all=True):
                if message.text == button[0]:
                    keys.append(button[1])
            if keys:
                bot.send_message(id, "Tanlang!", reply_markup=keyboards.markup(keys))
                return True
        else:
            bot.send_message(id, config.start_text.format(name, bot.get_me().username, config.member_text),reply_markup=keyboards.member(),parse_mode="html")
    except:
        print("xato")
@bot.message_handler(content_types=["text"])
def text(message):
    try:
        id = message.from_user.id
        if id in config.admins and message.text == "/rek":
            db().update("users", "step", "rek", "id", id)
            bot.send_message(id, "Send me Reklama👇")
        elif id in config.admins and message.text[:9] == "addbutton":
            text = list(str(message.text).split())
            db().add("keyboards",text[1], text[2])
            bot.send_message(id ,f"<b>{text[2]}  qo'shildi!</b>", parse_mode="html")
        elif id in config.admins:
            db().update("users", "step", message.text, "id", id)
            bot.send_message(id, "Send me Content👇")
        else:
            keys = []
            for button in db().filter("keyboards","markup_name",message.text):
                keys.append(button[1])
            if keys:
                bot.send_message(id, "Tanlang!", reply_markup=keyboards.markup(keys))
                return True
            for content in db().filter("contents", "button_name", message.text):
                copy_message(id, content[1],content[2])
    except:
        print("xato")
@bot.message_handler(content_types=["sticker", "photo", "audio","voice", "document", "video"])
def photo(message):
    try:
        id = message.from_user.id
        message_id = message.message_id
        step = db().filter("users","id", id)[0][3]
        if step == "rek":
            users = 0
            for user in db().filter("users", "","",all=True):
                try:
                    copy_message(user[0],message.message_id, id)
                    users += 1
                except:
                    print("ooooops")
            bot.send_message(id, f"<code>Foydalanuvchilar soni: <b>{users}</b> ta</code>\n<i>{datetime.now().strftime('%d.%m.%y  %H:%M holatiga ko`ra')}</i>\n@{bot.get_me().username}", parse_mode='html')

            db().update("users", "step", 0, "id", id)
        elif step != "break" and id in config.admins:
            db().add("contents", step, message_id, id)
    except:
        print("xato")
print("Starting...")
bot.polling()