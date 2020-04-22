from django.db import models

class WelcomeText(models.Model):
    title = models.CharField(max_length=500)
    title_ru = models.CharField(max_length=500)
    content = models.CharField(max_length=500)
    content_ru = models.CharField(max_length=500)
    def __int__(self):
        return self.title

class Services(models.Model):
    title = models.CharField(max_length=1000)
    title_ru = models.CharField(max_length=1000)
    content = models.TextField(blank=True)
    content_ru = models.TextField(blank=True)
    def __int__(self):
        return self.title

class Terms(models.Model):
    title = models.CharField(max_length=1000)
    title_ru = models.CharField(max_length=1000)
    content = models.TextField(blank=True)
    content_ru = models.TextField(blank=True)
    def __int__(self):
        return self.title

class FooterText(models.Model):
    sitename = models.CharField(max_length=200)
    middletext = models.CharField(max_length=300)
    middletext_ru = models.CharField(max_length=300)
    email = models.CharField(max_length=150)
    def __int__(self):
        return self.title
