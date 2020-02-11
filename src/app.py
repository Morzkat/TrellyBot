import requests
from flask import Flask, escape, request

app = Flask(__name__)
chat_id = 0
BOT_TOKEN = '{BOT_TOKEN}'
BOT_URL = 'https://api.telegram.org/bot{BOT_TOKEN}/'


def set_chat_id(new_chat_id):
    global chat_id
    chat_id = new_chat_id


def respond(message):
    json_data = {
        "chat_id": chat_id,
        "text": message
    }
    url = BOT_URL + 'sendMessage'
    requests.post(url, json=json_data)
    print('Message sended...')
    return


def setWebhook(webhook_url):
    request_result = requests.get(f'{BOT_URL}setWebHook?url={webhook_url}')
    print(request_result)


def default_action(args):
    respond('No action found it...')
          

def get_commits(args):
    respond(f'getting commits of {args}')
          
def get_action(action):
    return {
        'get_commits' : get_commits,
        'default_action' : default_action
    }.get(action, default_action)          


@app.route('/',  methods=['POST'])
def proccess_telegram_message():
    telegram_message = request.json['message']

    chat = telegram_message['chat']
    set_chat_id(chat['id'])

    actions_and_args = telegram_message['text'].lower().split('-', 1)

    get_action(actions_and_args[0])(actions_and_args[1])
    
    return '200'


@app.before_first_request
def main():
    print('Bot started...')
    setWebhook('https://9a7e1a78.ngrok.io')
    return "."
    

if __name__ == "__app__":
    app.run()
