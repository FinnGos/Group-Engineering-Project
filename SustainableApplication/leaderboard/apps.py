"""Allows django to load the leaderboard app"""

from django.apps import AppConfig


class LeaderboardConfig(AppConfig):
    """Configuration for leaderboard"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leaderboard'
