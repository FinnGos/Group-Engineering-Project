"""Tests the model system is working properly"""
from django.test import TestCase
from collectables.tests.test_views import TEST_IMAGES
from collectables.models import Collectable

COLLECTABLE_NAME = "test name"
UNUSED_NAME = "testtesttest"        
class CollectableTest(TestCase):
    """Tests the collectable model works as expected"""
        
    def setUp(self):
        """Sets up a test collectable"""
        self.test_collectable = Collectable(
            name = COLLECTABLE_NAME,
            image = TEST_IMAGES[0],
            fact = "Fact 1"
            )
        self.test_collectable.save()

    def test_no_duplicate_names(self):
        """Tests that adding a collectable with the non-unique name won't be added"""
        expected = len(Collectable.objects.all())

        # Adding matching name collectable
        Collectable(
            name = COLLECTABLE_NAME,
            image = TEST_IMAGES[1],
            fact = "Fact 2"
            )
        actual = len(Collectable.objects.all())
        self.assertEqual(expected, actual)

    def test_defaults_values(self):
        """Tests that when specific values are given, the correct defaults are given"""
        collectable_object = Collectable(
            name = "default test"
        )

        self.assertEqual(
            collectable_object.image,
            "placeholder.jpg"
            )
        self.assertEqual(
            collectable_object.fact,
            ""
        )

    def test_basic_functionality(self):
        """Tests that model retains valid values"""
        expected_name = f"{COLLECTABLE_NAME}123"
        expected_fact = "facts facts facts 123"

        collectable_object = Collectable(
            name = expected_name,
            image = TEST_IMAGES[1],
            fact = expected_fact
        )

        self.assertEqual(
            collectable_object.name,
            expected_name
        )
        self.assertEqual(
            collectable_object.image,
            TEST_IMAGES[1]
        )
        self.assertEqual(
            collectable_object.fact,
            expected_fact
        )
