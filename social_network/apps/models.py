from django.db import models
from django.conf import settings
class city(models.Model):
    name = models.CharField(max_length=100)
class country(models.Model):
    name = models.CharField(max_length=100)    
class state(models.Model):
    name = models.CharField(max_length=100)    
class Profile(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()
    phone_number = models.BigIntegerField(blank=True, null=True, unique=True)
    avatar = models.ImageField(blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)  
   
    country = models.ForeignKey(to='country', blank=True, null=True, on_delete=models.CASCADE, related_name='+')
    state = models.ForeignKey(to='state', blank=True, null=True, on_delete=models.CASCADE, related_name='+')
    city = models.ForeignKey(to='City', blank=True, null=True, on_delete=models.CASCADE, related_name='+')
