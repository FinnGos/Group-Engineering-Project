from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from riddles.models import Riddle
from Checkin.models import Location
import datetime

User = get_user_model()

class RiddleTests(TestCase):
    """Tests for riddle check-in and weekly cycle behavior."""
    
    databases = {"default", "location_db"}  # Allow test access to both databases

    def setUp(self):
        """Set up test data for riddles, locations, and a user."""
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Create 16 riddles, 4 for each week
        self.riddles = []
        for i in range(16):
            location = Location.objects.using("location_db").create(
                id=i+50,  
                name=f"Test Location {i}",
                latitude=50.736 + (i * 0.001),
                longitude=-3.529 - (i * 0.001),
                radius=20
            )
            riddle = Riddle.objects.create(
                riddle_question=f"Test Riddle {i}",
                location_id=location.id,
                week_group=(i % 4) + 1  # Cycle through 1-4
            )
            self.riddles.append(riddle)

    def test_four_riddles_displayed(self):
        """ Test that exactly 4 riddles are displayed for the current week."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("riddles_page"))

        self.assertEqual(response.status_code, 200)
        riddles_in_page = response.context["riddles"]
        self.assertEqual(len(riddles_in_page), 4, "Should display exactly 4 riddles for the current week.")

    def test_all_riddles_are_different(self):
        """ Test that all riddles displayed in a week are different."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("riddles_page"))

        riddles_in_page = response.context["riddles"]
        riddle_questions = [riddle.riddle_question for riddle in riddles_in_page]

        self.assertEqual(len(riddle_questions), len(set(riddle_questions)), "Riddles should be unique.")

    def test_riddles_change_each_week(self):
        """ Test that riddles change every week on a 4-week cycle."""
        self.client.login(username="testuser", password="password123")

        # Get riddles for the current week
        week_1_riddles = list(Riddle.objects.filter(week_group=(datetime.date.today().isocalendar()[1] % 4) + 1))

        # Simulate moving forward by 1 week
        next_week = (datetime.date.today().isocalendar()[1] + 1) % 4 + 1
        week_2_riddles = list(Riddle.objects.filter(week_group=next_week))

        self.assertNotEqual(set(week_1_riddles), set(week_2_riddles), "Riddles should change each week.")

def test_riddle_checkin_marks_as_completed(self):
    """Test that checking in at the correct location marks the riddle as completed."""
    self.client.login(username="testuser", password="password123")

    # Pick a riddle from the current week
    current_week = (datetime.date.today().isocalendar()[1] % 4) + 1
    riddle_to_checkin = Riddle.objects.filter(week_group=current_week).first()

    # Use the exact location of the riddle
    riddle_lat = riddle_to_checkin.latitude
    riddle_lon = riddle_to_checkin.longitude

    checkin_url = reverse("get_location", args=[5])
    
    # Debugging print to see location
    print(f"Checking in at: lat={riddle_lat}, lon={riddle_lon}")

    # Perform check-in request
    response = self.client.get(checkin_url, {"lat": riddle_lat, "lon": riddle_lon})

    # Refresh user model to fetch latest updates from the DB
    self.user.refresh_from_db()

    # Debugging print to verify updated riddles
    print("User completed riddles after check-in:", self.user.completed_riddles.all())

    # Now check if the riddle is in the user's completed riddles
    self.assertIn(riddle_to_checkin, self.user.completed_riddles.all(), "Riddle should be marked as completed after check-in.")
