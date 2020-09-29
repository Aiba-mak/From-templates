
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from rest_framework import serializers
from users.models import *


class UserRegisterSerializer(serializers.ModelSerializer):
	email = serializers.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class UserUpdateSerializer(serializers.ModelSerializer):
	email = serializers.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']

class ProfileUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['bio', 'image']
