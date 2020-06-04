"""ping_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from ping_bot.settings import ENDPOINT_URL
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from core.telegram_api import invoke_telegram
from core.views import telegram_hook

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/telegram_hook/?', telegram_hook, name='telegram_hook'),
]


# Назначаем адрес для хуков телеграма
invoke_telegram('setWebhook', url=f'{ENDPOINT_URL}/api/telegram_hook/')

PeriodicTask.objects.all().delete()
IntervalSchedule.objects.all().delete()


from core.models import *
Chat.objects.all().delete()
Site.objects.all().delete()
SiteChat.objects.all().delete()
