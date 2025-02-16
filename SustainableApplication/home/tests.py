from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from home.models import Locations, Collectable, CustomUser
from home.forms import CustomUserCreationForm



class LocationsModelTest(TestCase):
    def test_create_location(self):
        location = Locations.objects.create(name="Test Location")
        self.assertEqual(str(location), "Test Location")

class CollectableModelTest(TestCase):
    def test_create_collectable(self):
        item = Collectable.objects.create(name="Test Item")
        self.assertEqual(str(item), "Test Item")

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(username="testuser", password="testpass")
        self.assertEqual(str(user), "testuser")
        self.assertEqual(user.points, 0)

class LoginRequiredTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass")

    def test_index_redirects_when_not_logged_in(self):
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, "/accounts/login/?next=/home/")

    def test_index_accessible_when_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_user_can_signup(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
        })
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertRedirects(response, reverse("home"))

class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form = CustomUserCreationForm(data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CustomUserCreationForm(data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Testpassword123",
            "password2": "WrongPassword",
        })
        self.assertFalse(form.is_valid())

class URLTests(TestCase):
    def test_project_urls(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/home/")
        self.assertRedirects(response, "/accounts/login/?next=/home/")

# Fins tests

User1 = get_user_model()

class UserAuthTests(TestCase):

    def setUp(self):
        #set up new users
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "securepassword123"
        self.user = User1.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_login_existing_user(self):
        #test login
        response = self.client.post(reverse("login"), {"username": self.username, "password": self.password})
        self.assertRedirects(response, reverse("home"))

    def test_register_new_user(self):
        #test signup
        new_user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "newPassword456!",
            "password2": "newPassword456!",
        }
        response = self.client.post(reverse("signup"), new_user_data)
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User1.objects.filter(username="newuser").exists())


    def test_long_username(self):
        data = {
            "username": "a" * 152,
            "email": "longusername@example.com",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensure this value has at most 150 characters (it has 152).")
    
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
        self.assertFalse(User1.objects.filter(username=data["username"]).exists())
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
        self.assertRedirects(response, reverse("home"))

    def test_email_case_insensitive_login(self):
        response = self.client.post(reverse("login"), {"username": self.email.upper(), "password": self.password})
        self.assertRedirects(response, reverse("home"))

    def test_empty_username_login(self):
        response = self.client.post(reverse("login"), {"username": "", "password": self.password})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_empty_password_login(self):
        response = self.client.post(reverse("login"), {"username": self.username, "password": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
