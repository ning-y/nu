import os, xdg
from urllib import parse, request

def get_last_token():
    fp = os.path.join(xdg.XDG_CACHE_HOME, "nu", "bot-token")
    with open(fp, "r") as txtfile:
        return txtfile.readline().strip()

def get_last_chat_id():
    fp = os.path.join(xdg.XDG_CACHE_HOME, "nu", "chat-id")
    with open(fp, "r") as txtfile:
        return int(txtfile.readline().strip())

def send_message(token, chat_id, message, should_save):
    # I could not get application/json to work.
    req = request.Request(
        os.path.join(
            f"https://api.telegram.org/bot{token}/",
            f"sendMessage?chat_id={chat_id}&text={parse.quote_plus(message)}"))
    if should_save: _save(token, chat_id)
    return request.urlopen(req, data).read()

def _save(token, chat_id):
    os.makedirs(os.path.join(xdg.XDG_CACHE_HOME, "nu"), exist_ok=True)
