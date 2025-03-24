"""Allows django to load the home app"""

from django.apps import AppConfig


class HomeConfig(AppConfig):
    """Configuration for home"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
