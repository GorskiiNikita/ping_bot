import requests

from ping_bot import settings


URL = 'https://api.telegram.org'

# Данные для прокси, только для Российских серверов
proxies = {'https': 'https://Selerohatoha1337:R0z9VzP@176.114.12.193:45785',
           'http': 'http://Selerohatoha1337:R0z9VzP@176.114.12.193:45785'}


# Для Российских серверов нужно добавить параметр proxies в requests.post()
def invoke_telegram(method, **kwargs):
    resp = requests.post(f'{URL}/bot{settings.TELEGRAM_BOT_TOKEN}/{method}', data=kwargs, proxies=proxies)
    return resp
