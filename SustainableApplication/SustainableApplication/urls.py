"""
URL configuration for SustainableApplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from tasks import views

urlpatterns = [
    path('', include('TermsAndConditions.urls')),
    path('', include('PrivacyPolicy.urls')),
    path('', include('Checkin.urls')),
    path("", RedirectView.as_view(url="/accounts/login/", permanent=False)),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("home/", include("home.urls")),
    path("leaderboard/", include("leaderboard.urls")),
    path("tasks/", include("tasks.urls")),
    path('upload/', views.upload_file, name='upload_file'),
    path('gallery/', views.image_gallery, name='image_gallery'),
    path("collectables/", include("collectables.urls")),
    path("lootboxes/", include("lootboxes.urls")),
]

# Serve static and media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Adds access to media directory through URLs
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
