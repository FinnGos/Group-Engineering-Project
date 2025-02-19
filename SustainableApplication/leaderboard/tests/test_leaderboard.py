from django.test import TestCase
from home.models import CustomUser

class LeaderboardTest(TestCase):
    def setUp(self):
        # Use 'username' instead of 'name' since 'name' does not exist
        CustomUser.objects.create(username="Alice", all_time_points=100)
        CustomUser.objects.create(username="Bob", all_time_points=200)
        CustomUser.objects.create(username="Charlie", all_time_points=100)
        CustomUser.objects.create(username="David", all_time_points=300)
        CustomUser.objects.create(username="Eve", all_time_points=200)

    def test_leaderboard_order(self):
        response = self.client.get('/leaderboard/') 
        self.assertEqual(response.status_code, 200)

        ranked_users = response.context['ranked_users']

        # Expected order based on all_time_points (descending), then username (ascending)
        expected_order = [
            ('David', 300),
            ('Bob', 200),
            ('Eve', 200),
            ('Alice', 100),
            ('Charlie', 100),
        ]

        for i, entry in enumerate(ranked_users):
            self.assertEqual(entry['user'].username, expected_order[i][0])
            self.assertEqual(entry['user'].all_time_points, expected_order[i][1])

    def test_same_rank_for_same_points(self):
        response = self.client.get('/leaderboard/')
        ranked_users = response.context['ranked_users']

        # Extract ranks based on username
        ranks = {entry['user'].username: entry['rank'] for entry in ranked_users}

        # Users with the same points should have the same rank
        self.assertEqual(ranks["Alice"], ranks["Charlie"])  
        self.assertEqual(ranks["Bob"], ranks["Eve"])        
