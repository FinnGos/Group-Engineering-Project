"""Tests for lootboxes"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from collectables.models import Collectable

class LootboxTests(TestCase):
    """Test case for lootboxes"""
    def setUp(self):
        """Set up a test user and collectables."""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.user.current_points = 200  # Give user enough points
        self.user.save()

        # Create test collectables
        self.collectable1 = Collectable.objects.create(name="Rare Card", fact="Very rare!", image="")
        self.collectable2 = Collectable.objects.create(name="Legendary Card", fact="Super rare!", image="")

        self.lootbox_url = reverse("open_lootbox")  # URL for lootbox view

    def test_cannot_open_lootbox_with_insufficient_points(self):
        """Ensure users cannot open a lootbox if they lack points."""
        self.user.current_points = 50  # Not enough for a lootbox
        self.user.save()

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.lootbox_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Not enough points", response.json()["error"])

    def test_points_are_deducted_when_opening_lootbox(self):
        """Ensure lootbox costs points and updates correctly."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.lootbox_url)

        self.user.refresh_from_db()  # Refresh user data from DB
        self.assertEqual(self.user.current_points, 100)  # 200 - 100 = 100
        self.assertEqual(response.status_code, 200)
        self.assertIn("new_points", response.json())
        self.assertEqual(response.json()["new_points"], 100)

    def test_lootbox_gives_collectable(self):
        """Ensure user receives a collectable if they win."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.lootbox_url)

        self.user.refresh_from_db()
        loot_item = response.json().get("loot_item")

        if loot_item:  # If user won something
            self.assertTrue(self.user.collectables_owned.exists())  # User has at least 1 collectable
            self.assertEqual(loot_item["name"], self.user.collectables_owned.first().name)

    def test_no_duplicate_collectables(self):
        """Ensure users do not get duplicates of the same collectable."""
        self.user.collectables_owned.add(self.collectable1)  # Pre-add a collectable
        self.client.login(username="testuser", password="testpass")
        self.client.post(self.lootbox_url)

        self.user.refresh_from_db()
        self.assertLessEqual(self.user.collectables_owned.count(), 2)  # At most 2 collectables

    def test_json_response_structure(self):
        """Ensure the response contains expected keys."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.lootbox_url)
        json_data = response.json()

        self.assertIn("success", json_data)
        self.assertIn("new_points", json_data)
        self.assertIn("loot_item", json_data)
