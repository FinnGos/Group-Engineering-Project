"""Tests for leaderboard"""
from django.test import TestCase
from home.models import CustomUser
from django.urls import reverse

class LeaderboardTest(TestCase):
    """Test case for leaderboard"""
    def setUp(self):
        """Create test users with different point values."""
        self.user1 = CustomUser.objects.create_user(username='player1', password='pass', all_time_points=100)
        self.user2 = CustomUser.objects.create_user(username='player2', password='pass', all_time_points=200)
        self.user3 = CustomUser.objects.create_user(username='player3', password='pass', all_time_points=150)
        self.user4 = CustomUser.objects.create_user(username='player4', password='pass', all_time_points=50)
        self.user5 = CustomUser.objects.create_user(username='player5', password='pass', all_time_points=300)
        self.user6 = CustomUser.objects.create_user(username='player6', password='pass', all_time_points=250)
        self.admin = CustomUser.objects.create_superuser(username='admin', password='adminpass')
        self.client.login(username='player1', password='pass')

    def get_leaderboard(self):
        """helper function to get leaderboard"""
        response = self.client.get(reverse('leaderboard'))
        return response.context['ranked_users']

    def test_three_players_on_leaderboard(self):
        """Test that when there are three players, the leaderboard has three players in the correct order"""
        CustomUser.objects.exclude(username__in=["player1", "player2", "player3"]).delete()
        leaderboard = self.get_leaderboard()
        self.assertEqual(len(leaderboard), 3)

    def test_five_players_on_leaderboard(self):
        """Test that when there are five players, the leaderboard has five players in the correct order"""
        CustomUser.objects.exclude(username__in=["player1", "player2", "player3", "player4", "player5"]).delete()
        leaderboard = self.get_leaderboard()
        self.assertEqual(len(leaderboard), 5)

    def test_seven_players_show_top_five(self):
        """Test that when there are seven players, the leaderboard shows the top five players in the correct order"""
        leaderboard = self.get_leaderboard()
        self.assertEqual(len(leaderboard), 5)

    def test_players_ordered_by_points(self):
        """Test that when there are players, they are ordered by points in descending order"""
        expected_order = ["player5","player6","player2","player3","player1"]
        leaderboard = self.get_leaderboard()
        actual_order = [entry['user'].username for entry in leaderboard]
        self.assertEqual(expected_order, actual_order)

    


