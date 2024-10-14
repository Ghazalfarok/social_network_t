from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=51)
    password = models.CharField(max_length=51)
    phone = models.CharField(max_length=11)


    def __str__(self):
        return f"{self.username}"