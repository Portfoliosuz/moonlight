from telebot import TeleBot 
import config
from datetime import datetime
from functions import get_chat_member, copy_message,send_tanleng
import keyboards
import json
from database import db
bot = TeleBot(config.Token)
@bot.message_handler(commands = ["start"])
def start(message):
    id = message.from_user.id
    name = message.from_user.first_name
    Username = message.from_user.username
    try:
        if get_chat_member(id):
            bot.send_message(id, config.start_text.format(name, bot.get_me().username, ""),parse_mode="html")
            if db().filter("users", "id", id):
                print("Finded!")
            else:
                db().add("users", id, name,Username,0)
            send_tanleng(bot, id,message.text)
        else:
            bot.send_message(id, config.start_text.format(name, bot.get_me().username, config.member_text),reply_markup=keyboards.member(),parse_mode="html")
    except:
        print("xato")
@bot.message_handler(content_types=["text"])
def text(message):
    try:
        id = message.from_user.id
        name = message.from_user.first_name
        if id in config.admins:
            if message.text == "/rek":
                db().update("users", "step", "rek", "id", id)
                bot.send_message(id, "Send me Reklama👇")
            elif message.text[:9] == "addbutton":
                dic = json.loads(message.text[9:])
                for c in dic.keys():
                    db().add("keyboards", c, dic[c])
                    bot.send_message(id, f"<b>{dic[c]}  qo'shildi!</b>", parse_mode="html")
            elif message.text == "copy_all":
                try:
                    db().copy_all_info("users")
                    db().copy_all_info("contents")
                    db().copy_all_info("keyboards")
                    bot.send_message(id, "copy all informations")
                except:
                    bot.send_message(id, "ooooops")
            else:
                db().update("users", "step", message.text, "id", id)
                if message.text.lower() == "break":
                    bot.send_message(id, "Added all informations!")
                    return True
                bot.send_message(id, "Send me Content👇")
        elif get_chat_member(id):
                send_tanleng(bot, id, message.text)
                for content in db().filter("contents", "button_name", message.text):
                    print(content)
                    copy_message(id, content[1], content[2])
                    return True
                if message.text == "🔙Orqaga":
                    step = db().filter("users", "id", id)[0][3]

                    key = db().filter("keyboards", "button_name", step)[0]

                    send_tanleng(bot, id, key[0])

                    db().update("users", "step", key[0], "id", id)
                elif message.text == "🔝Bosh Sahifa":
                    send_tanleng(bot, id, "/start")

                else:
                    db().update("users", "step", message.text, "id", id)
        else:
            bot.send_message(id, config.start_text.format(name, bot.get_me().username, config.member_text),
                             reply_markup=keyboards.member(), parse_mode="html")
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
        elif step.lower() != "break" and id in config.admins:
            db().add("contents", step, message_id, id)
            bot.send_message(id, f"Add Information({message_id})")
    except:
        print("xato")
print("Starting...")
bot.polling()