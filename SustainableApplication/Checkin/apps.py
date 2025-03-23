"""Allows django to load the Checkin app"""

from django.apps import AppConfig


class CheckinConfig(AppConfig):
    """Configuration for Checkin"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Checkin'
