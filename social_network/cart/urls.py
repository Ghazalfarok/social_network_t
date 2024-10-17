
from .views import *
from django.urls import path,include
from accounts import views

urlpatterns = [
    path('login/', views.login_attempt, name='login'),
    path('cart' , cart , name="cart"),
        
]