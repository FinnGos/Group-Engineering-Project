"""Allows django to load the terms and conditions app"""

from django.apps import AppConfig


class TermsandconditionsConfig(AppConfig):
    """Configuration for terms and conditions"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TermsAndConditions'
