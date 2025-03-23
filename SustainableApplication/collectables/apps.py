"""Allows django to load the collectable app"""

from django.apps import AppConfig


class CollectablesConfig(AppConfig):
    """Configuration for collectables"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectables'
