""" Views for the home app. """
# Standard library imports
import logging
import os
import re
from datetime import datetime, timedelta

# Related third-party imports
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm, UserChangeForm
)
from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.contrib.auth.views import LoginView, LogoutView
from django.dispatch import receiver
from django.shortcuts import render, redirect

# Local application/library specific imports
from .forms import CustomUserCreationForm
from .models import CustomUser

# Set up a logger for authentication events
auth_logger = logging.getLogger("django")


# Define the path to the log file
LOG_FILE_PATH = os.path.join(settings.BASE_DIR, "django_logs.log")


@login_required
def home(request):
    """
    View function for the home page of the site.
    
    This function ensures that only authenticated users can access the home page.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: Renders the home.html template.
    """
    return render(request, "home.html")


def signup(request):
    """
    Handles user signup and logs signup events.
    
    This function processes user registration using a custom signup form.
    It logs both successful and failed signup attempts.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: Renders the signup form template.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            auth_logger.info("New user signed up: %s", user.username)
            return redirect("home")
        auth_logger.warning("Failed signup attempt.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})

@receiver(user_logged_out)
def log_successful_logout(sender, request, user, **kwargs):
    """
    Logs successful logout attempts.

    Args:
        sender: The sender of the signal.
        request (HttpRequest): The HTTP request object.
        user (User): The user logging out.
        kwargs: Additional arguments.
    """
    try:
        if user.is_authenticated:
            auth_logger.info("User logged out: %s", user.username)
    except AttributeError:
        auth_logger.info("Logout by an unauthenticated user or session end.")

@receiver(user_logged_in)
def log_successful_login(sender, request, user, **kwargs):
    """
    Logs successful login attempts and triggers log cleanup.

    Args:
        sender: The sender of the signal.
        request (HttpRequest): The HTTP request object.
        user (User): The user logging in.
        kwargs: Additional arguments.
    """
    auth_logger.info("User logged in: %s", user.username)
    #

@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    """
    Logs failed login attempts.

    Args:
        sender: The sender of the signal.
        credentials (dict): A dictionary containing login credentials.
        request (HttpRequest): The HTTP request object.
        kwargs: Additional arguments.
    """
    attempted_username = credentials.get("username", "UNKNOWN")
    auth_logger.info("Failed login attempt for username: %s", attempted_username)

class LoginFormView(LoginView):
    """
    Custom login view to log login attempts.
    
    Inherits from Django's built-in LoginView.
    """
    template_name = "registration/login.html"

class CustomLogoutView(LogoutView):
    """
    Custom logout view that logs when a user logs out.
    
    Inherits from Django's built-in LogoutView.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Logs logout events if the user is authenticated.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        
        Returns:
            HttpResponseRedirect: Redirects to the login page after logout.
        """
        if request.user.is_authenticated:
            auth_logger.info("User logged out: %s", request.user.username)
        return redirect("login")

def delete_account(request):
    """
    Deletes the logged-in user's account and logs the event.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponseRedirect: Redirects to the login page after deletion.
    """
    user = request.user
    auth_logger.info("User deleted account: %s", user.username)
    user.delete()
    return redirect("login")

class CustomUserUpdateForm(forms.ModelForm):
    """
    Custom form to allow users to update their username and email.
    """
    class Meta:
        """" Meta class for the CustomUserUpdateForm. """
        model = CustomUser
        fields = ["username", "email"]

def update_profile(request):
    """
    View to update username and email.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: Renders the profile update form template.
    """
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            auth_logger.info("User updated profile (username & email): %s", request.user.username)
            messages.success(request, "Profile updated successfully!")
            return redirect("home")
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, "registration/update_profile.html", {"form": form})

def change_password(request):
    """
    View to change user password.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: Renders the password change form template.
    """
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            auth_logger.info("User changed password: %s", request.user.username)
            messages.success(request, "Your password was successfully updated!")
            return redirect("home")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "registration/change_password.html", {"form": form})




def view_user_data(request):
    """
    View that displays all stored information about the logged-in user.
    
    This includes their username, email, password (hashed), 
    and a list of logs associated with their username.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the user data template with user details and logs.
    """
    # Adding logs
    auth_logger.info("User asked for personal data stored: %s", request.user.username)

    user = request.user

    # Read logs related to the exact username using regex
    user_logs = []
    username_pattern = re.compile(rf"\b{re.escape(user.username)}\b")  # Exact match

    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as file:
            for line in file:
                if username_pattern.search(line):  # Match exact username
                    user_logs.append(line.strip())

    context = {
        "user": user,
        "user_logs": user_logs,
        "hashed_password": user.password  # Django stores hashed passwords
    }
    
    return render(request, "registration/view_user_data.html", context)
