import requests

from core.telegram_api import invoke_telegram
from ping_bot.celery import app
from core.models import SiteChat, Site


@app.task
def start_ping_site(site_url):
    resp = requests.get(site_url)
    status_code = resp.status_code
    if status_code != 200:
        try:
            site = Site.objects.get(site_url=site_url)
        except:
            return 'error site in database'

        site_chat_objs = SiteChat.objects.filter(site_id=site)
        for site_chat in site_chat_objs:
            invoke_telegram('sendMessage', text=f'Error code {status_code} for site {site_url}', chat_id=site_chat.chat_id_id)
    return f'{site_url} - {status_code}'






