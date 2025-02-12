from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """UserCreationForm is for django's built in auth.User model but we have our own CustomUser model therefore
    default form will result in an error. Using CustomUserCreationForm allows us to include extra fields and
    allows form validation to work with our model"""

    # defines metadata for the form. Specifying which models and fields should be used
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
