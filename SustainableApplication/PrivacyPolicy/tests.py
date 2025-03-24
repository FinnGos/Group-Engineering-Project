"""Tests for privacy policy"""
from django.urls import reverse

def test_privacy_page_loads(self):
    """Tests to see if the webpage loads"""
    response = self.client.get(reverse('privacyPolicy'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'privacy.html')