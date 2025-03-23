"""Tests for Checkin"""
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Checkin.models import Location
from tasks.models import Tasks

class ViewsTestCase(TestCase):
    """Tests for Checkin"""
    databases = {"default", "location_db"}

    def setUp(self):
        """
        Sets up the tests so that it is forced logged into the system to run the tests
        """
        self.client = Client()
        User1 = get_user_model()
        self.user = User1.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)

        # Create a sample task
        self.task = Tasks.objects.create(task_name="Test Task", has_checked_in=False, reward=10)

        # Create a sample location in the location_db
        self.valid_location = Location.objects.using("location_db").create(
            name="Test Location",
            latitude=37.7749,
            longitude=-122.4194,
            radius=100  # 100 meters
        )

    def test_get_location_missing_params(self):
        """Tests initial load of the page where no location is given"""
        response = self.client.get(reverse('get_location', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin_page.html')

    def test_get_location_missing_lat(self):
        """Tests when only longitude is given"""
        response = self.client.get(reverse('get_location', args=[self.task.id]), {'lon': '-74.0060'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin_page.html')

    def test_get_location_missing_lon(self):
        """Tests when only latitude is given"""
        response = self.client.get(reverse('get_location', args=[self.task.id]), {'lat': '40.7128'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin_page.html')

    def test_get_location_invalid_values(self):
        """Tests if an invalid type is given"""
        response = self.client.get(reverse('get_location', args=[self.task.id]), {'lat': 'abc', 'lon': 'xyz'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_above_maximum_values(self):
        """Tests going over maximum"""
        response = self.client.get(reverse('get_location', args=[self.task.id]), {'lat': '90.1', 'lon': '180.1'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_below_minimum_values(self):
        """Tests going under minimum"""
        response = self.client.get(reverse('get_location', args=[self.task.id]), {'lat': '-90.1', 'lon': '-180.1'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    @patch("Checkin.views.geodesic")  # Mocking geodesic function
    def test_valid_location_checkin(self, mock_geodesic):
        """Tests if lon and lat are valid and within the location range"""
        mock_geodesic.return_value.meters = 50  # Within 100m radius
        response = self.client.get(reverse("get_location", args=[self.task.id]), {"lat": "37.7749", "lon": "-122.4194"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Check-in Succesfull at Test Location!")

