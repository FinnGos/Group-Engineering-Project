"""Allows django to load the daily tasks app"""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Configuration for daily tasks"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
