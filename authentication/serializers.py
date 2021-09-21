from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=7, write_only=True)
    
    class Meta:
        model=User
        fields = ['username', 'password']
        
    def validate(self, attrs):
        username = attrs.get('username', '')
        
        if not username.isalnum():
            raise serializers.ValidationError('The username should only alphabet')
        try:
            User.objects.get(username=username)
            raise serializers.ValidationError('The username already exist')
        except:
            pass

        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        

class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=255, min_length=5, write_only=True)
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens=serializers.SerializerMethodField()
    
    def get_tokens(self, obj):
        user=User.objects.get(username=obj['username'])
        tokens = user.tokens()
        return{
            'access':tokens['access'],
            'refresh':tokens['refresh']
        }
    
    class Meta:
        model=User
        fields=['username', 'password', 'tokens']
    
    def validate(self, attrs):
        username=attrs.get('username', '')
        password=attrs.get('password', '')
        user=auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled")
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()

    error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise NotFound("Already logout or doesn't exist")
        

class SetNewPasswordSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=255, min_length=5, write_only=True)
    new_password_1=serializers.CharField(min_length=6, max_length=68, write_only=True)
    new_password_2=serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = ['username', 'new_password_1', 'new_password_2']
        
    def validate(self, attrs):
        username=attrs.get('username', '')
        new_password_1=attrs.get('new_password_1', '')
        new_password_2=attrs.get('new_password_2', '')
        
        if new_password_1 != new_password_2:
            raise ValidationError('diffrent password error')

        try:
            user=User.objects.get(username=username)
            user.set_password(new_password_2)
            user.save()
            
            return super().validate(attrs)
        except:
            AuthenticationFailed("Invalid credentials, try again")
