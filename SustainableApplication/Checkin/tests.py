
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from Checkin.models import Location

class ViewsTestCase(TestCase):
    databases = {"default", "location_db"}

    """Set up for all the tests"""
    def setUp(self):
        """
        Sets up the tests so that it is forced logged into the system to run the tests and the database has something to be tested against
        """
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)
        self.valid_location = Location.objects.using("location_db").create(
            name="Test Location",
            latitude=37.7749,
            longitude=-122.4194,
            radius=100  # 100 meters
        )

    def test_get_location_missing_params(self):
        """
        Tests initial load up of page where no location is given
        """
        response = self.client.get(reverse('get_location'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin_page.html')

    def test_get_location_missing_lat(self):
        """
        Tests when only longitude is given
        """
        response = self.client.get(reverse('get_location'), {'lon': '-74.0060'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin_page.html')

    def test_get_location_missing_lon(self):
        """
        Tests when only latitude is given
        """
        response = self.client.get(reverse('get_location'), {'lat': '40.7128'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin_page.html')

    def test_get_location_empty_values(self):
        """
        Tests when lat and lon are empty
        """
        response = self.client.get(reverse('get_location'), {'lat': '', 'lon': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkin_page.html')

    def test_get_location_invalid_values(self):
        """
        Tests if an invalid type is given
        """
        response = self.client.get(reverse('get_location'), {'lat': 'abc', 'lon': 'xyz'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_above_maximum_values(self):
        """
        Tests going over maximum
        """
        response = self.client.get(reverse('get_location'), {'lat': '90.1', 'lon': '180.1'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_below_minimum_values(self):
        """
        Tests going over minimum
        """
        response = self.client.get(reverse('get_location'), {'lat': '-90.1', 'lon': '-180.1'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_lat_below_minimum_values(self):
        """
        Tests lat going over minimum
        """
        response = self.client.get(reverse('get_location'), {'lat': '-90.1', 'lon': '0'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_lon_below_minimum_values(self):
        """
        Tests lon going over minimum
        """
        response = self.client.get(reverse('get_location'), {'lat': '0', 'lon': '-180.1'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_lat_above_maximum_values(self):
        """
        Tests lat going over maximum
        """
        response = self.client.get(reverse('get_location'), {'lat': '90.1', 'lon': '0'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_lon_above_maximum_values(self):
        """
        Tests lon going over maximum
        """
        response = self.client.get(reverse('get_location'), {'lat': '0', 'lon': '180.1'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_lat_invalid_values(self):
            """
            Tests if lat is an invalid type is given
            """
            response = self.client.get(reverse('get_location'), {'lat': 'abc', 'lon': '0'})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_lon_invalid_values(self):
        """
        Tests if lon is an invalid type is given
        """
        response = self.client.get(reverse('get_location'), {'lat': '0', 'lon': 'xyz'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    @patch("Checkin.views.geodesic")  # Mocking geodesic function
    def test_valid_location_checkin(self, mock_geodesic):
        """
        Tests if lon and lat are valid and are within the location range
        """
        mock_geodesic.return_value.meters = 50  # Within 100m radius
        response = self.client.get(reverse("database_location"), {"lat": "37.7749", "lon": "-122.4194"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Check-in Succesfull at Test Location!")

    @patch("Checkin.views.geodesic")
    def test_invalid_location_checkin(self, mock_geodesic):
        """
        Tests if lon and lat are valid but are not within the location range
        """
        mock_geodesic.return_value.meters = 200  # Outside 100m radius
        response = self.client.get(reverse("database_location"), {"lat": "37.7750", "lon": "-122.4195"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sorry, you are currently not in the right location", response.content.decode())

    @patch("Checkin.views.geodesic")
    def test_invalid_range_location_checkin(self, mock_geodesic):
        """
        Tests if lon and lat are valid but are just not within the location range
        """
        mock_geodesic.return_value.meters = 100.001  # Outside 100m radius
        response = self.client.get(reverse("database_location"), {"lat": "37.7750", "lon": "-122.4195"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sorry, you are currently not in the right location", response.content.decode())

    @patch("Checkin.views.geodesic")  # Mocking geodesic function
    def test_valid_location_checkin(self, mock_geodesic):
        """
        Tests if lon and lat are valid and are on top of the location
        """
        mock_geodesic.return_value.meters = 0  # Within 100m radius
        response = self.client.get(reverse("database_location"), {"lat": "37.7749", "lon": "-122.4194"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Check-in Succesfull at Test Location!")
