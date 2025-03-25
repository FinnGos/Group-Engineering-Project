"""Tests for leaderboard"""
from django.test import TestCase
from home.models import CustomUser

class LeaderboardTest(TestCase):
   """Test case for leaderboard"""
   def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass")
        self.client.force_login(self.user)

        CustomUser.objects.create(username="Alice", all_time_points=100)
        CustomUser.objects.create(username="Bob", all_time_points=200)
        CustomUser.objects.create(username="Charlie", all_time_points=100)
        CustomUser.objects.create(username="David", all_time_points=300)
        CustomUser.objects.create(username="Eve", all_time_points=200)
        
   def test_leaderboard_order(self):
    """Test users appear in correct order on the leaderboard"""
    response = self.client.get('/leaderboard/')  
    self.assertEqual(response.status_code, 200)  # Ensure the page loads correctly

    ranked_users = CustomUser.objects.exclude(username=self.user.username).order_by('-all_time_points')
    self.assertGreater(len(ranked_users), 0, "Leaderboard should not be empty")

    expected_order = [
        ('David', 300),
        ('Bob', 200),
        ('Eve', 200),
        ('Alice', 100),
        ('Charlie', 100),
    ]

    self.assertEqual(len(ranked_users), len(expected_order), "Mismatch in expected and actual leaderboard length")

    # Check if the leaderboard order matches expectations
    for i, entry in enumerate(ranked_users):
        self.assertEqual(entry.username, expected_order[i][0])
        self.assertEqual(entry.all_time_points, expected_order[i][1])


