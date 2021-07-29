import requests
import config
import json
def get_chat_member(id):
    for channel in config.KanalvaGuruhlar:
        re = requests.get('http://api.telegram.org/bot' + str(config.Token) + '/getChatMember?chat_id=@' + channel[1] + '&user_id=' + str(id))
        re = json.loads(re.text)
        if re["result"]["status"] == 'left':
            return False
    return True
def copy_message(chat_id, message_id, from_chat_id):
    re = requests.get(f"https://api.telegram.org/bot{config.Token}/copyMessage?chat_id={chat_id}&message_id={message_id}&from_chat_id={from_chat_id}")
    re = json.loads(re.text)["result"]["message_id"]
    return re


