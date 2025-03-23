"""Allows django to load the unlockable map app"""

from django.apps import AppConfig


class UnlockablesConfig(AppConfig):
    """Configuration for unlockable map"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'unlockables'
