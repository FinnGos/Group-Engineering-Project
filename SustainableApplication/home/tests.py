from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from home.models import Locations, Collectable, CustomUser
from home.forms import CustomUserCreationForm
from django.contrib.auth import login

from datetime import datetime, timedelta
import os
from home.views import cleanup_old_logs

TEST_LOG_FILE = "test_django_logs.log"

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
        """
        Test if login is case-insensitive for usernames.
        """
        response = self.client.post(
            reverse("login"),
            {"username": self.username.upper(), "password": self.password},
        )
        self.assertEqual(response.status_code, 200)

    def test_email_case_insensitive_login(self):
        """
        Test if login is case-insensitive for emails.
        """
        response = self.client.post(
            reverse("login"),
            {"username": self.email.upper(), "password": self.password},
        )
        self.assertEqual(response.status_code, 200)

    def test_empty_username_login(self):
        response = self.client.post(reverse("login"), {"username": "", "password": self.password})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_empty_password_login(self):
        response = self.client.post(reverse("login"), {"username": self.username, "password": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")


#Tests for log out

class LogoutFunctionalityTests(TestCase):
    def setUp(self):
        """Set up a test user and client for the tests."""
        self.client = Client()
        self.user = User1.objects.create_user(username="testuser", password="testpassword")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
    
    def test_logout_redirects_to_login(self):
        """Test that logging out redirects to the login page."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)

    def test_logout_logs_event(self):
        """Test that a logout event is logged."""
        with self.assertLogs("django", level="INFO") as log_capture:
            self.client.login(username="testuser", password="testpassword")
            self.client.get(self.logout_url)  # Trigger logout
            # Check the logs for the logout message
            self.assertTrue(
                any("User logged out: testuser" in message for message in log_capture.output)
            )

    def test_logout_for_unauthenticated_user(self):
        """Test that a logout attempt by an unauthenticated user redirects to the login page."""
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)

#Tests for delete account

class DeleteAccountViewTests(TestCase):

    def setUp(self):
        """Set up a test user for account deletion tests."""
        self.user = User1.objects.create_user(username="testuser", password="testpassword")
        self.delete_account_url = reverse("delete_account")
        self.login_url = reverse("login")

    def test_account_deletion_redirects_to_login(self):
        """Test that account deletion redirects to the login page."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.delete_account_url)
        self.assertRedirects(response, self.login_url)

    def test_account_deleted_successfully(self):
        """Test that deleting an account removes it from the database."""
        self.client.login(username="testuser", password="testpassword")
        self.client.post(self.delete_account_url)

        # Ensure the user is deleted
        with self.assertRaises(User1.DoesNotExist):
            User1.objects.get(username="testuser")

    def test_cannot_login_after_deletion(self):
        """Test that the user cannot log in after their account is deleted."""
        self.client.login(username="testuser", password="testpassword")
        self.client.post(self.delete_account_url)

        # Try to log in with the deleted account
        login_successful = self.client.login(username="testuser", password="testpassword")
        self.assertFalse(login_successful)

    def test_logging_of_account_deletion(self):
        """Test that the account deletion is logged correctly."""
        with self.assertLogs("django", level="INFO") as log:
            self.client.login(username="testuser", password="testpassword")
            self.client.post(self.delete_account_url)

        # Check that at least one log message contains the expected text
        self.assertTrue(
            any("User deleted account: testuser" in message for message in log.output),
            "Expected log message not found in log output."
        )

# Tests for deleting logs

def create_test_log_file():
    """Creates a test log file with old and recent log entries."""
    now = datetime.now()

    # Create log entries
    old_log_time = now - timedelta(days=100)  # 100 days ago (should be deleted)
    recent_log_time = now - timedelta(days=30)  # 30 days ago (should be kept)

    old_log_entry = f"django INFO {old_log_time.strftime('%Y-%m-%d %H:%M:%S,%f')} views User logged in: old_user\n"
    recent_log_entry = f"django INFO {recent_log_time.strftime('%Y-%m-%d %H:%M:%S,%f')} views User logged in: recent_user\n"

    # Write logs to file
    with open(TEST_LOG_FILE, "w", encoding="utf-8") as file:
        file.writelines([old_log_entry, recent_log_entry])

def test_cleanup_old_logs():
    """Tests the cleanup_old_logs function."""
    global LOG_FILE_PATH  # Use the global variable for testing
    LOG_FILE_PATH = TEST_LOG_FILE  # Temporarily set the log file to the test file

    create_test_log_file()  # Create test logs
    cleanup_old_logs()  # Run log cleanup

    # Read the cleaned log file
    with open(TEST_LOG_FILE, "r", encoding="utf-8") as file:
        remaining_logs = file.readlines()

    # Assertions
    assert len(remaining_logs) == 1, "Old logs were not deleted!"
    assert "recent_user" in remaining_logs[0], "Recent log entry was mistakenly deleted!"

#Tests for editing acc detials


class AccountTests(TestCase):
    def setUp(self):
        """Create a test user before each test."""
        self.user = User1.objects.create_user(username="testuser", email="test@example.com", password="password123")

    def test_edit_account_details(self):
        """Test if a user can edit their details successfully."""
        self.user.first_name = "Updated"
        self.user.last_name = "Name"
        self.user.email = "updated@example.com"
        self.user.save()

        updated_user = User1.objects.get(username="testuser")
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "Name")
        self.assertEqual(updated_user.email, "updated@example.com")