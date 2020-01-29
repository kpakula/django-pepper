from django.db import models
from django import forms
from django.conf import settings
from bootstrap_datepicker_plus import DatePickerInput

# Create your models here.
class CustomLogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    date_published = models.DateField()
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    price = models.FloatField()
    votes = models.BigIntegerField()
    link = models.CharField(max_length=2048)
    description = models.CharField(max_length=500)
    link_to_image = models.CharField(max_length=2048)

    def __str__(self):
        return self.user.username + ': ' + self.title 

    
