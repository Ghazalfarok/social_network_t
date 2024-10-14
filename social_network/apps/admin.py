from django.contrib import admin
from .models import User
# Register your models here.

class ShowUser(admin.ModelAdmin):
    list_display = ['username' , 'phone']

admin.site.register(User ,ShowUser )