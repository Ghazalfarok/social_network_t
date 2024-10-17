from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()
    phone_number = models.BigIntegerField(blank=True, null=True, unique=True)
    country = models.ForeignKey(to=Country, blank=True, null=True, on_delete=models.CASCADE, related_name='+')
    state = models.ForeignKey(to=State, blank=True, null=True, on_delete=models.CASCADE, related_name='+')
    city = models.ForeignKey(to=City, blank=True, null=True, on_delete=models.CASCADE, related_name='+')
    avatar = models.ImageField(blank=True, null=True)