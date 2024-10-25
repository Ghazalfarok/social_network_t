from rest_framework import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'username', 'password']
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return attrs
class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

