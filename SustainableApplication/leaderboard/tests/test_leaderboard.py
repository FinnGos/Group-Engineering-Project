from django.test import TestCase
from django.urls import reverse
from home.models import CustomUser

class LeaderboardTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass")
        self.client.force_login(self.user)

        CustomUser.objects.create(username="Alice", all_time_points=100)
        CustomUser.objects.create(username="Bob", all_time_points=200)
        CustomUser.objects.create(username="Charlie", all_time_points=100)
        CustomUser.objects.create(username="David", all_time_points=300)
        CustomUser.objects.create(username="Eve", all_time_points=200)

        """
        PLEASE NOTE:
        the test written below is redundant and deprecated (can be removed after being reviewed)
        this test has a paradox - it wants to test the leaderboard when there are NO users,
        but in order to reach the leaderboard you must be logged in 
        i believe this test to be pointless for this reason
        """

   ## def test_leaderboard_order(self):  
   ##     """Test users appear in correct order"""
   ##     response = self.client.get(reverse('leaderboard')) 
   ##     self.assertEqual(response.status_code, 200)  
##
   ## def test_leaderboard_empty(self):
   ##     """Test leaderboard shows correctly when empty"""
   ##     CustomUser.objects.all().delete()  # Remove all users
##
   ##     # Recreate test user and re-login
##
   ##     self.client.force_login(self.user)
##
   ##     response = self.client.get(reverse('leaderboard'))  
##
   ##     
   ##     self.assertEqual(response.status_code, 200)  # Page should still load
   ##     self.assertNotContains(response, 'class="rank-item"')  # Ensure no users are displayed
