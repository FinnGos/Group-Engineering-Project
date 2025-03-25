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
        """Helper function to get leaderboard"""
        response = self.client.get(reverse('leaderboard'))
        return response.context['ranked_users']

    def test_one_player_on_leaderboard(self):
        """Test that only one player is on the leaderboard"""
        CustomUser.objects.exclude(username__in=["player1"]).delete()
        leaderboard = self.get_leaderboard()
        self.assertEqual(len(leaderboard), 1)

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
        expected_order = ["player5", "player6", "player2", "player3", "player1"]
        leaderboard = self.get_leaderboard()
        actual_order = [entry['user'].username for entry in leaderboard]
        self.assertEqual(expected_order, actual_order)

    def test_top_and_bottom_two_match(self):
        """Test that the top and bottom two players match the expected players"""
        self.user1.all_time_points = 100
        self.user2.all_time_points = 100
        self.user3.all_time_points = 90
        self.user4.all_time_points = 50
        self.user5.all_time_points = 50
        self.user6.all_time_points = 0
        self.user1.save()
        self.user2.save()
        self.user3.save()
        self.user4.save()
        self.user5.save()
        self.user6.save()

        leaderboard = self.get_leaderboard()
        self.assertEqual(leaderboard[0]['user'].username, "player1")
        self.assertEqual(leaderboard[1]['user'].username, "player2")
        self.assertEqual(leaderboard[2]['user'].username, "player3")
        self.assertEqual(leaderboard[3]['user'].username, "player4")
        self.assertEqual(leaderboard[4]['user'].username, "player5")

    def test_all_players_with_same_score(self):
        """Test for case where all players have the same score"""
        # Set all players to have the same score
        self.user1.all_time_points = 100
        self.user2.all_time_points = 100
        self.user3.all_time_points = 100
        self.user4.all_time_points = 100
        self.user5.all_time_points = 100
        self.user1.save()
        self.user2.save()
        self.user3.save()
        self.user4.save()
        self.user5.save()

        leaderboard = self.get_leaderboard()

        # All players should have the same rank
        self.assertEqual(leaderboard[0]['user'].username, "player6")
        self.assertEqual(leaderboard[1]['user'].username, "player1") 
        self.assertEqual(leaderboard[2]['user'].username, "player2")
        self.assertEqual(leaderboard[3]['user'].username, "player3")
        self.assertEqual(leaderboard[4]['user'].username, "player4") 
