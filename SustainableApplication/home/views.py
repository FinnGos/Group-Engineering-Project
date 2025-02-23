import logging  # Import Python's logging module for logging authentication events
from django.shortcuts import render, redirect  # Import functions to render templates and redirect users
from .models import Locations, Collectable, CustomUser  # Import custom models for the application
from django.contrib.auth import login, logout  # Import authentication functions for login and logout
from django.contrib.auth.forms import UserCreationForm  # Import default user creation form
from django.contrib.auth.views import LoginView, LogoutView  # Import Django’s built-in login and logout views
from django.contrib.auth.decorators import login_required  # Import decorator to restrict views to logged-in users
from .forms import CustomUserCreationForm  # Import custom user signup form
from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out  # Import authentication signals
from django.dispatch import receiver  # Import receiver to connect functions to signals
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django import forms

# Set up a logger for authentication events
auth_logger = logging.getLogger("django")

@login_required  # Ensures that only authenticated users can access this view
def home(request):
    """View function for the home page of the site."""
    return render(request, "home.html", {})  # Render the home.html template

def signup(request):
    """Handles user signup and logs signup events."""
    if request.method == "POST":  # Check if the request is a form submission
        form = CustomUserCreationForm(request.POST)  # Initialize form with submitted data
        if form.is_valid():  # Validate the form
            user = form.save(commit=False)  # Create user instance but don’t save it yet
            user.set_password(form.cleaned_data["password1"])  # Hash the password
            user.save()  # Save the user instance
            login(request, user)  # Log in the new user
            auth_logger.info(f"New user signed up: {user.username}")  # Log the signup event
            return redirect("home")  # Redirect user to the home page after signup
        else:
            auth_logger.warning("Failed signup attempt.")  # Log failed signup attempts

    else:
        form = CustomUserCreationForm()  # If not a POST request, render an empty form
    
    return render(request, "registration/signup.html", {"form": form})  # Render signup template with form

@receiver(user_logged_out)
def log_successful_logout(sender, request, user, **kwargs):
    """Logs successful logout attempts."""
    try:
        if user.is_authenticated:
            auth_logger.info(f"User logged out: {user.username}")  # Log the authenticated user's username
    except:
        auth_logger.info("Logout by an unauthenticated user or session end.")

# Signal handler to log successful logins
@receiver(user_logged_in)
def log_successful_login(sender, request, user, **kwargs):
    """Logs successful login attempts."""
    auth_logger.info(f"User logged in: {user.username}")  # Log the authenticated user's username

# Signal handler to log failed login attempts
@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    """Logs failed login attempts."""
    attempted_username = credentials.get("username", "UNKNOWN")  # Get the attempted username from credentials
    auth_logger.info(f"Failed login attempt for username: {attempted_username}")  # Log failed login attempt

class LoginFormView(LoginView):
    """Custom login view to log login attempts."""
    template_name = "registration/login.html"  # Specify template for login page

class CustomLogoutView(LogoutView):
    """Logs when a user logs out."""
    
    def dispatch(self, request, *args, **kwargs):
        """Logs logout event if the user is authenticated."""
        if request.user.is_authenticated:  # Check if user is logged in before logging the event
            auth_logger.info(f"User logged out: {request.user.username}")  # Log the logout event
        return redirect("login")  # Continue with default logout behavior

def delete_account(request):
    """View to delete the logged-in user's account."""
    user = request.user
    auth_logger.info(f"User deleted account: {user.username}")
    user.delete()
    return redirect("login")  

# Custom form to allow username and email updates
class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]

def update_profile(request):
    """View to update username and email."""
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            auth_logger.info(f"User updated profile (username & email): {request.user.username}")
            messages.success(request, "Profile updated successfully!")
            return redirect("home")
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, "registration/update_profile.html", {"form": form})


def change_password(request):
    """View to change user password."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            auth_logger.info(f"User changed password: {request.user.username}")
            messages.success(request, "Your password was successfully updated!")
            return redirect("home")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "registration/change_password.html", {"form": form})