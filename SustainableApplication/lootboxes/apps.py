"""Allows django to load the lootboxes app"""

from django.apps import AppConfig


class LootboxesConfig(AppConfig):
    """Configuration for lootboxes"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lootboxes'
