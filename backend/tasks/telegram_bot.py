import requests
import environ


env = environ.Env()
environ.Env.read_env()


def send_update_to_bot(bot_chatID, bot_message):

    bot_token = env('TELEGRAM_TOKEN')
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
