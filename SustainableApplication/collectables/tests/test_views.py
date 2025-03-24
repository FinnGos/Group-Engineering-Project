"""Tests the webpage is displayed correctly"""
from django.test import TestCase, Client
from home.models import CustomUser
from collectables.models import Collectable


TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpassword"
# Should have 3 images
TEST_IMAGES = ["test_image_1.png",
               "test_image_2.png",
               "test_image_3.png"]

class TestCollectablesPage(TestCase):
    """Tests collectable webpage display"""

    def setUp(self):
        """Sets up a test user and test collectables"""
        self.client = Client()
        self.user = CustomUser.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        self.image_list = []
        for i in range(3):
            self.image_list.append(Collectable.objects.create(
                name = f"Test Image {i+1}",
                image = TEST_IMAGES[i],
                fact = f"Fact {i+1}"
            ))
            self.image_list[i].save()

    def test_webpage_response_code(self):
        """Tests collectables webpage gives the correct response code"""
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        response = self.client.get("/collectables/")
        self.assertEqual(response.status_code, 200)

    def test_webpage_displays_html_file(self):
        """Tests the collectables webpage uses the right html template"""
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        response = self.client.get("/collectables/")
        self.assertTemplateUsed(response, "collectables/gallery.html")

    def test_webpage_displays_no_collectables(self):
        """Tests that a basic user that owns no collectables will have an empty gallery"""
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        response = self.client.get("/collectables/")
        for collectable in self.image_list:
            self.assertNotContains(response, collectable.image.url)

    def test_webpage_displays_some_collectables(self):
        """Tests that a user with some collectables owned can only see what they own"""
        # Giving user collectables
        self.user.collectables_owned.add(self.image_list[0])
        self.user.collectables_owned.add(self.image_list[1])

        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        response = self.client.get("/collectables/")

        # Checks user can see owned images and not unowned
        self.assertContains(response, self.image_list[0].image.url)
        self.assertContains(response, self.image_list[1].image.url)
        self.assertNotContains(response, self.image_list[2].image.url)
