from django.test import TestCase, Client
from home.models import CustomUser
from django.urls import reverse
from .models import Item, UserItem


class ShopTests(TestCase):
    def setUp(self):
        """Set up test user and some items"""
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass", current_points=500
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
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Solar Panel")
        self.assertContains(response, "Wind Turbine")

    def test_buy_success(self):
        """Test if an item can be bought successfully"""
        self.client.force_login(user=self.user)
        response = self.client.post(reverse("buy_item", args=[self.item1.id]))

        self.user.refresh_from_db()
        self.assertEqual(self.user.current_points, 400)

        messages = list(response.wsgi_request._messages)
        self.assertIn(
            "You bought Solar Panel and placed it on the map!", str(messages[0])
        )

    def test_buy_insufficient_points(self):
        """Test that item cant be bought if not enough points"""
        self.user.current_points = 50
        self.user.save()

        self.client.force_login(user=self.user)
        response = self.client.post(reverse("buy_item", args=[self.item2.id]))

        self.user.refresh_from_db()
        self.assertEqual(self.user.current_points, 50)

        messages = list(response.wsgi_request._messages)
        self.assertIn("Not enough Carbo Coins!", str(messages[0]))
