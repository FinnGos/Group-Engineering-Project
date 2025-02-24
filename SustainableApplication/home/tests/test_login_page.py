from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from home.models import CustomUser
from home.forms import CustomUserCreationForm


class CustomUserModelTest(TestCase):
    """Test the CustomUser model functionality."""
    def test_create_user(self):
        """
        Test creating a user with username and password.
        Ensure the user is created with default points as 0.
        """
        user = CustomUser.objects.create_user(username="testuser", password="testpass")
        self.assertEqual(str(user), "testuser")
        self.assertEqual(user.current_points, 0)
        self.assertEqual(user.all_time_points, 0)


class LoginRequiredTests(TestCase):
    """Test views that require a user to be logged in."""

    def setUp(self):
        """
        Set up client and test user for the LoginRequiredTests.
        """
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass"
        )

    def test_index_redirects_when_not_logged_in(self):
        """
        Test if the index page redirects when the user is not logged in.
        """
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, "/accounts/login/?next=/home/")

    def test_index_accessible_when_logged_in(self):
        """
        Test if the index page is accessible when logged in.
        """
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class SignupViewTest(TestCase):
    """Test the signup view and user creation."""

    def setUp(self):
        """
        Set up the client for the SignupViewTest.
        """
        self.client = Client()

    def test_signup_page_loads(self):
        """
        Test if the signup page loads correctly.
        """
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_user_can_signup(self):
        """
        Test if a user can successfully sign up.
        """
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "Testpassword123",
                "password2": "Testpassword123",
            },
        )
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertRedirects(response, reverse("home"))


class CustomUserCreationFormTest(TestCase):
    """Test the CustomUserCreationForm for validation."""

    def test_valid_form(self):
        """
        Test if the form is valid when given correct data.
        """
        form = CustomUserCreationForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "Testpassword123",
                "password2": "Testpassword123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Test if the form is invalid when passwords don't match.
        """
        form = CustomUserCreationForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "Testpassword123",
                "password2": "WrongPassword",
            }
        )
        self.assertFalse(form.is_valid())


class URLTests(TestCase):
    """Test the project's URLs."""

    def test_project_urls(self):
        """
        Test if the project URLs are working correctly.
        """
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/home/")
        self.assertRedirects(response, "/accounts/login/?next=/home/")


User1 = get_user_model()


class UserAuthTests(TestCase):
    """Test user authentication functionality."""

    def setUp(self):
        """
        Set up a new user for UserAuthTests.
        """
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "securepassword123"
        self.user = User1.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )

    def test_login_existing_user(self):
        """
        Test if an existing user can log in successfully.
        """
        response = self.client.post(
            reverse("login"), {"username": self.username, "password": self.password}
        )
        self.assertRedirects(response, reverse("home"))

    def test_register_new_user(self):
        """
        Test if a new user can successfully register.
        """
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
        """
        Test if a long username (greater than 150 characters) is rejected.
        """
        data = {
            "username": "a" * 152,
            "email": "longusername@example.com",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Ensure this value has at most 150 characters (it has 152)."
        )

    def test_whitespace_username(self):
        """
        Test if a username consisting only of whitespace is rejected.
        """
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
        """
        Test if a username with special characters is rejected.
        """
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
        """
        Test if SQL injection attempts are blocked in the username field.
        """
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
        """
        Test if SQL injection attempts are blocked during login.
        """
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
        """
        Test if login fails when the username is empty.
        """
        response = self.client.post(
            reverse("login"), {"username": "", "password": self.password}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_empty_password_login(self):
        """
        Test if login fails when the password is empty.
        """
        response = self.client.post(
            reverse("login"), {"username": self.username, "password": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
