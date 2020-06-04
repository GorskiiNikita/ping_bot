from django.contrib import admin

from .models import Chat, Site, SiteChat


admin.site.register(Chat)
admin.site.register(Site)
admin.site.register(SiteChat)
