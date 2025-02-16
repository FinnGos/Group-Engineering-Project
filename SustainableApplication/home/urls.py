from django.urls import path
from . import views
from .views import CustomLogoutView, LoginFormView

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("accounts/login/", LoginFormView.as_view(), name="login"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="logout"),  # Logout
]
