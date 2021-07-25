import requests as pythonRequests


def send_update_to_bot(bot_message):

    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = pythonRequests.get(send_text)

    return response.json()


test = send_update_to_bot("Testing Telegram bot")
print(test)
