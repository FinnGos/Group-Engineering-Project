from django.test import TestCase

#Arigato daniel
class SimpleTest(TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)


from django.test import TestCase, Client
from django.urls import reverse

class ProjectWideURLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_root_url_redirects_to_login(self):
        response = self.client.get("/")
        self.assertRedirects(response, "/accounts/login/", status_code=302, target_status_code=200)

    def test_admin_page_access(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_accounts_urls_exist(self):
        login_response = self.client.get("/accounts/login/")
        self.assertEqual(login_response.status_code, 200)  # Login page loads fine

        # Logout requires POST request
        logout_response = self.client.post("/accounts/logout/")
        self.assertEqual(logout_response.status_code, 302)  # Should redirect