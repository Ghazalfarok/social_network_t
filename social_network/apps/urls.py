from .views import *
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginAttempt.as_view(), name='api-login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('otp/', otp, name="otp"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('otp/', otp, name='otp_api'),
    path('reset-password/', reset_password, name='reset_password_api'),
]
