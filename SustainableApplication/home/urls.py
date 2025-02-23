from django.urls import path
from . import views
from .views import CustomLogoutView, LoginFormView

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("accounts/login/", LoginFormView.as_view(), name="login"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="logout"),
    path("accounts/delete_account/", views.delete_account, name="delete_account"),  # Logout
    path("accounts/update_profile/", views.update_profile, name="update_profile"),
    path("accounts/change_password/", views.change_password, name="change_password"),
]
