from django.shortcuts import render , redirect 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import Profile
import random
from django.contrib.auth import authenticate, login, logout
import http.client
from django.views import View
from django.conf import settings
from django.contrib.auth import authenticate, login
import requests
import http.client
import json
import logging
from django.conf import settings
from kavenegar import *
import smtplib
from email.message import EmailMessage
import ssl
import string
import os
from django.contrib.auth.forms import AuthenticationForm 
from django.http import HttpResponse 
def send_otp(request, mobile):
    otp = random.randint(1000, 9999)
    api = KavenegarAPI(os.getenv('KAVENEGAR_API_KEY'))  # Use environment variable for API key
    params = {
        'sender': 'YourSender',  # Use a verified sender
        'receptor': mobile,
        'message': f'Your OTP is: {otp}'
    }
    
    # Save the OTP in the profile or session
    profile = Profile.objects.filter(mobile=mobile).first()
    if profile:
        profile.otp = otp
        profile.save()
    
    try:
        response = api.sms_send(params)
        print(response)  # Consider using logging instead
    except Exception as e:
        print(f"Error: {e}")

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class CustomLogoutView(View):
    def get(self, request):
        logout(request)

def otp(request):
    mobile = request.session.get('mobile')
    context = {'mobile': mobile}
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        
        if profile and otp == str(profile.otp):
            return redirect('cart')
        else:
            context['message'] = 'Wrong OTP'
            context['class'] = 'danger'
    
    return render(request, 'otp.html', context)

def login_attempt(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if  form.is_valid():
            user_name=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=user_name,password=password)
            if user  is not None :
                user.save()
                login(request,user)
                messages.info(request, f"You are now logged in as {user_name}.")
                return redirect('apps:main_view')
            else:
                context = {'message': 'User does not exists', 'class': 'danger'}
                return render(request, 'login.html', context)

        else:
           context = {'message': 'User does not exists', 'class': 'danger'}
           return render(request, 'login.html', context)
    form=AuthenticationForm()
    return render(request,'login.html',{'form':form})
        
       

    

   
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        # Check for existing user by email and profile by mobile
        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(mobile=mobile).first()

        if check_user:
            messages.error(request, 'User with this email already exists.')
            return render(request, 'register.html')

        if check_profile:
            messages.error(request, 'User with this mobile number already exists.')
            return render(request, 'register.html')

        # Create a new user
        user = User(email=email, first_name=name, username=name)
        user.set_password(password)
        user.save()

        # Create a profile for the user
        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()

        # Send OTP (ensure send_otp function is defined)
        send_otp(request, mobile)

        # Store mobile in session
        request.session['mobile'] = mobile

        # Log in the user
        login(request, user)  

        # Redirect to the cart or another page
        return redirect('cart')  

    return render(request, 'register.html')

def send_email():
    length = random.randint(8, 20)
    characters = string.ascii_letters 
    password = ''.join(random.choice(characters) for i in range(length))
    email_sender = 'email'
    email_password='password'
    email_reciver='email'
    subject="your subject"
    body= f"Your password:{password}"
    em = EmailMessage()
    em['From']=email_sender
    em['To']=email_reciver
    em['subject']=subject
    em.set_content(body)

    context= ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:

        smtp.login(email_sender,'pndb djbe htox ppwp')
        smtp.sendmail(email_sender,email_reciver,em.as_string())

    
    
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        profile = Profile.objects.filter(email=email).first()
        send_email()
        if profile:  # Check if the profile exists
            return render(request, 'login.html', {'message': 'Reset password sent to your email.', 'class': 'success'})
        else:
           return render(request, 'login.html', {'message': 'Reset password sent to your email.', 'class': 'success'}) 
           
    return render(request, 'reset_password.html')


