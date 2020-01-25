from django.db import models
from django import forms

# Create your models here.
class CustomLogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
