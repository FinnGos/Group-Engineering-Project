"""Tests for Home"""
from datetime import datetime, timedelta
import os
import logging
import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from home.models import CustomUser
from home.forms import CustomUserCreationForm
from home.views import cleanup_old_logs

TEST_LOG_FILE = os.path.join(tempfile.gettempdir(), "django_test_logs.log")


class CustomUserModelTest(TestCase):
    """Test case for the CustomUser model."""

    def test_create_user(self):
        """Test that a CustomUser object can be created successfully."""
        user = CustomUser.objects.create_user(username="testuser", password="testpass")
        self.assertEqual(str(user), "testuser")
        self.assertEqual(user.current_points, 0)
        self.assertEqual(user.all_time_points, 0)


class LoginRequiredTests(TestCase):
    """Test cases for login-required views."""

    def setUp(self):
        """Set up a test user for authentication tests."""
        self.client = Client()
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass")

    def test_index_redirects_when_not_logged_in(self):
        """Test that the home page redirects to login if the user is not logged in."""
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, "/accounts/login/?next=/home/")

    def test_index_accessible_when_logged_in(self):
        """Test that the home page is accessible to logged-in users."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class SignupViewTest(TestCase):
    """Test case for user signup view."""

    def setUp(self):
        """Set up a test client."""
        self.client = Client()

    def test_signup_page_loads(self):
        """Test that the signup page loads successfully."""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_user_can_signup(self):
        """Test that a user can sign up successfully."""
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
        })
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertRedirects(response, reverse("home"))


class CustomUserCreationFormTest(TestCase):
    """Test case for the CustomUserCreationForm."""

    def test_valid_form(self):
        """Test that the form is valid with correct input data."""
        form = CustomUserCreationForm(data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Test that the form is invalid when passwords do not match."""
        form = CustomUserCreationForm(data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Testpassword123",
            "password2": "WrongPassword",
        })
        self.assertFalse(form.is_valid())


class URLTests(TestCase):
    """Test case for project URLs."""

    def test_project_urls(self):
        """Test that important URLs return the correct responses."""
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/home/")
        self.assertRedirects(response, "/accounts/login/?next=/home/")


User1 = get_user_model()


