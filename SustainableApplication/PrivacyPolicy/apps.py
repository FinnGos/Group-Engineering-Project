"""Allows django to load the Privacy Policy app"""

from django.apps import AppConfig


class PrivacypolicyConfig(AppConfig):
    """Configuration for Privacy Policy"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PrivacyPolicy'
