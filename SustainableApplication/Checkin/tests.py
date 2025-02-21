from django.test import TestCase, Client
from django.urls import reverse

class ViewsTestCase(TestCase):
    """Test the check-in button"""
    def test_get_location_success(self):
        """
        Tests a successful case of location check
        """
        response = self.client.get(reverse('get_location'), {'lat': '40.7128', 'lon': '-74.0060'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check-In Successful! Lat: 40.7128, Lon: -74.0060')
        self.assertTemplateUsed(response, 'checkin_page.html')

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

    def test_get_location_maximum_values(self):
        """
        Tests the edge cases of maximum
        """
        response = self.client.get(reverse('get_location'), {'lat': '90.0', 'lon': '180.0'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check-In Successful! Lat: 90.0, Lon: 180.0')
        self.assertTemplateUsed(response, 'checkin_page.html')

    def test_get_location_minimum_values(self):
        """
        Tests the edge of minimum
        """
        response = self.client.get(reverse('get_location'), {'lat': '-90.0', 'lon': '-180.0'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check-In Successful! Lat: -90.0, Lon: -180.0')
        self.assertTemplateUsed(response, 'checkin_page.html')

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