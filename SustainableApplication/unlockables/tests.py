from django.test import TestCase, Client, RequestFactory
from home.models import CustomUser
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.shortcuts import resolve_url
from django.contrib import messages
from .models import Item, UserItem, Rubbish, UserRubbish, Building
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages 
from collectables.models import Collectable
from django.utils.timezone import now, timedelta
import os
from .views import buy_item, shop, game_map, clean_rubbish
from django.conf import settings

User = get_user_model()
TEST_IMAGE_PATH = os.path.join(settings.MEDIA_ROOT,"test_image_1.png")  # Ensure this file exists in your project

class GameMapBuildingTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password")

        # Sets up the mock collectables and buildings
        self.collectable = Collectable.objects.create(name="Harrison", image=TEST_IMAGE_PATH)
        self.building1 = Building.objects.create(name="Harrison", sustainability_score=10, image=TEST_IMAGE_PATH, locked_image = TEST_IMAGE_PATH)
        self.building2 = Building.objects.create(name="Streatham", sustainability_score=10, image=TEST_IMAGE_PATH, locked_image = TEST_IMAGE_PATH)

        self.url = reverse("map")

    def test_all_buildings_initially_locked(self):
        """Test that all the buildings initially start off locked on the game map."""
        
        # Logins in
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)

        # Checks if the buildings are locked
        self.assertNotContains(response, "Harrison")
        self.assertNotContains(response, "Streatham")

    def test_unlocked_buildings_shown(self):
        """Test that unlocked buildings are marked correctly on the game map."""
        
        # Simulate the user unlocking the building
        collectable = self.collectable
        self.user.collectables_owned.add(collectable)
        
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)

        # Assert that the building name appears on the map
        self.assertContains(response, "Harrison")
        self.assertNotContains(response, "Streatham")

    def test_unlocked_multiple_buildings_shown(self):
        """Test that unlocked buildings are marked correctly on the game map."""
        
        # Simulate the user unlocking the building
        collectable = self.collectable
        self.user.collectables_owned.add(collectable)

        # Simulate the user unlocking another building
        self.collectable2 = Collectable.objects.create(name="Streatham", image=TEST_IMAGE_PATH)
        collectable2 = self.collectable2
        self.user.collectables_owned.add(collectable2)
        
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)

        # Assert that the building name appears on the map
        self.assertContains(response, "Harrison")
        self.assertContains(response, "Streatham")



class GameMapRubbishTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password")

        # Sets up the mock rubbish object
        self.item = Rubbish.objects.create(name="rubbish", x = 1, y = 1, image=TEST_IMAGE_PATH)
        self.rubbish = UserRubbish.objects.create(useritem=self.user, item=self.item, cleaned=True, cleaned_at= now())
        self.url = reverse('map')

    def test_rubbish_shown_for_user(self):
        """Test that rubbish is shown correctly for the user."""
        self.client.login(username="testuser", password="password")
        
        # Associate rubbish with the user
        UserRubbish.objects.create(useritem=self.user, item=self.item)

        response = self.client.get(self.url)

        # Check if rubbish appears
        self.assertContains(response, "rubbish")
    
    def test_new_rubbish_added_for_user(self):
        """Test that new rubbish is added to the user if they don't already have it."""
        
        self.client.login(username="testuser", password="password")
        # Create new rubbish not associated with any user yet
        new_rubbish = Rubbish.objects.create(name="rubbish", x = 1, y = 1, image=TEST_IMAGE_PATH)

        # Ensure that no user rubbish exists for the new item yet
        self.assertEqual(UserRubbish.objects.filter(useritem=self.user, item=new_rubbish).count(), 0)

        response = self.client.get(self.url)

        # Ensure the new rubbish appears in the response
        self.assertContains(response, "rubbish")

        # Check that the new rubbish has been associated with the user
        self.assertEqual(UserRubbish.objects.filter(useritem=self.user, item=new_rubbish).count(), 1)

    def test_rubbish_respawn_shown_for_users(self):
        """Test that once 3 days have passed, the user can see the rubbish again."""
        self.rubbish.cleaned_at = now() - timedelta(days=3, minutes=1)
        self.rubbish.save()

        if self.rubbish.should_respawn():
            # Reset rubbish for the user
            self.rubbish.save()

        self.assertFalse(self.rubbish.cleaned)

    def test_rubbish_respawn_decreases_campus_creds(self):
        """Test that once the rubbish respawns, the user's campus creds decrease by 2."""

        # Sets user's campus creds to 10
        self.user.all_time_points = 10
        self.user.save()
        self.rubbish.cleaned_at = now() - timedelta(days=3, minutes=1)
        self.rubbish.save()

        # Respawns rubbish
        if self.rubbish.should_respawn():
            # Reset rubbish for the user
            self.rubbish.save()
        self.user.refresh_from_db()

        # Checks if campus creds change
        self.assertEqual(self.user.all_time_points, 8)

    def test_removing_rubbish_decreases_carbo_coins(self):
        """Test that if the user removes the rubbish, their Carbo Coins decrease by 5."""
        self.client.force_login(self.user)

        # Sets the carbo coins
        initial_coins = self.user.current_points

        # Call the view
        self.client.post(reverse("clean_rubbish", args=[self.rubbish.id]))
        self.user.refresh_from_db()

        # Check if the carbo coins have decreased after cleaning 
        self.assertEqual(self.user.current_points, initial_coins - 5)

    def test_removing_rubbish_increases_campus_creds(self):
        """Test that if the user removes the rubbish, their campus creds increase by 2."""
        self.client.force_login(self.user)

        # Sets the campus creds 
        initial_creds = self.user.all_time_points

        # Call the view
        self.client.post(reverse("clean_rubbish", args=[self.rubbish.id]))
        self.user.refresh_from_db()

        # Check if the campus creds have increased after cleaning 
        self.assertEqual(self.user.all_time_points, initial_creds + 2)  




