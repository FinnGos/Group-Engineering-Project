from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthTests(TestCase):

    def setUp(self):
        #set up new users
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "securepassword123"
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_login_existing_user(self):
        #test login
        response = self.client.post(reverse("login"), {"username": self.username, "password": self.password})
        self.assertRedirects(response, reverse("index"))

    def test_register_new_user(self):
        #test signup
        new_user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "newPassword456!",
            "password2": "newPassword456!",
        }
        response = self.client.post(reverse("signup"), new_user_data)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())


    def test_long_username(self):
        data = {
            "username": "a" * 151,
            "email": "longusername@example.com",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensure this value has at most 150 characters.")

    def test_whitespace_username(self):
        data = {
            "username": " ",
            "email": "whitespace@example.com",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_special_characters_username(self):
        data = {
            "username": "user@#$%",
            "email": "special@example.com",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid username.")

    # SQL Injection Tests
    def test_sql_injection_username(self):
        data = {
            "username": "test'; DROP TABLE users; --",
            "email": "sqlinject@example.com",
            "password1": "SqlPass123!",
            "password2": "SqlPass123!",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=data["username"]).exists())
        self.assertContains(response, "Enter a valid username.")

    def test_sql_injection_login(self):
        data = {
            "username": "' OR '1'='1",
            "password": "fakepassword",
        }
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")


    def test_case_insensitive_username_login(self):
        response = self.client.post(reverse("login"), {"username": self.username.upper(), "password": self.password})
        self.assertRedirects(response, reverse("index"))

    def test_email_case_insensitive_login(self):
        response = self.client.post(reverse("login"), {"username": self.email.upper(), "password": self.password})
        self.assertRedirects(response, reverse("index"))

    def test_empty_username_login(self):
        response = self.client.post(reverse("login"), {"username": "", "password": self.password})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_empty_password_login(self):
        response = self.client.post(reverse("login"), {"username": self.username, "password": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
