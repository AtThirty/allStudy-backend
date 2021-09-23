from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    
    def create_user(self, username, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if password is None:
            raise TypeError('Users should have a password')

        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if password is None:
            raise TypeError('Users should have a password')
        
        user = self.create_user(username, password)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user

def get_profile_image_filepath(self):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image():
    return "todoAPI/sdi.png"

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)

    USERNAME_FIELD = 'username'

    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]