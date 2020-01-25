from django.db import models

# Create your models here.
class CustomLogin(models.Model):
    post = models.CharField(max_length=100)
    post2 = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
