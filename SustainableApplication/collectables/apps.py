"""Allows django to load the collectable app from the main page"""

from django.apps import AppConfig


class CollectablesConfig(AppConfig):
    """Configuration for collectables app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectables'
