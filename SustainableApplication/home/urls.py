"""Defines URL patterns for home."""
from django.http import HttpResponse
from django.urls import path
from tasks import views as tviews
from .views import CustomLogoutView, LoginFormView
from . import views

# Placeholder views
def placeholder_view(request):
    """Placeholder view for pages that are not yet implemented."""
    return HttpResponse("This page is under construction.", content_type="text/plain")

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("accounts/login/", LoginFormView.as_view(), name="login"),
    path("tasks/",tviews.tasks_view, name="task"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="logout"),
    path("accounts/delete_account/", views.delete_account, name="delete_account"),
    path("accounts/update_profile/", views.update_profile, name="update_profile"),
    path("accounts/change_password/", views.change_password, name="change_password"),
    path("accounts/view_data/", views.view_user_data, name="view_user_data"),
]