class ShopTests(TestCase):
    def setUp(self):
        """Set up test user and some items"""
        self.client = Client()

        # Sets up mock shop
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass", current_points=200
        )
        self.client.force_login(self.user)
        self.item1 = Item.objects.create(
            name="Solar Panel", price=100, sustainability_score=10
        )
        self.item2 = Item.objects.create(
            name="Wind Turbine", price=300, sustainability_score=20
        )

    def test_shop_view(self):
        """Test if shop page loads and displays items"""
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("shop"))
        
        # Check if the shop displays the items
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Solar Panel")
        self.assertContains(response, "Wind Turbine")

    def test_buy_success(self):
        """Test if an item can be bought successfully"""
        self.client.force_login(user=self.user)
        response = self.client.post(reverse("buy_item", args=[self.item1.id]))

        self.user.refresh_from_db()

        # Sets carbo coins to 100
        self.assertEqual(self.user.current_points, 100)
        self.assertTrue(
            UserItem.objects.filter(item=self.item1).exists()
        )

        # Check if the buy success comes through
        messages = list(response.wsgi_request._messages)
        self.assertIn(
            "You bought Solar Panel and placed it on the map!", str(messages[0])
        )

    def test_buy_insufficient_points(self):
        """Test that item cant be bought if not enough points"""

        # Sets the user's current points to 50
        self.user.current_points = 50
        self.user.save()

        self.client.force_login(user=self.user)
        response = self.client.post(reverse("buy_item", args=[self.item2.id]))

        self.user.refresh_from_db()
        self.assertEqual(self.user.current_points, 50)

        # Check if the item exists
        self.assertFalse(
            UserItem.objects.filter(item=self.item2).exists()
        )

        # check if the error message is sent 
        messages = list(response.wsgi_request._messages)
        self.assertIn("Not enough Carbo Coins!", str(messages[0]))

    def test_buy_item_does_not_exist(self):
            """Test trying to buy a non-existent item."""

            # Make non-existent item request
            response = self.client.post(reverse("buy_item", args=[999])) 

            # No items should be added
            self.assertEqual(UserItem.objects.filter(useritem=self.user).count(), 0)  

            # Check for error message
            messages = [msg.message for msg in get_messages(response.wsgi_request)]
            self.assertIn("Item not found!", messages)

    def test_buy_item_updates_user_points(self):
        """Test that buying an item deducts the correct amount of Carbo Coins."""
        # Ensure the user has 200 points initially
        self.assertEqual(self.user.current_points, 200)

        # Buy the item (using the correct item ID)
        response = self.client.post(reverse("buy_item", args=[self.item1.id]))

        # Reload user data from the database
        self.user.refresh_from_db()

        # Check that the points have been deducted correctly
        self.assertEqual(self.user.current_points, 100)
    
    def test_buy_item_updates_campus_creds(self):
        """Test that after buying an item, the user's campus creds are correctly updated."""
        
        # Ensure user is logged in
        self.client.force_login(self.user)
        
        # Get an item with a known sustainability score
        item = Item.objects.create(name="Solar Panel", price=50, sustainability_score=10)
        
        # Set initial campus creds
        initial_creds = self.user.all_time_points

        # Attempt to buy the item
        response = self.client.post(reverse("buy_item", kwargs={"item_id": item.id}))

        # Refresh user data from the database
        self.user.refresh_from_db()

        # Assert that the sustainability score is added to campus creds
        self.assertEqual(self.user.all_time_points, initial_creds + item.sustainability_score)
        

