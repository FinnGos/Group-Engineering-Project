from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """necessary to create custom user form as we are using a custom user model"""
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
