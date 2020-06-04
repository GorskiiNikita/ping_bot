import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Chat, Site, SiteChat
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .telegram_api import invoke_telegram


@csrf_exempt
def telegram_hook(request):
    update = json.loads(request.body)
    message = update.get('message')

    if message is None:
        return HttpResponse('OK')

    text_message = message['text']
    chat_id = message['chat']['id']

    chat, created = Chat.objects.get_or_create(chat_id=chat_id)

    if '/add_site' in text_message:
        if len(text_message.split()) != 2:
            return HttpResponse('OK')

        site_url = text_message.split()[1]
        site, created_site = Site.objects.get_or_create(site_url=site_url)
        site_chat, created_sitechat = SiteChat.objects.get_or_create(site_id=site, chat_id=chat)

        if created_site:
            schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
            PeriodicTask.objects.create(interval=schedule,
                                        task='core.tasks.start_ping_site',
                                        name=f'id{site.site_id}',
                                        args=json.dumps([site_url]))

    elif '/delete_site' in text_message:
        if len(text_message.split()) != 2:
            return HttpResponse('OK')

        site_url = text_message.split()[1]
        try:
            site = Site.objects.get(site_url=site_url)
            SiteChat.objects.filter(chat_id=chat, site_id=site).delete()
            site_chat_count = SiteChat.objects.filter(site_id=site).count()
            if site_chat_count == 0:
                PeriodicTask.objects.filter(name=f'id{site.site_id}').delete()
                site.delete()
        except:
            pass

    elif '/show_monitoring_list' in text_message:
        site_chat_objs = SiteChat.objects.filter(chat_id=chat)
        site_urls = [site_chat.site_id.site_url for site_chat in site_chat_objs]

        invoke_telegram('sendMessage', chat_id=chat_id, text='\n'.join(site_urls))

    return HttpResponse('OK')
