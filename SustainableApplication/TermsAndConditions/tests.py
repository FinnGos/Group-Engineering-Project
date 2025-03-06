from django.test import TestCase, Client
from django.urls import reverse

"""Tests to see if the webpage loads"""
def test_privacy_page_loads(self):
    """
    Asks for the webpage checks if it gets returned
    """
    response = self.client.get(reverse('TermsAndConditions'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'terms.html')