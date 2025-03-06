"""Tests the webpage is displayed correctly"""
from django.test import TestCase

class TestCollectablesPage(TestCase):
    """Tests collectable webpage display"""
    def test_webpage_response_code(self):
        """Tests collectables webpage gives the correct response code"""
        response = self.client.get("/collectables/")
        self.assertEqual(response.status_code, 200)

    def test_webpage_contains_image(self):
        """Tests the collectables webpage uses the right html template"""
        response = self.client.get("/collectables/")
        self.assertTemplateUsed(response, "gallery.html")
        