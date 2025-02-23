from django.test import TestCase, Client
from django.urls import reverse

class PrivacyViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_privacy_page_loads(self):
        response = self.client.get(reverse('privacyPolicy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'privacy.html')