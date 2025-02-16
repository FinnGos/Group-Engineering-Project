import logging
from django.shortcuts import render, redirect
from .models import Locations, Collectable, CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Set up a logger for authentication
auth_logger = logging.getLogger("django_auth")

@login_required
def home(request):
    """View function for home page of site."""
    return render(request, "home.html", {})

def signup(request):
    """Handles user signup and logs signup events."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # Hash password
            user.save()
            login(request, user)
            auth_logger.info(f"New user signed up: {user.username}")  # Log user signup
            return redirect("home")
        else:
            auth_logger.warning("Failed signup attempt.")  # Log failed signups

    else:
        form = CustomUserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})

class LoginFormView(LoginView):
    """Custom login view to log login attempts."""
    template_name = "registration/login.html"
    auth_logger.info("Test to see if here")  # Log successful login

    def form_valid(self, form):
        print("herereere")
        """Log successful logins before redirecting."""
        user = form.get_user()  # Get authenticated user
        auth_logger.info(f"User logged in: {user.username}")  # Log successful login
        return super().form_valid(form)

    def form_invalid(self, form):
        """Log failed login attempts."""
        attempted_username = self.request.POST.get("username", "UNKNOWN")
        auth_logger.info(f"Failed login attempt for username: {attempted_username}")
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    """Logs when a user logs out."""
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logger.info(f"User logged out: {request.user.username}")
        return super().dispatch(request, *args, **kwargs)