class UserAuthTests(TestCase):
    """Test case for user authentication (login and signup)."""

    def setUp(self):
        """Set up test users for authentication tests."""
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "securepassword123"
        self.user = User1.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_login_existing_user(self):
        """Test that an existing user can log in successfully."""
        response = self.client.post(reverse("login"), {"username": self.username, "password": self.password})
        self.assertRedirects(response, reverse("home"))

    def test_register_new_user(self):
        """Test that a new user can sign up successfully."""
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
        """Test that an overly long username is not allowed."""
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
        """Test that a username consisting only of whitespace is not allowed."""
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
        """Test that a username with special characters is not allowed."""
        data = {
            "username": "user@#$%",
            "email": "special@example.com",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid username.")

    def test_sql_injection_username(self):
        """Test that SQL injection in the username field is prevented."""
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
        """Test that SQL injection in the login fields is prevented."""
        data = {
            "username": "' OR '1'='1",
            "password": "fakepassword",
        }
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_case_insensitive_username_login(self):
        """Test that login is case-insensitive for usernames."""
        response = self.client.post(reverse("login"), {"username": self.username.upper(), "password": self.password})
        self.assertEqual(response.status_code, 200)

    def test_email_case_insensitive_login(self):
        """Test that login is case-insensitive for emails."""
        response = self.client.post(reverse("login"), {"username": self.email.upper(), "password": self.password})
        self.assertEqual(response.status_code, 200)

    def test_empty_username_login(self):
        """Test that inputting an empty username in will return error with message."""
        response = self.client.post(reverse("login"), {"username": "", "password": self.password})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_empty_password_login(self):
        """Test that inputting an empty password in will return error with message."""
        response = self.client.post(reverse("login"), {"username": self.username, "password": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
#From her

class LogoutFunctionalityTests(TestCase):
    """Test cases for user logout functionality."""

    def setUp(self):
        """Set up a test user and client for logout tests."""
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
            self.assertTrue(
                any("User logged out: testuser" in message for message in log_capture.output)
            )

    def test_logout_for_unauthenticated_user(self):
        """Test that a logout attempt by an unauthenticated user redirects to the login page."""
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)


class DeleteAccountViewTests(TestCase):
    """Test cases for account deletion."""

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

        with self.assertRaises(User1.DoesNotExist):
            User1.objects.get(username="testuser")

    def test_cannot_login_after_deletion(self):
        """Test that the user cannot log in after their account is deleted."""
        self.client.login(username="testuser", password="testpassword")
        self.client.post(self.delete_account_url)

        login_successful = self.client.login(username="testuser", password="testpassword")
        self.assertFalse(login_successful)

    def test_logging_of_account_deletion(self):
        """Test that the account deletion is logged correctly."""
        with self.assertLogs("django", level="INFO") as log:
            self.client.login(username="testuser", password="testpassword")
            self.client.post(self.delete_account_url)

        self.assertTrue(
            any("User deleted account: testuser" in message for message in log.output),
            "Expected log message not found in log output."
        )


def create_test_log_file():
    """Create a test log file with old and recent log entries."""
    now = datetime.now()

    old_log_time = now - timedelta(days=100)  # 100 days ago (should be deleted)
    recent_log_time = now - timedelta(days=30)  # 30 days ago (should be kept)

    old_log_entry = f"django INFO {old_log_time.strftime('%Y-%m-%d %H:%M:%S,%f')} views User logged in: old_user\n"
    recent_log_entry = f"django INFO {recent_log_time.strftime('%Y-%m-%d %H:%M:%S,%f')} views User logged in: recent_user\n"

    with open(TEST_LOG_FILE, "w", encoding="utf-8") as file:
        file.writelines([old_log_entry, recent_log_entry])


def test_cleanup_old_logs():
    """Test the cleanup_old_logs function."""

    create_test_log_file()
    cleanup_old_logs()

    with open(TEST_LOG_FILE, "r", encoding="utf-8") as file:
        remaining_logs = file.readlines()

    assert len(remaining_logs) == 1, "Old logs were not deleted!"
    assert "recent_user" in remaining_logs[0], "Recent log entry was mistakenly deleted!"


class AccountTests(TestCase):
    """Test cases for editing account details."""

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



class ViewUserDataTests(TestCase):
    """Test cases for viewing personal data."""

    def setUp(self):
        """Set up a test user and create a test log file."""
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="matt4", password="securepassword")
        self.client.login(username="matt4", password="securepassword")

        self.log_entry = f"django INFO 2025-02-24 13:45:58,056 views 1288 34744 User asked for personal data stored: {self.user.username}\n"
        
        # Ensure we properly close the file after writing
        with open(TEST_LOG_FILE, "w", encoding="utf-8") as file:
            file.write(self.log_entry)

    def tearDown(self):
        """Ensure logging is properly closed and remove the test log file."""
        logging.shutdown()  # Ensure logging handlers are closed

        # Manually close open handlers before deleting
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
            handler.close()

        # Delete log file
        if os.path.exists(TEST_LOG_FILE):
            try:
                os.remove(TEST_LOG_FILE)
            except PermissionError:
                print(f"Could not delete {TEST_LOG_FILE}, file may still be in use.")

    def test_user_can_view_personal_data(self):
        """Test that a logged-in user can access their personal data page."""
        response = self.client.get(reverse("view_user_data"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/view_user_data.html")

        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)

    def test_user_sees_correct_log_entry(self):
        """Test that the correct log entry appears on the page."""
        response = self.client.get(reverse("view_user_data"))
        self.assertContains(response, self.log_entry.strip())

    def test_user_does_not_see_other_user_logs(self):
        """Ensure the user does not see logs from another user."""
        other_log = "django INFO 2025-02-24 14:00:00,000 views 1234 56789 User asked for personal data stored: matt44\n"

        # Properly write and close the log file
        with open(TEST_LOG_FILE, "a", encoding="utf-8") as file:
            file.write(other_log)

        response = self.client.get(reverse("view_user_data"))

        self.assertContains(response, self.log_entry.strip())
        self.assertNotContains(response, "matt44")