from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import redirect
from tasks import views as tviews
from leaderboard import views as lviews
from .views import CustomLogoutView, LoginFormView
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

# Placeholder views
def placeholder_view(request):
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
    path("how-to-play/", placeholder_view, name="how_to_play"),
    path("tasks-view/", placeholder_view, name="tasks_view"),
    path("leaderboard/", lviews.leaderboard, name="leaderboard"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

