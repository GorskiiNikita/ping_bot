from django.db import models


class Chat(models.Model):
    chat_id = models.IntegerField(primary_key=True)


class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    site_url = models.TextField()


class SiteChat(models.Model):
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)











