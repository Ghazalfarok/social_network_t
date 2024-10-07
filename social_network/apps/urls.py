from django.urls import path
from .views import * 
urlpatterns = [
    path('' , show_init_page , name='Home page'),
]
