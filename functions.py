import requests
import config
import json
import keyboards
from database import db
def get_chat_member(id):
    for channel in db().filter("channels", "","",all=True):
        re = requests.get('http://api.telegram.org/bot' + str(config.Token) + '/getChatMember?chat_id=@' + channel[1] + '&user_id=' + str(id))
        re = json.loads(re.text)
        if re["result"]["status"] == 'left':
            return False
    return True
def copy_message(chat_id, message_id, from_chat_id):
    requests.get(f"https://api.telegram.org/bot{config.Token}/copyMessage?chat_id={chat_id}&message_id={message_id}&from_chat_id={from_chat_id}")
def send_tanleng(bot, id,text):
    keys = []
    for button in db().filter("keyboards", "markup_name", text):
        keys.append(button[1])
    if keys:
        bot.send_message(id, "Tanlang!", reply_markup=keyboards.markup(keys, text))

