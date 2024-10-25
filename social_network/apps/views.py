from django.shortcuts import render , redirect 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import Profile
import random
from django.contrib.auth import authenticate, login, logout
import http.client
from django.views import View
from django.conf import settings
import requests
import http.client
import json
import logging
from django.conf import settings
import smtplib
from email.message import EmailMessage
import ssl
import string
from django.contrib.auth.forms import AuthenticationForm 
from django.http import HttpResponse 
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from .models import Profile
from kavenegar import KavenegarAPI
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, LoginSerializer, OTPSerializer, ResetPasswordSerializer
from django.contrib.auth import authenticate, login
import re

class HomeView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Home Page!"})

class RegisterAPIView(APIView):
    
    @staticmethod
    def is_valid_phone_number(phone):
        return re.match(r'^\d+$', phone) is not None

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            mobile = request.data.get('mobile')


            # Check for existing user by email and profile by mobile
            if User.objects.filter(email=email).exists():
                return Response({'message': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            elif Profile.objects.filter(phone_number=mobile).exists():
                return Response({'message': 'User with this mobile number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            elif not self.is_valid_phone_number(mobile):
                return Response({'error': 'Invalid phone number. Only digits are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

            # Create a new user
            user = serializer.save()

            # Create a profile for the user
            profile = Profile(user=user, phone_number=mobile)
            profile.save()

            # Send OTP 
            send_otp(request)

            # Login the user
            login(request, user)

            # Return success response
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAttempt(APIView):
    def post(self, request):
        print("Received data:", request.data)  # چاپ داده‌های دریافتی
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = authenticate(username=username, password=serializer.validated_data['password'])
            if user is not None:
                login(request, user)
                return Response({"message": "Login successful", "username": username}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Invalid form data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_otp(request,APIView):
    mobile = request.data.get('mobile')
    
    if not mobile:
        return Response({"error": "Mobile number is required."}, status=status.HTTP_400_BAD_REQUEST)

    otp = random.randint(1000, 9999)
    api = KavenegarAPI(os.getenv('KAVENEGAR_API_KEY'))  # Use environment variable for API key
    params = {
        'sender': 'YourSender',  # Use a verified sender
        'receptor': mobile,
        'message': f'Your OTP is: {otp}'
    }

    # Save the OTP in the profile
    profile = Profile.objects.filter(mobile=mobile).first()
    if profile:
        profile.otp = otp
        profile.save()

    try:
        response = api.sms_send(params)
        print(response)  # Consider using logging instead
        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error: {e}")
        return Response({"error": "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"message": "Logged out successfully."}, status=200)


@api_view(['POST'])
def otp(request):
    mobile = request.session.get('mobile')
    
    if not mobile:
        return Response({'message': 'Mobile number not found in session.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            profile = Profile.objects.filter(mobile=mobile).first()
            
            if profile and otp == str(profile.otp):
                return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Wrong OTP'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        profile = Profile.objects.filter(email=email).first()
        
        if profile:
            send_email(email)  # Pass the email to send_email function
            return Response({'message': 'Reset password sent to your email.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
