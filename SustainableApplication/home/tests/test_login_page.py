from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom user model dynamically

class UserAuthTests(TestCase):

    def setUp(self):
        """Set up a test user before each test."""
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "securepassword123"  # Must meet Django's password validation criteria
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_login_existing_user(self):
        """test that an existing user can log in."""
        response = self.client.post(reverse("login"), {"username": self.username, "password": self.password})
        self.assertredirects(response, reverse("index")) #navigate to the login page to login

    def test_register_new_user(self):
        """Test that a new user can register successfully."""
        new_user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "newPassword456!", #I know storing plaintext password is bad 
            "password2": "newPassword456!", #Potentially we could add a sub user "test" user for this
        }
        response = self.client.post(reverse("signup"), new_user_data)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_password_too_short(self):
        """Test that a password with fewer than 8 characters is rejected."""
        data = {
            "username": "shortpassuser",
            "email": "shortpass@example.com",
            "password1": "short",
            "password2": "short",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is too short. It must contain at least 8 characters.")

    def test_password_too_common(self):
        """Test that a common password is rejected."""
        data = {
            "username": "commonpassuser",
            "email": "commonpass@example.com",
            "password1": "password123",
            "password2": "password123",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is too common.")

    def test_password_entirely_numeric(self):
        """Test that an all-numeric password is rejected."""
        data = {
            "username": "numericpassuser",
            "email": "numericpass@example.com",
            "password1": "12345678",
            "password2": "12345678",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is entirely numeric.")

    def test_password_similar_to_personal_info(self):
        """Test that a password too similar to personal info is rejected."""
        data = {
            "username": "similaruser",
            "email": "similar@example.com",
            "password1": "similaruser123",
            "password2": "similaruser123",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The password is too similar to the username.")

    def test_email_required(self):
        """Test that email is required for registration."""
        data = {
            "username": "noemailuser",
            "password1": "ValidPass789!",
            "password2": "ValidPass789!",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_duplicate_username(self):
        """Test that duplicate usernames are not allowed."""
        data = {
            "username": self.username,  # Already exists
            "email": "newemail@example.com",
            "password1": "AnotherPass789!",
            "password2": "AnotherPass789!",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that username already exists.")

    def test_duplicate_email(self):
        """Test that duplicate emails are not allowed."""
        data = {
            "username": "uniqueuser",
            "email": self.email,  # Already exists
            "password1": "UniquePass123!",
            "password2": "UniquePass123!",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that email already exists.")
