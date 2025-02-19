from django.test import TestCase, Client
from django.urls import reverse

class ViewsTestCase(TestCase):
    """Test the check-in button"""
    def test_get_location_success(self):
        response = self.client.get(reverse('get_location'), {'lat': '40.7128', 'lon': '-74.0060'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check-In Successful! Lat: 40.7128, Lon: -74.0060')
        self.assertTemplateUsed(response, 'index.html')

    def test_get_location_missing_params(self):
        response = self.client.get(reverse('get_location'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_location_missing_lat(self):
        response = self.client.get(reverse('get_location'), {'lon': '-74.0060'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_location_missing_lon(self):
        response = self.client.get(reverse('get_location'), {'lat': '40.7128'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_location_empty_values(self):
        response = self.client.get(reverse('get_location'), {'lat': '', 'lon': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_location_invalid_values(self):
        response = self.client.get(reverse('get_location'), {'lat': 'abc', 'lon': 'xyz'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_maximum_values(self):
        response = self.client.get(reverse('get_location'), {'lat': '90.0', 'lon': '180.0'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check-In Successful! Lat: 90.0, Lon: 180.0')
        self.assertTemplateUsed(response, 'index.html')

    def test_get_location_minimum_values(self):
        response = self.client.get(reverse('get_location'), {'lat': '-90.0', 'lon': '-180.0'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check-In Successful! Lat: -90.0, Lon: -180.0')
        self.assertTemplateUsed(response, 'index.html')

    def test_get_location_above_maximum_values(self):
        response = self.client.get(reverse('get_location'), {'lat': '90.1', 'lon': '180.1'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')

    def test_get_location_below_minimum_values(self):
        response = self.client.get(reverse('get_location'), {'lat': '-90.1', 'lon': '-180.1'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid location data.')
